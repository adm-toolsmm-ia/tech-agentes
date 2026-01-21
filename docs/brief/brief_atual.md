# Brief do Projeto

> **Portal Tech Arauz** — Sistema de Gestão de TI, Inovação e Projetos
> **Versão**: 1.0.0 | **Última atualização**: 2026-01-18

---

## 1. Identificação

| Campo | Valor |
|-------|-------|
| **Nome do Projeto** | Portal Tech Arauz |
| **Código/ID** | TECH-ARAUZ-MVP |
| **Tenant** | arauz (single-tenant inicial) |
| **Owner** | CTO |
| **Stakeholders** | CTO, Equipe de TI, Gestores de Área |
| **Data de Início** | 2026-01-18 |
| **Deadline** | Sem prazo definido (priorização por valor) |

---

## 2. Contexto e Problema

### 2.1 Situação Atual
O escritório de advocacia utiliza o ERP **Espaider** como sistema central, mas a gestão de demandas de TI, inovação e projetos internos carece de uma interface dedicada. Atualmente:
- Solicitações são registradas no Espaider, mas sem visibilidade consolidada para a equipe de TI.
- Não há dashboards para acompanhamento de métricas e KPIs de atendimento.
- Documentação técnica e procedimentos estão dispersos.
- Falta controle granular de acesso e auditoria de operações.

### 2.2 Problema a Resolver
Centralizar a gestão de demandas de TI em uma plataforma moderna, integrada ao Espaider, com dashboards analíticos, gestão de documentação e controle de acesso adequado.

### 2.3 Impacto do Problema

| Métrica | Valor Atual | Meta |
|---------|-------------|------|
| Tempo médio para visualizar demandas abertas | Manual (consulta ERP) | < 5 segundos (dashboard) |
| Visibilidade de backlog para gestão | Baixa | Alta (dashboards em tempo real) |
| Documentação técnica centralizada | Dispersa | 100% no portal |

---

## 3. Objetivos e Escopo

### 3.1 Objetivo Principal
Entregar um portal web moderno para gestão de demandas de TI, sincronizado com o ERP Espaider, com dashboards analíticos, gestão de documentação e controle de acesso por perfil.

### 3.2 Objetivos Secundários
- [x] Sincronização automática de solicitações do Espaider
- [x] Dashboards com KPIs de atendimento (geral, gestão, tecnologia)
- [x] Visão Kanban e Lista para gestão de tickets
- [x] Gestão de documentação técnica interna
- [x] Controle de acesso por roles (admin, user, viewer)

### 3.3 Escopo Incluído (MVP)

| Módulo | Funcionalidades |
|--------|-----------------|
| **Dashboards** | Dashboard Geral, Gestão, Tecnologia; KPIs; Gráficos de evolução |
| **Solicitações** | Kanban, Lista, Filtros, Detalhes, Entregas, Cronogramas, Requisitos |
| **Tarefas de Sincronização** | Configuração, execução manual, agendamento |
| **Documentações** | CRUD, categorização, editor Markdown, visualizações |
| **Logs** | Histórico de execuções, detalhes técnicos (admin), sanitização para users |
| **APIs** | Configuração de integrações (admin only) |
| **Automações** | Gestão de jobs de sincronização (admin only) |
| **Tabelas Auxiliares** | Status, Tipos, Prioridades, Categorias, Áreas, Etapas Kanban |

### 3.4 Escopo Excluído (Out of Scope)
- Integração com sistemas além do Espaider (fase futura)
- App mobile nativo
- Módulo financeiro/faturamento
- Multi-tenancy (fase futura)

---

## 4. Requisitos

### 4.1 Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|------------|-------------------|
| RF01 | Autenticação com Supabase Auth | Must | Login/logout funcionando, sessão persistida |
| RF02 | Dashboard com KPIs de solicitações | Must | Exibir total abertos, em atendimento, resolvidos, aguardando |
| RF03 | Visão Kanban de solicitações | Must | Colunas por status, drag-and-drop, filtros |
| RF04 | Visão Lista de solicitações | Must | Tabela com ordenação, busca, filtros |
| RF05 | Detalhes de solicitação com entregas, cronogramas, requisitos | Must | Sheet lateral com abas |
| RF06 | CRUD de documentações com editor Markdown | Should | Criar, editar, visualizar, excluir docs |
| RF07 | Logs de execução com detalhes expansíveis | Should | Tabela com linhas expansíveis, sanitização por role |
| RF08 | Configuração de APIs (admin) | Must | CRUD de integrações, token mascarado |
| RF09 | Gestão de automações (admin) | Should | Ativar/desativar, executar manualmente |
| RF10 | Tabelas auxiliares configuráveis | Could | CRUD de status, tipos, prioridades, etc. |

