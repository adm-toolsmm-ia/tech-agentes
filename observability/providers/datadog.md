# Datadog Provider

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

## Objetivo
Configuração mínima para enviar métricas e logs do framework para Datadog.

## Pré-requisitos
- Conta Datadog ativa
- API Key e App Key configuradas em ambiente seguro

## Configuração

1. Definir provider em `configs/projeto.json`:

```json
{
  "instrumentation": {
    "provider": "datadog",
    "enabled": true
  }
}
```

2. Referenciar secrets em `configs/ambientes.json`:

```json
{
  "prod": {
    "refs": {
      "DATADOG_API_KEY": "vault:datadog/api_key",
      "DATADOG_APP_KEY": "vault:datadog/app_key"
    }
  }
}
```

## Checklist
- [ ] API Key registrada
- [ ] Logs com `run_id` e `tenant_id`
- [ ] Métricas de LLM enviadas

