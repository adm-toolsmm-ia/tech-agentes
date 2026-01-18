from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich import print

from tech_agents.context_scan import scan_repo
from tech_agents.scaffold import init_repo_scaffold
from tech_agents.schemas.plan_response import AgentRosterItem, PlanResponse, TaskItem
from tech_agents.schemas.common import ProjectRef, SLO
from tech_agents.schemas.configs import EnvironmentsConfig, ModelPolicy, ProjectConfig
from tech_agents.schemas.execution_log import ExecutionLog
from tech_agents.schemas.workflows import Backlog, ExecutionPlan
from tech_agents.evals.runner import EvalRunner
from tech_agents.utils import read_text, write_text_if_missing
from tech_agents.validate import RepoValidationError, validate_repo

app = typer.Typer(add_completion=False)


def _resolve_repo(path: str) -> Path:
    return Path(path).expanduser().resolve()


@app.command()
def scan(repo: str) -> None:
    """Detect type/phase and whether the repo already has local standards/configs."""
    r = _resolve_repo(repo)
    s = scan_repo(r)
    print(
        {
            "repo_root": str(s.repo_root),
            "project_type": s.project_type,
            "phase": s.phase,
            "is_multiagent": s.is_multiagent,
            "has_project_configs": s.has_project_configs,
            "has_project_standards": s.has_project_standards,
        }
    )


@app.command()
def init(
    repo: str,
    project_name: str = typer.Option(..., "--project-name"),
    tenant_id: str = typer.Option("", "--tenant-id"),
    env: str = typer.Option("dev", "--env"),
    approve_token: Optional[str] = typer.Option(None, "--approve-token"),
) -> None:
    """Install the full scaffold into a target repo (safe: does not overwrite existing files)."""
    if env in ("stage", "prod") and not approve_token:
        raise typer.Exit(code=3)
    r = _resolve_repo(repo)
    stats = init_repo_scaffold(r, project_name=project_name, tenant_id=tenant_id, environment=env)
    print({"ok": True, **stats})


@app.command()
def install_rules(repo: str) -> None:
    """Install or merge the repo rules into target .cursorrules (between markers)."""
    target = _resolve_repo(repo)
    src_rules = Path(__file__).resolve().parents[2] / ".cursorrules"
    content = read_text(src_rules)

    dst = target / ".cursorrules"
    if not dst.exists():
        write_text_if_missing(dst, content)
        print({"ok": True, "action": "created", "path": str(dst)})
        return

    existing = read_text(dst)
    begin = "# BEGIN TECH-AGENTES RULES"
    end = "# END TECH-AGENTES RULES"

    if begin in existing and end in existing:
        # Replace block
        pre = existing.split(begin)[0]
        post = existing.split(end, 1)[1]
        merged = pre + content + post
        dst.write_text(merged, encoding="utf-8", newline="\n")
        print({"ok": True, "action": "replaced_block", "path": str(dst)})
        return

    # Append safely
    dst.write_text(existing.rstrip() + "\n\n" + content + "\n", encoding="utf-8", newline="\n")
    print({"ok": True, "action": "appended", "path": str(dst)})


@app.command()
def validate(repo: str) -> None:
    """Validate configs/workflows (schemas + invariants)."""
    r = _resolve_repo(repo)
    try:
        summary = validate_repo(r)
    except RepoValidationError as e:
        raise typer.Exit(code=2) from e
    print(summary)


