# Templates

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém templates padronizados para documentação, planejamento e operação de projetos no framework tech-agentes. Os templates são organizados por domínio e fornecem estruturas reutilizáveis para garantir consistência e qualidade.

---

## Princípio de Uso

**Adapte, não engesse**: Templates são pontos de partida. Cada projeto deve:

1. **Avaliar aplicabilidade**: Nem todo template é necessário para todo projeto
2. **Adaptar ao contexto**: Remover seções não aplicáveis, adicionar específicas
3. **Manter consistência**: Usar a estrutura base para facilitar navegação
4. **Versionar mudanças**: Alterações significativas devem ser versionadas

---

## Índice de Templates por Categoria

### AI/LLM (`ai_llm/`)

Templates para projetos que utilizam modelos de linguagem.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_model_selection_log.md`](ai_llm/01_model_selection_log.md) | Registro de seleção de modelo | Escolha inicial de LLM |
| [`02_prompt_spec_template.md`](ai_llm/02_prompt_spec_template.md) | Especificação formal de prompt | Prompts críticos em produção |
| [`03_eval_plan_golden_sets.md`](ai_llm/03_eval_plan_golden_sets.md) | Plano de avaliação | Validação de qualidade |

### Arquitetura (`architecture/`)

Templates para decisões e documentação arquitetural.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_system_architecture.md`](architecture/01_system_architecture.md) | Visão geral da arquitetura | Início de projeto |
| [`02_adr_template.md`](architecture/02_adr_template.md) | Architecture Decision Record | Decisões técnicas significativas |
| [`03_c4_context_container.md`](architecture/03_c4_context_container.md) | Diagramas C4 | Documentação visual |

### Dados (`data/`)

Templates para governança e contratos de dados.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_data_contract.md`](data/01_data_contract.md) | Contrato de dados | Integrações, consumo de dados |
| [`02_data_dictionary.md`](data/02_data_dictionary.md) | Dicionário de dados | Modelagem de dados |
| [`03_migration_etl_plan.md`](data/03_migration_etl_plan.md) | Plano de migração/ETL | ETL, integrações |

### DevOps (`devops/`)

Templates para CI/CD, infraestrutura e operações.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_ci_cd_pipeline.md`](devops/01_ci_cd_pipeline.md) | Pipeline de CI/CD | Setup de automação |
| [`02_iac_overview.md`](devops/02_iac_overview.md) | Infraestrutura como código | Setup de infra |
| [`03_runbook_operacao.md`](devops/03_runbook_operacao.md) | Runbook operacional | Procedimentos de suporte |
| [`04_release_plan.md`](devops/04_release_plan.md) | Plano de release | Lançamentos coordenados |

### Integrações (`integrations/`)

Templates para APIs e integrações externas.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_api_integration_spec.md`](integrations/01_api_integration_spec.md) | Especificação de integração | Nova integração |
| [`02_mapping_sheet.md`](integrations/02_mapping_sheet.md) | Mapeamento de dados | ETL, sincronização |

### Legal (`legal/`)

Templates para compliance e aspectos legais.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_oss_licensing_compliance.md`](legal/01_oss_licensing_compliance.md) | Compliance de licenças OSS | Uso de dependências |

### Observabilidade (`observability/`)

Templates para logging, métricas e monitoramento.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_logging_metrics_plan.md`](observability/01_logging_metrics_plan.md) | Plano de observabilidade | Setup de monitoramento |
| [`02_cost_management_plan.md`](observability/02_cost_management_plan.md) | Gestão de custos | Controle de budget |

### Operações (`operations/`)

Templates para operação e suporte.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_incident_report.md`](operations/01_incident_report.md) | Relatório de incidente | Pós-mortem |
| [`02_change_request.md`](operations/02_change_request.md) | Requisição de mudança | Mudanças em prod |
| [`03_maintenance_window.md`](operations/03_maintenance_window.md) | Janela de manutenção | Manutenções programadas |

### Projeto (`project/`)

Templates para gestão de projeto.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_project_brief.md`](project/01_project_brief.md) | Brief do projeto | Início de projeto |
| [`02_sow_scope.md`](project/02_sow_scope.md) | Escopo/SOW | Planejamento |
| [`03_raci_stakeholders.md`](project/03_raci_stakeholders.md) | RACI & stakeholders | Governança |
| [`04_kpis_okrs.md`](project/04_kpis_okrs.md) | KPIs & OKRs | Metas e sucesso |
| [`05_risk_register.md`](project/05_risk_register.md) | Registro de riscos | Gestão de riscos |

### QA (`qa/`)

Templates para qualidade e testes.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_test_plan.md`](qa/01_test_plan.md) | Plano de testes | Estratégia de QA |
| [`02_qa_checklist.md`](qa/02_qa_checklist.md) | Checklist de qualidade | Gates de release |
| [`03_contract_tests.md`](qa/03_contract_tests.md) | Testes de contrato | Integrações |

