from __future__ import annotations

import json
from pathlib import Path

from tech_agents.context_scan import scan_repo
from tech_agents.scaffold_manifest import base_scaffold
from tech_agents.utils import read_text, write_json_if_missing, write_text_if_missing


def init_repo_scaffold(
    target_repo: Path,
    project_name: str,
    tenant_id: str,
    environment: str,
) -> dict[str, int]:
    """
    Create the full scaffold in a target repo without overwriting existing files.
    Returns counters of created dirs/files.
    """
    target_repo = target_repo.resolve()
    created_dirs = 0
    created_files = 0

    dirs, files = base_scaffold()
    for d in dirs:
        p = target_repo / d.path
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            created_dirs += 1

    for f in files:
        if write_text_if_missing(target_repo / f.path, f.content):
            created_files += 1

    # Defaults for configs (only if missing)
    write_json_if_missing(
        target_repo / "configs" / "projeto.json",
        {
            "name": project_name,
            "version": "0.1.0",
            "owners": [],
            "environment": environment,
            "tenant_id": tenant_id,
            "deadlines": {},
            "kpis": [],
            "acceptance_criteria": [],
            "constraints": [],
            "budgets": {"run_usd": 0, "daily_usd": 0, "project_usd": 0},
            "slo": {"latency_s": 8, "critical_error_rate_max": 0.01, "daily_budget_usd": 0},
            "instrumentation": {"provider": "none", "enabled": False, "notes": "Enable for stage/prod."},
        },
    )
    write_json_if_missing(
        target_repo / "configs" / "modelos.json",
        {
            "version": "1.0.0",
            "pricing_version": "2024-01",
            "thresholds": {},
            "defaults": {
                "architecture": {"temperature": 0.2, "top_p": 0.9},
                "extraction": {"temperature": 0.1, "top_p": 1.0},
                "chat": {"temperature": 0.4, "top_p": 0.95},
            },
            "routing": [
                {
                    "task_class": "architecture|compliance|context_long",
                    "preferred": ["gpt-4o", "claude-3-opus", "gemini-1.5-pro"],
                    "fallback": ["gpt-4o-mini", "claude-3-sonnet"],
                    "max_temperature": 0.3,
                },
                {
                    "task_class": "templated_generation|semi_structured_extraction",
                    "preferred": ["gpt-4o", "claude-3-sonnet", "gemini-1.5-pro"],
                    "fallback": ["gpt-4o-mini"],
                    "max_temperature": 0.5,
                },
                {
                    "task_class": "parsing|classification_simple",
                    "preferred": ["gpt-4o-mini"],
                    "fallback": ["gpt-4o"],
                    "max_temperature": 0.3,
                },
            ],
        },
    )
    write_json_if_missing(
        target_repo / "configs" / "ambientes.json",
        {"version": "1.0.0", "dev": {"refs": {}}, "stage": {"refs": {}}, "prod": {"refs": {}}},
    )

    # Workflows default (if missing / empty)
    plan_path = target_repo / "workflows" / "plano_execucao.json"
    if plan_path.exists():
        try:
            raw = json.loads(read_text(plan_path) or "{}")
        except Exception:
            raw = {}
        if not raw:
            plan_path.write_text(
                json.dumps(
                    {
                        "version": "0.1.0",
                        "environment": environment,
                        "tasks": [
                            {
                                "id": "init-brief",
                                "assigned_to": "contexto_requisitos",
                                "goal": "Capturar brief e open_questions; atualizar docs/brief/brief_atual.md",
                                "acceptance_criteria": [
                                    "Brief atualizado com escopo e fora de escopo",
                                    "Lista de perguntas abertas priorizada",
                                ],
                                "deliverable_format": "md",
                                "deadline": "",
                            }
                        ],
                        "recommendations": [],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    backlog_path = target_repo / "workflows" / "backlog_tarefas.json"
    if backlog_path.exists():
        try:
            raw = json.loads(read_text(backlog_path) or "{}")
        except Exception:
            raw = {}
        if not raw:
            backlog_path.write_text(
                json.dumps({"version": "0.1.0", "items": []}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    return {"created_dirs": created_dirs, "created_files": created_files}


def should_respect_project_overrides(target_repo: Path) -> bool:
    scan = scan_repo(target_repo)
    return scan.has_project_configs or scan.has_project_standards