@app.command()
def eval(
    repo: str,
    env: str = typer.Option("dev", "--env"),
    outputs_json: Optional[str] = typer.Option(None, "--outputs-json"),
    cases: Optional[str] = typer.Option(None, "--cases"),
    use_expected: bool = typer.Option(False, "--use-expected"),
    allow_skip_llm_judge: bool = typer.Option(False, "--allow-skip-llm-judge"),
    model: str = typer.Option("n/a", "--model"),
    temperature: Optional[float] = typer.Option(None, "--temperature"),
    output: Optional[str] = typer.Option(None, "--output"),
    check_gate: bool = typer.Option(False, "--check-gate"),
) -> None:
    """Run golden sets evaluation using external outputs or expected outputs."""
    r = _resolve_repo(repo)
    golden_sets = r / "evals" / "golden_sets.json"
    rubricas = r / "evals" / "rubricas.json"
    output_dir = Path(output).resolve() if output else (r / "evals" / "resultados")
    case_ids = [c.strip() for c in cases.split(",")] if cases else None

    runner = EvalRunner(golden_sets, rubricas, output_dir)
    results = runner.run_all(
        environment=env,
        outputs_path=outputs_json,
        use_expected=use_expected,
        allow_skip_llm_judge=allow_skip_llm_judge,
        model=model,
        temperature=temperature,
        case_ids=case_ids,
    )
    print({"summary": results.get("summary"), "gate_status": results.get("gate_status")})
    if check_gate and not results.get("gate_status", {}).get("can_promote", False):
        raise typer.Exit(code=3)


