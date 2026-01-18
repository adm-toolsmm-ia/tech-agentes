# Observabilidade

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém as configurações de observabilidade: métricas, dashboards, alertas e relatórios.

---

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| [`dashboards.json`](dashboards.json) | Configuração de métricas e dashboards |
| [`alertas.json`](alertas.json) | Configuração de alertas |
| [`relatorios_periodicos.md`](relatorios_periodicos.md) | Templates de relatórios |

---

## Pilares

### Métricas (dashboards.json)

- **LLM**: requests, latência, tokens, custos, erros
- **Agentes**: tarefas, duração, sucesso
- **Gates**: status de workflows
- **Evals**: pass rate de golden sets

### Alertas (alertas.json)

- **Critical**: Error rate > 5%, budget excedido, instrumentação off
- **Warning**: Latência alta, gates bloqueados, budget em 80%

### Relatórios

- **Semanal**: Resumo de métricas para Tech Leads
- **Mensal**: Custos detalhados para Finance
- **Incidente**: Post-mortem quando aplicável

---

## Política de Observabilidade

### Regra Fundamental

> **NÃO registrar estimativas não instrumentadas**

Se não houver instrumentação ativa:
- Campos de tokens/latência/custo devem ser `null`
- Promoção para stage/prod é **bloqueada**
- Requer aprovação explícita do CTO para exceções

### Campos Obrigatórios em Logs

```json
{
  "timestamp": "ISO8601",
  "run_id": "UUID",
  "tenant_id": "string",
  "environment": "dev|stage|prod"
}
```

---

## Provedores Suportados

| Provedor | Métricas | Logs | Traces |
|----------|----------|------|--------|
| Datadog | ✅ | ✅ | ✅ |
| Grafana + Prometheus | ✅ | ❌ | ❌ |
| Langfuse | ✅ | ✅ | ✅ |
| Helicone | ✅ | ✅ | ❌ |
| CloudWatch | ✅ | ✅ | ✅ |

Configurar em `configs/projeto.json`:
```json
{
  "instrumentation": {
    "provider": "langfuse",
    "enabled": true
  }
}
```

---

## Referências

- [Plano de Logging](../templates/observability/01_logging_metrics_plan.md)
- [Gestão de Custos](../templates/observability/02_cost_management_plan.md)
- [Políticas de Segurança](../docs/seguranca/politicas.md) (o que não logar)
