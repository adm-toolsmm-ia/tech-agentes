# Agentes

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém as definições dos agentes base do framework tech-agentes. Cada agente tem um mandato específico, entradas/saídas definidas, e regras de operação.

---

## Agentes Base

| Agente | Mandato | Arquivo |
|--------|---------|---------|
| **Orquestrador** | Planejar, priorizar e supervisionar execução | [`orquestrador.md`](orquestrador.md) |
| **Contexto & Requisitos** | Capturar e manter contexto do projeto | [`contexto_requisitos.md`](contexto_requisitos.md) |
| **Engenharia de Prompt** | Converter objetivos em prompts versionados | [`engenharia_prompt.md`](engenharia_prompt.md) |
| **Segurança & Compliance** | Proteger dados e garantir conformidade | [`seguranca_compliance.md`](seguranca_compliance.md) |
| **QA/Evals** | Garantir qualidade e regressão | [`qualidade_auditoria_testes.md`](qualidade_auditoria_testes.md) |
| **Observabilidade & Custos** | Monitorar métricas e budgets | [`observabilidade_custos.md`](observabilidade_custos.md) |
| **Eng. Software/Arquiteto/DevOps** | Arquitetura, CI/CD, operação | [`eng_software_arquiteto_ia_devops.md`](eng_software_arquiteto_ia_devops.md) |

---

## Estrutura de Definição de Agente

Cada agente é definido com:

```markdown
# Agente: [Nome]

## Mandato
O que o agente é responsável por fazer.

## Entradas
- Quais arquivos/dados o agente consome
- De quais outros agentes recebe informação

## Saídas (obrigatórias)
- Quais arquivos/artefatos o agente produz
- Formato esperado das saídas

## Regras
- Restrições e políticas que o agente deve seguir
- Gates e aprovações necessárias

## Handoffs
- Para quais agentes passa informação
- O que é passado em cada handoff
```

---

## Fluxo de Coordenação

```
                    ┌─────────────────┐
                    │   Orquestrador  │
                    │    (coordena)   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    Contexto     │ │   Segurança     │ │  Observabilidade│
│   Requisitos    │ │   Compliance    │ │     Custos      │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         │         ┌─────────┴─────────┐         │
         │         │                   │         │
         ▼         ▼                   ▼         ▼
┌─────────────────┐               ┌─────────────────┐
│   Engenharia    │               │  QA/Auditoria   │
│    Prompt       │               │    Testes       │
└────────┬────────┘               └────────┬────────┘
         │                                 │
         └────────────────┬────────────────┘
                          ▼
                ┌─────────────────┐
                │  Eng. Software  │
                │ Arquiteto/DevOps│
                └─────────────────┘
```

---

## Specialists

O diretório [`specialists/`](specialists/) contém agentes especializados criados para necessidades específicas de projetos.

**Regras para Specialists**:
- Máximo de 2 specialists por iteração (salvo aprovação CTO)
- ROI deve ser justificado antes da criação
- Devem seguir o template de definição de agente
- Não podem conflitar com agentes base

---

## Criando/Estendendo Agentes

### Criar Specialist

1. Justificar ROI em `workflows/backlog_tarefas.json`
2. Obter aprovação (se necessário)
3. Criar arquivo em `agents/specialists/[nome].md`
4. Seguir template de agente
5. Documentar handoffs com agentes existentes

### Modificar Agente Base

1. Criar ADR documentando mudança
2. Obter aprovação do CTO
3. Atualizar arquivo do agente
4. Atualizar este README se necessário
5. Comunicar mudança à equipe

---

## Referências

- [Workflows](../workflows/)
- [Templates de Prompts](../prompts/)
- [Padrões do Projeto](../docs/padrões/padroes_projeto.md)