@app.command()
def export(repo: str, out: Optional[str] = typer.Option(None, "--out")) -> None:
    """Export lightweight artifacts for tools like n8n/Make (MVP)."""
    r = _resolve_repo(repo)
    out_dir = Path(out).resolve() if out else (r / "outputs" / "artefatos_gerados")
    out_dir.mkdir(parents=True, exist_ok=True)

    scan_info = scan_repo(r)
    # Export tasks for workflow engines (generic JSON that n8n/Make can ingest).
    plan = ExecutionPlan.model_validate(json.loads(read_text(r / "workflows" / "plano_execucao.json")))
    backlog = Backlog.model_validate(json.loads(read_text(r / "workflows" / "backlog_tarefas.json")))

    schemas = {
        "ProjectConfig": ProjectConfig.model_json_schema(),
        "ModelPolicy": ModelPolicy.model_json_schema(),
        "EnvironmentsConfig": EnvironmentsConfig.model_json_schema(),
        "ExecutionPlan": ExecutionPlan.model_json_schema(),
        "Backlog": Backlog.model_json_schema(),
        "PlanResponse": PlanResponse.model_json_schema(),
        "ExecutionLog": ExecutionLog.model_json_schema(),
    }

    payload = {
        "repo_root": str(r),
        "scan": {
            "project_type": scan_info.project_type,
            "phase": scan_info.phase,
            "is_multiagent": scan_info.is_multiagent,
        },
        "workflows": {
            "plano_execucao": plan.model_dump(),
            "backlog_tarefas": backlog.model_dump(),
        },
    }
    (out_dir / "export.summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out_dir / "export.schemas.json").write_text(json.dumps(schemas, indent=2), encoding="utf-8")
    print({"ok": True, "path": str(out_dir / "export.summary.json")})


@app.command()
def sync(
    repo: str,
    from_version: str = typer.Option(..., "--from-version"),
    env: str = typer.Option("dev", "--env"),
    approve_token: Optional[str] = typer.Option(None, "--approve-token"),
) -> None:
    """
    Sync scaffold/templates from this base into a target repo (safe by default).
    MVP behavior: only adds missing files/dirs and writes a report.
    """
    if env in ("stage", "prod") and not approve_token:
        raise typer.Exit(code=3)
    r = _resolve_repo(repo)
    project_name = r.name
    cfg = r / "configs" / "projeto.json"
    if cfg.exists():
        try:
            project_name = json.loads(read_text(cfg)).get("name") or project_name
        except Exception:
            project_name = project_name

    stats = init_repo_scaffold(r, project_name=project_name, tenant_id="", environment=env)
    out_dir = r / "outputs" / "artefatos_gerados"
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"ok": True, "from_version": from_version, **stats}
    (out_dir / "sync_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(report)


@app.command()
def run(
    repo: str,
    workflow: str = typer.Option("workflows/plano_execucao.json", "--workflow"),
) -> None:
    """
    Run a workflow in MVP mode: generate a Plan/Response JSON artifact.
    (Does not execute external tools automatically.)
    """
    r = _resolve_repo(repo)
    cfg_path = r / "configs" / "projeto.json"
    cfg = json.loads(read_text(cfg_path)) if cfg_path.exists() else {"name": r.name, "environment": "dev"}

    wf_path = r / workflow
    wf = json.loads(read_text(wf_path))

    agent_roster = [
        AgentRosterItem(
            name="contexto_requisitos",
            type="base",
            mandate="Capturar/estruturar brief e manter contexto vivo.",
            inputs=["docs/brief/brief_atual.md", "configs/projeto.json"],
            outputs=["docs/brief/brief_atual.md", "workflows/backlog_tarefas.json"],
            tools=[],
            handoff_to=["orquestrador"],
        ),
        AgentRosterItem(
            name="orquestrador",
            type="base",
            mandate="Planejar, priorizar, delegar e supervisionar; sugerir specialists com ROI.",
            inputs=["docs/brief/brief_atual.md", "configs/projeto.json", "configs/modelos.json"],
            outputs=["workflows/plano_execucao.json", "workflows/backlog_tarefas.json"],
            tools=[],
            handoff_to=[],
        ),
        AgentRosterItem(
            name="engenharia_prompt",
            type="base",
            mandate="Converter objetivos em templates/prompt specs com formatos e critérios de sucesso.",
            inputs=["prompts/templates_*.md", "evals/golden_sets.json", "evals/rubricas.json"],
            outputs=["prompts/templates_*.md"],
            tools=[],
            handoff_to=["qualidade_auditoria_testes"],
        ),
        AgentRosterItem(
            name="seguranca_compliance",
            type="base",
            mandate="Proteger PII/segredos e auditar integrações; impor gates quando cabível.",
            inputs=["docs/seguranca/politicas.md", "configs/ambientes.json", "integrations/*"],
            outputs=["docs/seguranca/politicas.md"],
            tools=[],
            handoff_to=["orquestrador"],
        ),
        AgentRosterItem(
            name="observabilidade_custos",
            type="base",
            mandate="Instrumentar logs/métricas/custos; bloquear stage/prod sem instrumentação real.",
            inputs=["configs/projeto.json", "configs/modelos.json"],
            outputs=["observability/dashboards.json", "logs/costs.summary.json"],
            tools=[],
            handoff_to=["orquestrador"],
        ),
        AgentRosterItem(
            name="eng_software_arquiteto_ia_devops",
            type="base",
            mandate="Definir arquitetura/CI/CD/runbooks e ADRs para mudanças estruturais.",
            inputs=["docs/decisoes/adr/*", "devops/*"],
            outputs=["docs/decisoes/adr/*", "devops/*"],
            tools=[],
            handoff_to=["qualidade_auditoria_testes"],
        ),
        AgentRosterItem(
            name="qualidade_auditoria_testes",
            type="base",
            mandate="QA/Evals: contract tests + anti-alucinação + evidências antes de stage/prod.",
            inputs=["templates/qa/*", "evals/*"],
            outputs=["evals/resultados/*"],
            tools=[],
            handoff_to=["orquestrador"],
        ),
    ]

    tasks = [
        TaskItem(
            id=t["id"],
            assigned_to=t["assigned_to"],
            goal=t["goal"],
            acceptance_criteria=t.get("acceptance_criteria", []),
            deliverable_format=t.get("deliverable_format", ""),
            deadline=t.get("deadline", ""),
        )
        for t in wf.get("tasks", [])
    ]

    pr = PlanResponse(
        project=ProjectRef(
            name=cfg.get("name", r.name),
            version=cfg.get("version", "0.1.0"),
            environment=cfg.get("environment", "dev"),
            tenant_id=cfg.get("tenant_id", ""),
            repo_root=str(r),
        ),
        slo=SLO(),
        agent_roster=agent_roster,
        tasks=tasks,
        open_questions=[],
        security_findings=[],
        recommendations=[],
        file_ops=[],
        next_actions=[
            "Atualizar docs/brief/brief_atual.md com contexto e escopo",
            "Registrar riscos de segurança/compliance (PII, segredos, integrações)",
            "Confirmar política de instrumentação e gates para stage/prod",
        ],
    )

    out_dir = r / "outputs" / "artefatos_gerados"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "plan_response.json").write_text(pr.model_dump_json(indent=2), encoding="utf-8")
    print({"ok": True, "path": str(out_dir / "plan_response.json")})


if __name__ == "__main__":
    app()

