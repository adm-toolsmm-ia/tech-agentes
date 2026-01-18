# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- (próximas features serão listadas aqui)

### Changed
- (próximas mudanças serão listadas aqui)

---

## [0.1.0] - 2026-01-18

### Added

#### Core Framework
- Estrutura base do projeto tech-agentes
- CLI com comandos: `scan`, `init`, `install-rules`, `validate`, `export`, `sync`
- Schemas Pydantic para validação de configs e workflows
- `.cursorrules` com hierarquia de decisão e políticas

#### Agentes Base (7 agentes)
- `orquestrador`: Planejamento, priorização e delegação
- `contexto_requisitos`: Captura e manutenção de contexto do projeto
- `engenharia_prompt`: Criação e versionamento de prompts
- `seguranca_compliance`: LGPD, PII, gestão de segredos
- `qualidade_auditoria_testes`: QA, evals, gates de qualidade
- `observabilidade_custos`: Métricas, logging, budgets
- `eng_software_arquiteto_ia_devops`: Arquitetura, CI/CD, runbooks

#### Configurações
- `configs/projeto.json`: Configuração principal do projeto
- `configs/modelos.json`: Política de roteamento de modelos LLM
- `configs/ambientes.json`: Referências de segredos por ambiente

#### Workflows
- `workflows/plano_execucao.json`: Plano executável de tarefas
- `workflows/backlog_tarefas.json`: Backlog priorizado

#### Templates (36 templates em 12 categorias)
- `templates/ai_llm/`: Model selection, prompt spec, eval plan
- `templates/architecture/`: System arch, ADR, C4
- `templates/data/`: Data modeling, ETL, dictionary
- `templates/devops/`: CI/CD, IaC, runbook, release
- `templates/integrations/`: API spec, mapping sheet
- `templates/legal/`: Legal compliance
- `templates/observability/`: Logging/metrics, cost management
- `templates/operations/`: Change management, incident, capacity
- `templates/project/`: Kickoff, status, retrospective, risk, RACI
- `templates/qa/`: Test plan, QA checklist, contract tests
- `templates/requirements/`: BRD, user stories, acceptance criteria
- `templates/security/`: Security assessment, threat model, ACL, secrets

#### Prompts
- `prompts/templates_analise.md`: Templates de análise
- `prompts/templates_extracao.md`: Templates de extração
- `prompts/templates_geracao.md`: Templates de geração
- `prompts/templates_decisao.md`: Templates de decisão

#### Evals
- `evals/golden_sets.json`: Casos de teste para regressão
- `evals/rubricas.json`: Rubricas de avaliação

#### Observabilidade
- `observability/dashboards.json`: Definição de métricas
- `observability/relatorios_periodicos.md`: Template de relatórios

#### Integrações
- `integrations/inventario_sistemas.json`: Inventário de sistemas
- `integrations/mapeamentos_schemas.json`: Mapeamentos entre sistemas
- `integrations/specs_endpoints.md`: Especificações de endpoints

#### Documentação
- `docs/padrões/padroes_projeto.md`: Padrões obrigatórios
- `docs/padrões/versionamento.md`: Política de versionamento
- `docs/seguranca/politicas.md`: Políticas de segurança e compliance
- `docs/brief/brief_atual.md`: Template de brief
- `docs/dados/data_contracts.md`: Template de contratos de dados
- `docs/modelos/guia_modelos.md`: Guia de seleção de modelos
- `docs/decisoes/adr/ADR-YYYYMMDD-template.md`: Template de ADR

#### DevOps
- `devops/pipelines.yaml`: Pipeline CI/CD base
- `devops/runbooks.md`: Procedimentos operacionais

#### Governança
- `agents/specialists/README.md`: Protocolo de criação de specialists
- Gate de aprovação CTO para stage/prod
- Política anti-estimativas não instrumentadas

### Security
- Política de nunca versionar segredos
- Controles LGPD documentados
- Checklist de segurança por fase (dev/stage/prod)
- Guardrails anti-alucinação para prompts

---

## Convenções

- **Added**: Novos recursos
- **Changed**: Alterações em recursos existentes
- **Deprecated**: Recursos que serão removidos em breve
- **Removed**: Recursos removidos
- **Fixed**: Correções de bugs
- **Security**: Correções de vulnerabilidades

---

## Links

- [Repositório](https://github.com/empresa/tech-agentes)
- [Documentação](./docs/)
- [Issues](https://github.com/empresa/tech-agentes/issues)