### Requisitos (`requirements/`)

Templates para captura de requisitos.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_brd_negocio.md`](requirements/01_brd_negocio.md) | BRD (Negócio) | Visão e objetivos |
| [`02_frd_funcional.md`](requirements/02_frd_funcional.md) | FRD (Funcional) | Requisitos funcionais |
| [`03_user_stories.md`](requirements/03_user_stories.md) | User stories | Detalhamento de casos |

### Segurança (`security/`)

Templates para segurança e compliance.

| Template | Descrição | Quando Usar |
|----------|-----------|-------------|
| [`01_security_privacy_assessment.md`](security/01_security_privacy_assessment.md) | Assessment de segurança | Avaliação inicial |
| [`02_threat_model_stride.md`](security/02_threat_model_stride.md) | Threat modeling STRIDE | Análise de ameaças |
| [`03_access_control_matrix.md`](security/03_access_control_matrix.md) | Matriz de acesso | RBAC/ABAC |
| [`04_secrets_management.md`](security/04_secrets_management.md) | Gestão de segredos | Credenciais |

---

## Guia de Seleção de Templates

### Por Fase do Projeto

| Fase | Templates Essenciais |
|------|---------------------|
| **Kick-off** | Project Brief, RACI & Stakeholders, Risk Register |
| **Discovery** | User Stories, Data Dictionary, System Architecture |
| **Design** | ADR, C4 Diagrams, API Spec, Threat Model |
| **Desenvolvimento** | Test Plan, CI/CD Pipeline, Logging Plan |
| **QA** | QA Checklist, Contract Tests, Golden Sets |
| **Deploy** | Runbook, Release Plan, Security Assessment |
| **Operação** | Incident Report, Change Request, Maintenance |

### Por Tipo de Projeto

| Tipo | Templates Prioritários |
|------|----------------------|
| **API/Backend** | System Architecture, API Spec, Runbook, Logging Plan |
| **Frontend** | User Stories, Test Plan, Release Plan |
| **Data/ETL** | Data Dictionary, Data Flow, Contract Tests, Mapping Sheet |
| **AI/LLM** | Prompt Spec, Eval Plan, Model Selection, Security Assessment |
| **Integração** | API Integration Spec, Mapping Sheet, Contract Tests |

---

## Como Usar um Template

### 1. Copiar para o Projeto

```bash
# Copiar template específico
cp templates/devops/01_ci_cd_pipeline.md docs/devops/pipeline.md

# Ou criar estrutura completa
# (CLI tech-agentes não faz parte deste repositório)
```

### 2. Preencher Metadados

Cada template inicia com metadados que devem ser preenchidos:

```markdown
| Campo | Valor |
|-------|-------|
| **Projeto** | [Preencher] |
| **Data** | [YYYY-MM-DD] |
| **Responsável** | [Nome] |
```

### 3. Adaptar Seções

- **Manter**: Seções aplicáveis ao contexto
- **Remover**: Seções não aplicáveis (marcar como N/A se preferir manter estrutura)
- **Adicionar**: Seções específicas do projeto

### 4. Revisar e Aprovar

Templates preenchidos devem ser revisados conforme governança do projeto:

| Template | Revisor |
|----------|---------|
| Security Assessment | Security Lead + CTO |
| ADR | Tech Lead + CTO |
| Runbook | DevOps + On-call team |

---

## Criando Novos Templates

### Estrutura Padrão

```markdown
# Template: [Nome do Template]

> **Versão**: X.Y.Z
> **Categoria**: [Categoria]
> **Uso**: [Descrição curta de quando usar]

---

## Metadados

| Campo | Valor |
|-------|-------|
| **Projeto** | [Nome] |
| **Data** | [YYYY-MM-DD] |
| **Responsável** | [Nome] |

---

## 1. [Primeira Seção]

### 1.1 [Subseção]
[Conteúdo]

---

## 2. [Segunda Seção]
[...]

---

## Checklist de Validação

- [ ] Item 1
- [ ] Item 2

---

## Histórico

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
```

### Processo de Criação

1. Identificar necessidade não coberta
2. Criar draft seguindo estrutura padrão
3. Validar com usuários potenciais
4. Review por Tech Lead
5. Adicionar ao índice deste README
6. Documentar em prompts se usado por agentes

---

## Versionamento

### Política de Versão

- **Patch (X.Y.Z)**: Correções de typos, clarificações
- **Minor (X.Y.0)**: Novas seções opcionais, melhorias
- **Major (X.0.0)**: Mudanças estruturais breaking

### Changelog

Mudanças significativas devem ser documentadas em cada template e neste README.

---

## Referências

- [Políticas de Segurança](../docs/seguranca/politicas.md)
- [Padrões do Projeto](../docs/padrões/padroes_projeto.md)
- [Prompts de Análise](../prompts/templates_analise.md)
- [Golden Sets](../evals/golden_sets.json)
