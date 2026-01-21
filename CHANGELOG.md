# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2026-01-20

### Added - Phase 5: QA & Polish

#### Formulários CRUD
- `SolicitacaoForm` - Formulário completo de criação/edição com validação Zod
- `SolicitacaoFormDialog` - Modal responsivo (Sheet em mobile, Dialog em desktop)
- Schema de validação `solicitacaoSchema` com regras de negócio

#### Testes Automatizados
- Setup de testes com Vitest + Testing Library
- 38 testes passando em 5 arquivos de teste
- Cobertura de schemas Zod (validação)
- Cobertura de componentes compartilhados (StatusBadge, EmptyState)
- Cobertura de hooks utilitários (useMediaQuery)

#### CI/CD
- GitHub Actions workflow para CI (lint, test, build)
- Workflow de PR Check com comentário automático
- Deploy staging configurável

#### Observabilidade
- Logger estruturado com sanitização de PII/secrets
- Coletor de métricas (API latency, Web Vitals)
- Run ID para correlação de logs

---

## [1.0.0] - 2026-01-19

### Added - Migração Completa v2

#### ADR e Governança
- ADR-002: Arquitetura de Sincronização com Espaider em `docs/docs/decisoes/adr/ADR-20260119-sync-architecture.md`
- Sistema multi-agente movido para pasta raiz `agents/`
- Arquivo `.cursorrules` consolidado com regras de acionamento
- Workflow de delegação em `agents/workflow.json`

#### Database Layer
- Migration: Tabelas `tarefas_sincronizacao` e `logs_execucao`
- View sanitizada `logs_execucao_safe` (esconde detalhes sensíveis para não-admins)
- Campos Espaider em solicitações: `id_espaider`, `codigo_espaider`, `origem`, `sincronizado_em`
- Função `is_circuit_open()` para circuit breaker

#### Data Access Layer (Types & Hooks)
- Types por feature: `tarefas`, `documentacoes`, `automacoes`, `tabelas-auxiliares`, `logs`, `dashboard`
- Hooks completos para todas as entidades com React Query
- `useTarefas`, `useLogsExecucao` - Gerenciamento de sincronização
- `useDocumentacoes`, `useCategorias` - CRUD de documentações
- `useAutomacoes` - CRUD de automações
- `useTabelaAuxiliar` - Hook genérico para tabelas auxiliares
- `useSLAMetrics`, `useGestaoStats` - Métricas de gestão
- `useTechDashboardStats`, `useIntegrationStatus` - Métricas técnicas

#### Components Layer
- `DataTable` - Tabela com sort/filter reutilizável
- `FormDialog` - Modal CRUD padronizado
- `ConfirmDialog` - Confirmação de ações destrutivas
- `StatusBadge` - Badge com cores dinâmicas
- `LoadingState`, `PageLoading`, `TableSkeleton` - Estados de loading
- `ErrorState`, `QueryState` - Tratamento de erros
- `EmptyState` - Estado vazio com ação

#### Pages Layer (Migração de Mock Data)
- Dashboard de Gestão com métricas SLA reais
- Dashboard de Tecnologia com status de integrações
- Tarefas de Sincronização com execução manual
- Logs de Execução com filtros e detalhes expandíveis
- Documentações com editor e preview
- Automações com CRUD completo
- Tabelas Auxiliares refatorado com hook genérico

#### Edge Functions
- `sync-solicitacoes` - Sincronização com Espaider (retry + circuit breaker)
- `test-api-connection` - Teste de conexão com APIs

#### pg_cron Configuration
- Migration para configuração de jobs agendados
- View `sync_jobs_status` para monitoramento
- Funções `create_sync_job` e `remove_sync_job`
- Tabela `sync_jobs_config` para configuração de agendamentos

### Changed
- Backlog atualizado com status das tarefas concluídas
- Brief atualizado com status das fases

### Removed
- Arquivo `src/data/mockData.ts` removido
- Todas as referências a dados mockados nas páginas

---

### Added - Phase 1: Foundation (2026-01-18)

#### Documentação do Projeto Oficial
- Brief completo do Portal Tech Arauz em `docs/docs/brief/brief_atual.md`
- Backlog do MVP com 20 itens em `workflows/backlog_tarefas.json`
- Plano de execução com 5 fases em `workflows/plano_execucao.json`
- Configuração do projeto em `configs/projeto.json`
- Resumo executivo em `outputs/artefatos_gerados/RESUMO_EXECUTIVO_MVP.md`

#### Security Assessment
- Assessment inicial do protótipo em `docs/docs/seguranca/assessment_mvp.md`
- Validação de RLS em todas as tabelas
- Confirmação de tokens protegidos via view `apis_safe`

#### ADR - Decisões Arquiteturais
- ADR-001: Feature-based architecture em `docs/docs/decisoes/adr/ADR-20260118-feature-based-structure.md`

#### Refatoração do Frontend
- Nova estrutura feature-based: `src/app/`, `src/features/`, `src/shared/`
- Providers centralizados em `src/app/providers.tsx`
- Rotas centralizadas em `src/app/routes.tsx`
- Componentes UI migrados para `src/shared/components/ui/`
- Layout migrado para `src/shared/components/layout/`

#### Hooks com React Query
- `useSolicitacoes` - CRUD completo de solicitações
- `useLookupTables` - Tabelas auxiliares (status, tipos, prioridades, etc.)
- `useDashboardStats` - Estatísticas e gráficos do dashboard
- `useDocumentacoes` - CRUD de documentações

### Changed
- Guias de providers de observabilidade (Datadog, Grafana/Prometheus, Langfuse)
- Exemplo mínimo de OpenAPI em `integrations/openapi/`
- Evidência de execução bloqueada para golden sets em `evals/resultados/`
- Runner de evals com CLI `eval` para validar outputs externos
- Catálogo de templates alinhado aos arquivos reais
- Referências OpenAPI padronizadas para `integrations/openapi/`
- Templates críticos preenchidos com conteúdo mínimo (legal, project, requirements)
- Documentação de resultados de evals ajustada para o MVP atual

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
