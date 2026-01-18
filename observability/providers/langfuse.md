# Langfuse Provider

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

## Objetivo
Configuração mínima para telemetria LLM com Langfuse.

## Pré-requisitos
- Projeto no Langfuse
- Public key e secret key disponíveis

## Configuração

1. Definir provider em `configs/projeto.json`:

```json
{
  "instrumentation": {
    "provider": "langfuse",
    "enabled": true
  }
}
```

2. Referenciar secrets em `configs/ambientes.json`:

```json
{
  "prod": {
    "refs": {
      "LANGFUSE_PUBLIC_KEY": "vault:langfuse/public_key",
      "LANGFUSE_SECRET_KEY": "vault:langfuse/secret_key",
      "LANGFUSE_HOST": "env:LANGFUSE_HOST"
    }
  }
}
```

## Checklist
- [ ] Chaves configuradas
- [ ] Eventos com `run_id` e `tenant_id`
- [ ] Tokens/latencia/custo instrumentados

