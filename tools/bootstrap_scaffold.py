from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tech_agents.scaffold_manifest import base_scaffold, placeholder_md  # noqa: E402
from tech_agents.utils import write_text_if_missing  # noqa: E402


TEMPLATES_FULL = [
    "templates/project/01_project_brief.md",
    "templates/project/02_sow_scope.md",
    "templates/project/03_raci_stakeholders.md",
    "templates/project/04_kpis_okrs.md",
    "templates/project/05_risk_register.md",
    "templates/requirements/01_brd_negocio.md",
    "templates/requirements/02_frd_funcional.md",
    "templates/requirements/03_user_stories.md",
    "templates/architecture/01_system_architecture.md",
    "templates/architecture/02_adr_template.md",
    "templates/architecture/03_c4_context_container.md",
    "templates/data/01_data_contract.md",
    "templates/data/02_data_dictionary.md",
    "templates/data/03_migration_etl_plan.md",
    "templates/integrations/01_api_integration_spec.md",
    "templates/integrations/02_mapping_sheet.md",
    "templates/security/01_security_privacy_assessment.md",
    "templates/security/02_threat_model_stride.md",
    "templates/security/03_access_control_matrix.md",
    "templates/security/04_secrets_management.md",
    "templates/ai_llm/01_model_selection_log.md",
    "templates/ai_llm/02_prompt_spec_template.md",
    "templates/ai_llm/03_eval_plan_golden_sets.md",
    "templates/devops/01_ci_cd_pipeline.md",
    "templates/devops/02_iac_overview.md",
    "templates/devops/03_runbook_operacao.md",
    "templates/devops/04_release_plan.md",
    "templates/qa/01_test_plan.md",
    "templates/qa/02_qa_checklist.md",
    "templates/qa/03_contract_tests.md",
    "templates/observability/01_logging_metrics_plan.md",
    "templates/observability/02_cost_management_plan.md",
    "templates/operations/01_sop_suporte.md",
    "templates/operations/02_incident_response.md",
    "templates/operations/03_backup_dr_plan.md",
    "templates/legal/01_oss_licensing_compliance.md",
]


def main() -> None:
    repo_root = REPO_ROOT
    dirs, files = base_scaffold()

    for d in dirs:
        (repo_root / d.path).mkdir(parents=True, exist_ok=True)

    for f in files:
        write_text_if_missing(repo_root / f.path, f.content)

    for path in TEMPLATES_FULL:
        title = path.split("/")[-1]
        write_text_if_missing(repo_root / path, placeholder_md(title))

    print("Scaffold bootstrap complete.")


if __name__ == "__main__":
    main()