### 4.2 Requisitos Não-Funcionais

| ID | Requisito | Métrica | Target |
|----|-----------|---------|--------|
| RNF01 | Performance | Latência P95 dashboard | < 2s |
| RNF02 | Disponibilidade | Uptime | 99% (ambiente dev/stage) |
| RNF03 | Segurança | RLS ativo em todas tabelas | 100% |
| RNF04 | Segurança | Tokens/segredos nunca expostos em logs | 100% |
| RNF05 | UX | Responsividade | Mobile-first, breakpoints sm/md/lg |

### 4.3 Restrições

| Tipo | Restrição | Impacto |
|------|-----------|---------|
| Técnica | Stack: React + TypeScript + Vite + Tailwind + Shadcn/ui | Manutenção simplificada |
| Técnica | Backend: Supabase (Auth, Database, RLS) | Custo previsível, serverless |
| Técnica | Origem de dados: Sincronização com Espaider (API) | Dependência de disponibilidade |

---

## 5. KPIs e Métricas de Sucesso

### 5.1 KPIs Principais

| KPI | Baseline | Meta | Prazo |
|-----|----------|------|-------|
| Solicitações visíveis no dashboard | 0 | 100% sync | MVP |
| Documentações criadas | 0 | 10+ | MVP + 30 dias |
| Usuários ativos | 0 | Equipe TI (5+) | MVP |

### 5.2 Critérios de Aceite do Projeto

```markdown
## Critérios de Aceite (Definition of Done)

- [x] Todos os requisitos "Must" implementados
- [ ] Testes passando (cobertura mínima: 70%)
- [ ] Documentação atualizada
- [ ] Code review aprovado
- [ ] Deploy em staging validado
- [ ] Aprovação do CTO
```

---

## 6. Dados e Integrações

### 6.1 Fontes de Dados

| Sistema | Tipo | Dados | Frequência | Owner |
|---------|------|-------|------------|-------|
| Espaider | API REST | Solicitações, entregas, cronogramas, requisitos | Diária/Manual | TI |
| Supabase | Database | Dados locais, documentações, logs | Real-time | Sistema |

### 6.2 Integrações Necessárias

| Sistema | Direção | Protocolo | Status |
|---------|---------|-----------|--------|
| Espaider | IN | REST API | Em uso (protótipo) |

### 6.3 Classificação de Dados

| Dado | Classificação | Controles Necessários |
|------|---------------|----------------------|
| Email/Nome de usuários | PII | RLS, acesso por profile |
| Tokens de API | Sensível | Armazenamento seguro, mascaramento em views |
| Logs de execução | Interno | Sanitização para não-admins |

---

## 7. Arquitetura e Tecnologia

### 7.1 Stack Tecnológico

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Frontend | React 18 + TypeScript + Vite | Performance, DX, ecossistema |
| UI | Tailwind CSS + Shadcn/ui + Radix | Consistência, acessibilidade |
| State | TanStack Query (React Query) | Cache, sync, devtools |
| Backend | Supabase (PostgreSQL + Auth + RLS) | Serverless, custo previsível |
| Charts | Recharts | Integração React, customização |
| Forms | React Hook Form + Zod | Validação tipada |

### 7.2 Decisões Arquiteturais

- **ADR-001**: Uso de Supabase RLS para controle de acesso — Aprovado
- **ADR-002**: Mascaramento de tokens via view `apis_safe` — Aprovado
- **ADR-003**: Sanitização de logs por role — Aprovado

---

## 8. Riscos e Dependências

### 8.1 Riscos Identificados

| ID | Risco | Probabilidade | Impacto | Mitigação |
|----|-------|---------------|---------|-----------|
| R01 | Indisponibilidade da API Espaider | Média | Alto | Cache local, retry com backoff |
| R02 | Escopo creep durante desenvolvimento | Alta | Médio | Priorização rígida, backlog fechado |
| R03 | Falta de testes automatizados | Alta | Médio | Implementar testes progressivamente |

