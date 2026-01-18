# Relatórios Periódicos

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este documento define os templates e processos para relatórios periódicos de observabilidade do framework tech-agentes.

---

## 1. Relatório Semanal

### Frequência
- **Quando**: Toda segunda-feira às 9h
- **Destinatários**: CTO, Tech Leads
- **Formato**: Markdown + gráficos

### Template

```markdown
# Relatório Semanal - Tech-Agentes
**Período**: [DATA_INICIO] a [DATA_FIM]
**Gerado em**: [TIMESTAMP]

## Resumo Executivo

| Métrica | Valor | Variação | Status |
|---------|-------|----------|--------|
| Total de Requests | X | +Y% | 🟢/🟡/🔴 |
| Custo Total | $X | +Y% | 🟢/🟡/🔴 |
| Latência P95 | Xms | +Y% | 🟢/🟡/🔴 |
| Error Rate | X% | +Y% | 🟢/🟡/🔴 |
| Uptime | X% | - | 🟢/🟡/🔴 |

## SLOs

| SLO | Target | Atual | Status |
|-----|--------|-------|--------|
| Latência P95 < 8s | 99.9% | X% | ✅/❌ |
| Error Rate < 1% | 99.9% | X% | ✅/❌ |
| Budget Diário | $X | $Y avg | ✅/❌ |

## Performance por Modelo

| Modelo | Requests | Tokens | Custo | Latência P50 | Latência P95 |
|--------|----------|--------|-------|--------------|--------------|
| gpt-4o | X | X | $X | Xms | Xms |
| claude-sonnet | X | X | $X | Xms | Xms |

## Performance por Agente

| Agente | Tarefas | Sucesso | Duração Média |
|--------|---------|---------|---------------|
| orquestrador | X | X% | Xs |
| engenharia_prompt | X | X% | Xs |

## Incidentes

| Data | Severidade | Descrição | Resolução | Duração |
|------|------------|-----------|-----------|---------|
| [DATA] | P1/P2/P3 | [DESC] | [RESOLUÇÃO] | Xmin |

## Alertas Disparados

| Alerta | Vezes | Ação Tomada |
|--------|-------|-------------|
| HighErrorRate | X | [AÇÃO] |
| HighLatency | X | [AÇÃO] |

## Quality Gates

| Gate | Passou | Falhou | Taxa |
|------|--------|--------|------|
| all_tests_pass | X | X | X% |
| golden_sets_pass | X | X | X% |

## Tendências

[GRÁFICO: Requests ao longo da semana]
[GRÁFICO: Custo ao longo da semana]
[GRÁFICO: Latência ao longo da semana]

## Recomendações

1. [Recomendação baseada nos dados]
2. [Recomendação baseada nos dados]

## Próximas Ações

- [ ] [Ação 1]
- [ ] [Ação 2]
```

---

## 2. Relatório Mensal de Custos

### Frequência
- **Quando**: Primeiro dia útil do mês às 9h
- **Destinatários**: CTO, Finance
- **Formato**: Markdown + Excel

### Template

```markdown
# Relatório Mensal de Custos - Tech-Agentes
**Período**: [MÊS/ANO]
**Gerado em**: [TIMESTAMP]

## Resumo de Custos

| Categoria | Planejado | Realizado | Variação |
|-----------|-----------|-----------|----------|
| LLM APIs | $X | $Y | +Z% |
| Infraestrutura | $X | $Y | +Z% |
| Observabilidade | $X | $Y | +Z% |
| **Total** | **$X** | **$Y** | **+Z%** |

## Custo por Modelo

| Modelo | Tokens (M) | Custo | % do Total | Variação MoM |
|--------|------------|-------|------------|--------------|
| gpt-4o | X | $Y | Z% | +W% |
| claude-sonnet | X | $Y | Z% | +W% |
| gpt-mini | X | $Y | Z% | +W% |

## Custo por Tenant (se multi-tenant)

| Tenant | Requests | Custo | % do Total |
|--------|----------|-------|------------|
| tenant-1 | X | $Y | Z% |
| tenant-2 | X | $Y | Z% |

## Custo por Tipo de Tarefa

| Tipo | Requests | Custo | Custo Médio |
|------|----------|-------|-------------|
| extraction | X | $Y | $Z |
| generation | X | $Y | $Z |
| analysis | X | $Y | $Z |

## Tendência de Custos

[GRÁFICO: Custo diário ao longo do mês]
[GRÁFICO: Custo por modelo ao longo do mês]

## Análise de Eficiência

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Custo por request | $X | $Y | ✅/❌ |
| Custo por token (avg) | $X | $Y | ✅/❌ |
| Cache hit rate | X% | Y% | ✅/❌ |

## Otimizações Implementadas

| Otimização | Economia Estimada | Status |
|------------|-------------------|--------|
| [Descrição] | $X/mês | ✅ Implementado |

## Recomendações de Otimização

1. **[Recomendação]**: Economia estimada de $X/mês
2. **[Recomendação]**: Economia estimada de $X/mês

## Previsão Próximo Mês

| Cenário | Custo Estimado |
|---------|----------------|
| Conservador | $X |
| Base | $Y |
| Agressivo | $Z |

## Anexos

- [ ] Planilha detalhada (Excel)
- [ ] Dashboard interativo (link)
```

