from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from tech_agents.schemas.configs import EnvironmentsConfig, ModelPolicy, ProjectConfig
from tech_agents.schemas.execution_log import ExecutionLog
from tech_agents.schemas.plan_response import PlanResponse
from tech_agents.schemas.workflows import Backlog, ExecutionPlan
from tech_agents.utils import read_text


class RepoValidationError(Exception):
    pass


def _read_json(path: Path) -> Any:
    return json.loads(read_text(path))


# Placeholder patterns to detect incomplete templates
PLACEHOLDER_PATTERNS = [
    r">\s*Placeholder gerado por tech-agentes",
    r"^\s*#\s+\[Nome\]",
    r"\[PREENCHER\]",
    r"\[TODO\]",
    r"\[DATA\]",
    r"\[YYYY-MM-DD\]",
]


def _is_placeholder(content: str) -> bool:
    """Check if content is a placeholder template."""
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            return True
    # Also check if file is too short (likely placeholder)
    lines = [line for line in content.strip().split("\n") if line.strip()]
    if len(lines) <= 3:
        return True
    return False


def _validate_not_placeholder(file_path: Path, errors: list[str]) -> None:
    """Validate that a file is not just a placeholder."""
    if not file_path.exists():
        errors.append(f"{file_path}: File does not exist")
        return

    content = read_text(file_path)
    if _is_placeholder(content):
        errors.append(f"{file_path}: File appears to be a placeholder (incomplete content)")


def _validate_readme_exists(directory: Path, errors: list[str]) -> None:
    """Validate that a README.md exists in the directory."""
    readme_path = directory / "README.md"
    if not readme_path.exists():
        errors.append(f"{directory}: Missing README.md")
    elif _is_placeholder(read_text(readme_path)):
        errors.append(f"{readme_path}: README is a placeholder")


def _validate_golden_sets(repo_root: Path, errors: list[str], min_cases: int = 2) -> None:
    """Validate that golden_sets.json has minimum required cases."""
    golden_path = repo_root / "evals" / "golden_sets.json"
    if not golden_path.exists():
        errors.append(f"{golden_path}: Golden sets file does not exist")
        return

    try:
        data = _read_json(golden_path)
        cases = data.get("cases", [])
        if len(cases) < min_cases:
            errors.append(
                f"{golden_path}: Insufficient golden set cases "
                f"(found {len(cases)}, minimum {min_cases})"
            )
    except Exception as e:
        errors.append(f"{golden_path}: Failed to validate - {e}")


def _validate_rubricas(repo_root: Path, errors: list[str], min_rubrics: int = 2) -> None:
    """Validate that rubricas.json has minimum required rubrics."""
    rubricas_path = repo_root / "evals" / "rubricas.json"
    if not rubricas_path.exists():
        errors.append(f"{rubricas_path}: Rubricas file does not exist")
        return

    try:
        data = _read_json(rubricas_path)
        rubrics = data.get("rubrics", [])
        if len(rubrics) < min_rubrics:
            errors.append(
                f"{rubricas_path}: Insufficient rubrics "
                f"(found {len(rubrics)}, minimum {min_rubrics})"
            )
    except Exception as e:
        errors.append(f"{rubricas_path}: Failed to validate - {e}")


def _validate_agents(repo_root: Path, errors: list[str]) -> None:
    """Validate that agent files have required sections."""
    agents_dir = repo_root / "agents"
    if not agents_dir.exists():
        errors.append(f"{agents_dir}: Agents directory does not exist")
        return

    required_sections = ["## Mandato", "## Entradas", "## Saídas", "## Regras"]

    for agent_file in agents_dir.glob("*.md"):
        if agent_file.name == "README.md":
            continue

        content = read_text(agent_file)
        missing_sections = []

        for section in required_sections:
            if section not in content:
                missing_sections.append(section)

        if missing_sections:
            errors.append(
                f"{agent_file}: Missing required sections: {', '.join(missing_sections)}"
            )


