# Grafana + Prometheus Provider

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

## Objetivo
Configuração mínima para métricas via Prometheus e dashboards no Grafana.

## Pré-requisitos
- Prometheus configurado para scrape
- Grafana com datasource Prometheus

## Configuração

1. Definir provider em `configs/projeto.json`:

```json
{
  "instrumentation": {
    "provider": "grafana",
    "enabled": true
  }
}
```

2. Expor métricas no endpoint `/metrics` do serviço integrador.

## Checklist
- [ ] Endpoint `/metrics` acessível
- [ ] Dashboards base importados
- [ ] Alertas configurados em `observability/alertas.json`