---

## 3. Relatório de Incidente (Post-Mortem)

### Quando Gerar
- Após qualquer incidente P1 ou P2
- Dentro de 5 dias úteis após resolução

### Template

```markdown
# Post-Mortem: [TÍTULO DO INCIDENTE]
**ID**: INC-[NUMERO]
**Data**: [DATA]
**Severidade**: P1/P2
**Duração**: [DURAÇÃO]
**Autor**: [NOME]

## Resumo Executivo

[1-2 parágrafos resumindo o incidente, impacto e resolução]

## Timeline

| Hora | Evento |
|------|--------|
| HH:MM | Alerta disparado |
| HH:MM | Investigação iniciada |
| HH:MM | Causa identificada |
| HH:MM | Mitigação aplicada |
| HH:MM | Serviço restaurado |
| HH:MM | Incidente encerrado |

## Impacto

| Métrica | Valor |
|---------|-------|
| Usuários afetados | X |
| Requests com erro | X |
| Duração do impacto | X min |
| Custo estimado | $X |

## Causa Raiz

[Descrição detalhada da causa raiz]

### 5 Whys

1. Por que [sintoma]? Porque [causa 1]
2. Por que [causa 1]? Porque [causa 2]
3. Por que [causa 2]? Porque [causa 3]
4. Por que [causa 3]? Porque [causa 4]
5. Por que [causa 4]? Porque [causa raiz]

## O que funcionou bem

- [Item 1]
- [Item 2]

## O que poderia melhorar

- [Item 1]
- [Item 2]

## Ações Corretivas

| Ação | Responsável | Prazo | Status |
|------|-------------|-------|--------|
| [Ação 1] | [Nome] | [Data] | ⏳/✅ |
| [Ação 2] | [Nome] | [Data] | ⏳/✅ |

## Lições Aprendidas

1. [Lição 1]
2. [Lição 2]

## Aprovações

| Papel | Nome | Data |
|-------|------|------|
| Autor | [Nome] | [Data] |
| Tech Lead | [Nome] | [Data] |
| CTO | [Nome] | [Data] |
```

---

## 4. Geração Automática

### Script de Geração

```python
# scripts/generate_report.py

from datetime import datetime, timedelta
from tech_agents.observability import MetricsClient

def generate_weekly_report(start_date: datetime, end_date: datetime) -> str:
    """Gera relatório semanal."""
    client = MetricsClient()

    metrics = {
        "total_requests": client.query("sum(llm_request_total)", start_date, end_date),
        "total_cost": client.query("sum(llm_cost_usd)", start_date, end_date),
        "latency_p95": client.query("histogram_quantile(0.95, llm_request_duration_seconds)", start_date, end_date),
        "error_rate": client.query("sum(llm_error_total) / sum(llm_request_total)", start_date, end_date),
    }

    # Gerar markdown usando template
    template = load_template("weekly_report.md.j2")
    return template.render(metrics=metrics, start_date=start_date, end_date=end_date)
```

### Agendamento

```yaml
# .github/workflows/reports.yml
name: Generate Reports

on:
  schedule:
    - cron: '0 9 * * 1'  # Segunda às 9h (semanal)
    - cron: '0 9 1 * *'  # Dia 1 às 9h (mensal)

jobs:
  weekly:
    if: github.event.schedule == '0 9 * * 1'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate Weekly Report
        run: python scripts/generate_report.py weekly
      - name: Send to Slack
        run: python scripts/send_report.py weekly

  monthly:
    if: github.event.schedule == '0 9 1 * *'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate Monthly Report
        run: python scripts/generate_report.py monthly
      - name: Send to Email
        run: python scripts/send_report.py monthly
```

---

## 5. Armazenamento

### Onde Salvar

| Tipo | Local | Retenção |
|------|-------|----------|
| Semanal | `observability/reports/weekly/YYYY-WW.md` | 1 ano |
| Mensal | `observability/reports/monthly/YYYY-MM.md` | 3 anos |
| Incidente | `observability/reports/incidents/INC-XXX.md` | Permanente |

### Estrutura de Diretórios

```
observability/
├── reports/
│   ├── weekly/
│   │   ├── 2026-01.md
│   │   ├── 2026-02.md
│   │   └── ...
│   ├── monthly/
│   │   ├── 2026-01.md
│   │   └── ...
│   └── incidents/
│       ├── INC-001.md
│       └── ...
└── ...
```

---

## Referências

- [Dashboards](dashboards.json)
- [Alertas](alertas.json)
- [Template de Logging](../templates/observability/01_logging_metrics_plan.md)
