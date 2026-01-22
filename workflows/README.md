# Workflows

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém os workflows de execução e backlog para o framework tech-agentes. Os workflows definem como os agentes coordenam tarefas, quais gates devem ser passados, e como erros são tratados.

---

## Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| [`plano_execucao.json`](plano_execucao.json) | Plano de execução com tarefas, triggers, gates e error handling |
| [`backlog_tarefas.json`](backlog_tarefas.json) | Backlog priorizado de tarefas pendentes |

---

## Estrutura do Plano de Execução

### Metadados Globais

```json
{
  "version": "1.0.0",
  "environment": "dev|stage|prod",
  "metadata": {
    "owner": "CTO",
    "description": "..."
  },
  "global_config": {
    "max_retries": 3,
    "timeout_seconds": 300,
    "notification_channel": "slack:tech-alerts"
  }
}
```

### Estrutura de Tarefa

```json
{
  "id": "task-id",
  "assigned_to": "agente_responsavel",
  "goal": "Objetivo da tarefa",
  "acceptance_criteria": ["Critério 1", "Critério 2"],
  "deliverable_format": "md|json|yaml",
  "deadline": "YYYY-MM-DD",

  "trigger": {
    "type": "manual|event|schedule",
    "condition": "Condição para disparo",
    "inputs_required": ["input1", "input2"]
  },

  "error_handling": {
    "on_failure": "notify_and_pause|notify_and_continue|block_pipeline",
    "retry": {
      "enabled": true,
      "max_attempts": 3,
      "backoff": "linear|exponential"
    },
    "fallback": "Ação alternativa se tudo falhar"
  },

  "rollback": {
    "enabled": true,
    "procedure": "Como reverter",
    "auto": false,
    "requires_approval": true
  },

  "gates": [
    {
      "name": "gate_name",
      "condition": "expressão booleana",
      "blocking": true,
      "message": "Mensagem se bloqueado"
    }
  ],

  "dependencies": ["task-id-1", "task-id-2"]
}
```

---

## Fluxo de Execução

```
┌─────────────────────────────────────────────────────────────────┐
│                         WORKFLOW FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    │
│   │ Trigger │───▶│ Execute │───▶│  Gates  │───▶│Complete │    │
│   └─────────┘    └────┬────┘    └────┬────┘    └─────────┘    │
│                       │              │                         │
│                       ▼              ▼                         │
│                  ┌─────────┐    ┌─────────┐                   │
│                  │  Error  │    │ Blocked │                   │
│                  │ Handler │    │  Notify │                   │
│                  └────┬────┘    └─────────┘                   │
│                       │                                        │
│              ┌────────┴────────┐                              │
│              ▼                 ▼                              │
│         ┌─────────┐      ┌─────────┐                         │
│         │  Retry  │      │Rollback │                         │
│         └─────────┘      └─────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tipos de Trigger

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `manual` | Iniciado por humano | Início de projeto |
| `event` | Disparado por evento/conclusão de tarefa | `task-x.completed` |
| `schedule` | Agendado (cron) | `0 9 * * 1` (segundas 9h) |

### Condições de Evento

```
# Tarefa concluída
task-id.completed

# Múltiplas condições
context-brief.completed AND security-assessment.completed

# Evento de sistema
integration_added OR data_model_changed
```

---

## Error Handling

### Estratégias de Falha

| Estratégia | Comportamento |
|------------|---------------|
| `notify_and_pause` | Notifica e aguarda intervenção |
| `notify_and_continue` | Notifica e continua pipeline |
| `block_pipeline` | Para todo o pipeline |

### Retry com Backoff

```json
{
  "retry": {
    "enabled": true,
    "max_attempts": 3,
    "backoff": "exponential",
    "initial_delay_seconds": 30
  }
}
```

- **linear**: delay fixo entre tentativas
- **exponential**: delay dobra a cada tentativa (30s, 60s, 120s)

---

## Gates e Promoção

### Gates por Ambiente

| Ambiente | Gates Obrigatórios |
|----------|-------------------|
| Dev | Nenhum |
| Stage | `all_tests_pass`, `coverage_threshold`, `no_critical_findings` |
| Prod | Todos acima + `instrumentation_configured`, `golden_sets_pass`, aprovação CTO |

### Regras de Promoção

```json
{
  "promotion_rules": {
    "dev_to_stage": {
      "approval_required": false,
      "auto_promote": true
    },
    "stage_to_prod": {
      "approval_required": true,
      "approvers": ["cto", "qa_lead"],
      "evidence_required": ["evals/resultados/"]
    }
  }
}
```

---

## Rollback

### Quando Aplicar Rollback

1. **Deploy falhou**: Reverter para versão anterior
2. **Bug crítico detectado**: Reverter mudança específica
3. **Gate falhou pós-deploy**: Reverter e investigar

### Procedimento de Rollback

```bash
# 1. Identificar versão estável
git log --oneline -10

# 2. Reverter (depende do tipo)
# Para código:
git revert <commit>

# Para infra:
terraform apply -target=module.x -var="version=previous"

# Para config:
kubectl rollout undo deployment/x

# 3. Verificar
curl https://api.exemplo.com/health

# 4. Notificar
# Automático via notification_channel
```

---

## Notificações

### Canais Configurados

```json
{
  "notifications": {
    "on_task_start": ["assigned_to"],
    "on_task_complete": ["assigned_to", "orquestrador"],
    "on_task_failure": ["assigned_to", "orquestrador", "cto"],
    "on_gate_blocked": ["cto", "qa_lead"]
  }
}
```

### Formato de Notificação

```
[WORKFLOW] Task "task-id" - STATUS
- Assigned to: agente
- Goal: objetivo
- Details: ...
- Action required: Sim/Não
```

---

## Backlog de Tarefas

O arquivo [`backlog_tarefas.json`](backlog_tarefas.json) mantém tarefas priorizadas que não estão no plano de execução atual.

### Estrutura

```json
{
  "version": "1.0.0",
  "items": [
    {
      "id": "task-id",
      "assigned_to": "agente",
      "goal": "objetivo",
      "acceptance_criteria": ["..."],
      "priority": "high|medium|low",
      "status": "pending|in_progress|blocked"
    }
  ]
}
```

### Priorização

- **High**: Bloqueia outros trabalhos ou é crítico para negócio
- **Medium**: Importante mas não urgente
- **Low**: Nice-to-have

---

## Integrando com Orquestrador

O agente `orquestrador` lê e atualiza estes arquivos:

1. **Leitura**: `plano_execucao.json` para saber próximas tarefas
2. **Delegação**: Atribui tarefas aos agentes via `assigned_to`
3. **Monitoramento**: Verifica gates e dependências
4. **Atualização**: Registra status e move para backlog se necessário

### Plano/Resposta Padrão

Output do orquestrador inclui:

- `tasks`: Tarefas delegadas
- `recommendations`: Sugestões para melhorias
- `file_ops`: Operações de arquivo necessárias

---

## Validação

O repositório não inclui CLI de validação automática:

```bash
# Validar estrutura
# Revisar JSON e comparar com o schema descrito neste documento

# Erros comuns:
# - Dependência circular
# - Gate referenciando campo inexistente
# - Trigger inválido
```

---

## Referências

- [Agente Orquestrador](../agents/orquestrador.md)
- Schemas de workflow são mantidos no repositório da ferramenta `tech-agentes`
- [Padrões do Projeto](../padrões/padroes_projeto.md)