### 8.2 Dependências

| Dependência | Tipo | Status | Responsável |
|-------------|------|--------|-------------|
| API Espaider | Externa | Disponível | TI |
| Supabase project | Técnica | Configurado | CTO |

---

## 9. Cronograma e Milestones

### 9.1 Fases do Projeto

| Fase | Início | Fim | Entregáveis |
|------|--------|-----|-------------|
| Discovery | 2026-01-18 | 2026-01-18 | Brief aprovado, backlog inicial |
| MVP | 2026-01-19 | A definir | Funcionalidades core refatoradas |
| Beta | A definir | A definir | Versão testada com equipe |
| Go-Live | A definir | A definir | Produção |

### 9.2 Milestones Críticos

- [x] **M0** 2026-01-18: Protótipo Lovable concluído (referência)
- [x] **M1** 2026-01-18: Brief e backlog do projeto oficial aprovados
- [x] **M1.5** 2026-01-18: Phase 1 (Foundation) e Phase 2 (Core Features) concluídas
- [ ] **M2**: MVP funcional em staging (Phase 3-5 em andamento)
- [ ] **M3**: Go-live para equipe de TI

### 9.3 Status das Fases

| Fase | Status | Data Conclusão |
|------|--------|----------------|
| Phase 1: Foundation | Concluída | 2026-01-18 |
| Phase 2: Core Features | Concluída | 2026-01-18 |
| Phase 3: Database & Types | Concluída | 2026-01-19 |
| Phase 4: Migração de Páginas | Concluída | 2026-01-19 |
| Phase 5: Edge Functions | Concluída | 2026-01-19 |
| Phase 5.1: pg_cron Config | Concluída | 2026-01-19 |
| Phase 5.2: QA & Polish | Concluída | 2026-01-20 |
| Phase 6: Launch | Pendente | - |

### 9.4 Entregáveis Concluídos (2026-01-19)

- ADR-002: Arquitetura de Sincronização Espaider
- Migration: `tarefas_sincronizacao`, `logs_execucao`, campos Espaider
- View sanitizada: `logs_execucao_safe`
- Types e Hooks para todas as features
- Componentes reutilizáveis: DataTable, FormDialog, StatusBadge, ErrorState, EmptyState, LoadingState
- 7 páginas migradas de mock data para Supabase:
  - Dashboard Gestão
  - Dashboard Tecnologia
  - Tarefas de Sincronização
  - Logs de Execução
  - Documentações
  - Automações
  - Tabelas Auxiliares
- Edge Functions:
  - `sync-solicitacoes` - Sincronização com retry e circuit breaker
  - `test-api-connection` - Teste de conexão com APIs
- pg_cron configurado para agendamentos automáticos
- Sistema multi-agente configurado na raiz do projeto

---

## 10. Time e Responsabilidades

| Papel | Nome | Responsabilidades |
|-------|------|-------------------|
| Product Owner / CTO | Gabriel Cristofolini | Priorização, aceite, decisões técnicas |
| Tech Lead | AI Assistant (tech-agentes) | Arquitetura, implementação, QA |
| DevOps | AI Assistant (tech-agentes) | CI/CD, infra, observabilidade |

---

## 11. Perguntas Abertas

| ID | Pergunta | Responsável | Prazo | Status |
|----|----------|-------------|-------|--------|
| Q01 | Definir frequência ideal de sincronização com Espaider | CTO | - | Aberta |
| Q02 | Mapear campos adicionais do Espaider para sincronização | CTO | - | Aberta |
| Q03 | Definir política de retenção de logs | CTO | - | Aberta |

---

## 12. Anexos e Referências

- Protótipo Lovable: Repositório atual (`src/`)
- Migrações Supabase: `supabase/migrations/`
- Padrões tech-agentes: `docs/`

---

## Histórico de Atualizações

| Data | Autor | Mudança |
|------|-------|---------|
| 2026-01-19 | AI Assistant (Eng. Software) | Conclusão da migração v2: Edge Functions, pg_cron, todas páginas sem mock data |
| 2026-01-18 | AI Assistant (Orquestrador) | Criação inicial baseada no protótipo |