def _validate_security_policies(repo_root: Path, errors: list[str]) -> None:
    """Validate that security policies are properly defined."""
    policies_path = repo_root / "docs" / "seguranca" / "politicas.md"
    if not policies_path.exists():
        errors.append(f"{policies_path}: Security policies file does not exist")
        return

    content = read_text(policies_path)

    # Check for essential sections
    required_sections = [
        "Classificação de Dados",
        "Gestão de Segredos",
        "LGPD",
        "Controle de Acesso",
    ]

    missing = [s for s in required_sections if s.lower() not in content.lower()]
    if missing:
        errors.append(
            f"{policies_path}: Missing security sections: {', '.join(missing)}"
        )


def _validate_critical_templates(repo_root: Path, errors: list[str]) -> None:
    """Validate that critical templates are not placeholders."""
    critical_templates = [
        "templates/devops/01_ci_cd_pipeline.md",
        "templates/qa/02_qa_checklist.md",
        "templates/security/01_security_privacy_assessment.md",
    ]

    for template in critical_templates:
        template_path = repo_root / template
        _validate_not_placeholder(template_path, errors)


def validate_repo(repo_root: Path, strict: bool = False) -> dict[str, Any]:
    """
    Validate a repo against the base schemas + critical invariants.

    Args:
        repo_root: Path to the repository root
        strict: If True, also validates templates, READMEs, and completeness

    Returns:
        Summary dict with validation results

    Raises:
        RepoValidationError: On validation failure
    """
    repo_root = repo_root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    def capture(label: str, fn) -> None:
        try:
            fn()
        except (ValidationError, json.JSONDecodeError, RepoValidationError, Exception) as e:
            errors.append(f"{label}: {e}")

    project_cfg: ProjectConfig | None = None

    def _validate_project() -> None:
        nonlocal project_cfg
        project_cfg = ProjectConfig.model_validate(_read_json(repo_root / "configs" / "projeto.json"))

    # Core schema validations
    capture("configs/projeto.json", _validate_project)
    capture(
        "configs/modelos.json",
        lambda: ModelPolicy.model_validate(_read_json(repo_root / "configs" / "modelos.json")),
    )
    capture(
        "configs/ambientes.json",
        lambda: EnvironmentsConfig.model_validate(_read_json(repo_root / "configs" / "ambientes.json")),
    )
    capture(
        "workflows/plano_execucao.json",
        lambda: ExecutionPlan.model_validate(_read_json(repo_root / "workflows" / "plano_execucao.json")),
    )
    capture(
        "workflows/backlog_tarefas.json",
        lambda: Backlog.model_validate(_read_json(repo_root / "workflows" / "backlog_tarefas.json")),
    )

    # Optional artifacts: validate if present and non-empty
    plan_response_path = repo_root / "outputs" / "artefatos_gerados" / "plan_response.json"
    if plan_response_path.exists():
        capture("outputs/.../plan_response.json", lambda: PlanResponse.model_validate(_read_json(plan_response_path)))

    sample_log_path = repo_root / "outputs" / "artefatos_gerados" / "execution_log.sample.json"
    if sample_log_path.exists():
        capture("outputs/.../execution_log.sample.json", lambda: ExecutionLog.model_validate(_read_json(sample_log_path)))

    # Extended validations (strict mode or stage/prod)
    is_production = project_cfg and project_cfg.environment in ("stage", "prod")

    if strict or is_production:
        # Validate READMEs exist in main directories
        main_dirs = [
            "agents", "configs", "workflows", "prompts", "templates",
            "observability", "evals", "devops", "integrations"
        ]
        for dir_name in main_dirs:
            dir_path = repo_root / dir_name
            if dir_path.exists():
                _validate_readme_exists(dir_path, warnings if not strict else errors)

        # Validate agents have required sections
        _validate_agents(repo_root, errors)

        # Validate security policies
        _validate_security_policies(repo_root, errors)

        # Validate golden sets and rubricas
        _validate_golden_sets(repo_root, errors)
        _validate_rubricas(repo_root, errors)

        # Validate critical templates are not placeholders
        _validate_critical_templates(repo_root, warnings if not is_production else errors)

    # Environment-specific gates
    if is_production:
        if project_cfg.instrumentation.provider == "none" or project_cfg.instrumentation.enabled is False:
            errors.append(
                f"env={project_cfg.environment} requires instrumentation enabled (provider != none)."
            )

    if errors:
        raise RepoValidationError(" | ".join(errors))

    result = {
        "ok": True,
        "validated": True,
        "environment": project_cfg.environment if project_cfg else "unknown",
        "strict_mode": strict,
    }

    if warnings:
        result["warnings"] = warnings

    return result


def validate_completeness(repo_root: Path) -> dict[str, Any]:
    """
    Comprehensive validation for enterprise standard compliance.

    Checks:
    - All directories have READMEs
    - No placeholder templates in critical paths
    - Golden sets and rubricas meet minimums
    - Security policies are complete
    - Agents have required structure

    Returns:
        Detailed report with scores and gaps
    """
    repo_root = repo_root.resolve()

    report = {
        "score": 0,
        "max_score": 100,
        "passed": [],
        "failed": [],
        "warnings": [],
    }

    checks = [
        ("Schema validation", 20, lambda: validate_repo(repo_root)),
        ("Security policies", 15, lambda: _check_security(repo_root)),
        ("Agent structure", 15, lambda: _check_agents(repo_root)),
        ("Golden sets", 10, lambda: _check_golden_sets(repo_root)),
        ("READMEs", 10, lambda: _check_readmes(repo_root)),
        ("Critical templates", 15, lambda: _check_templates(repo_root)),
        ("Observability", 10, lambda: _check_observability(repo_root)),
        ("DevOps", 5, lambda: _check_devops(repo_root)),
    ]

    for check_name, points, check_fn in checks:
        try:
            check_fn()
            report["passed"].append(check_name)
            report["score"] += points
        except Exception as e:
            report["failed"].append({"check": check_name, "error": str(e), "points_lost": points})

    report["grade"] = _calculate_grade(report["score"])
    report["enterprise_ready"] = report["score"] >= 70

    return report


def _check_security(repo_root: Path) -> None:
    errors = []
    _validate_security_policies(repo_root, errors)
    if errors:
        raise RepoValidationError("; ".join(errors))


def _check_agents(repo_root: Path) -> None:
    errors = []
    _validate_agents(repo_root, errors)
    if errors:
        raise RepoValidationError("; ".join(errors))


def _check_golden_sets(repo_root: Path) -> None:
    errors = []
    _validate_golden_sets(repo_root, errors, min_cases=2)
    _validate_rubricas(repo_root, errors, min_rubrics=2)
    if errors:
        raise RepoValidationError("; ".join(errors))


def _check_readmes(repo_root: Path) -> None:
    errors = []
    main_dirs = ["agents", "configs", "workflows", "prompts", "templates", "evals", "devops"]
    for dir_name in main_dirs:
        dir_path = repo_root / dir_name
        if dir_path.exists():
            _validate_readme_exists(dir_path, errors)
    if errors:
        raise RepoValidationError("; ".join(errors))


def _check_templates(repo_root: Path) -> None:
    errors = []
    _validate_critical_templates(repo_root, errors)
    if errors:
        raise RepoValidationError("; ".join(errors))


def _check_observability(repo_root: Path) -> None:
    dashboards_path = repo_root / "observability" / "dashboards.json"
    if not dashboards_path.exists():
        raise RepoValidationError(f"{dashboards_path}: File does not exist")

    data = _read_json(dashboards_path)
    if not data.get("metrics"):
        raise RepoValidationError(f"{dashboards_path}: No metrics defined")


def _check_devops(repo_root: Path) -> None:
    pipelines_path = repo_root / "devops" / "pipelines.yaml"
    if not pipelines_path.exists():
        raise RepoValidationError(f"{pipelines_path}: File does not exist")

    content = read_text(pipelines_path)
    if len(content.strip()) < 50:
        raise RepoValidationError(f"{pipelines_path}: Pipeline appears incomplete")


def _calculate_grade(score: int) -> str:
    """Calculate letter grade from score."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
