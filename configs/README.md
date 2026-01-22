# Configurações

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém as configurações do projeto validadas por schemas Pydantic.

---

## Arquivos

| Arquivo | Descrição | Schema |
|---------|-----------|--------|
| [`projeto.json`](projeto.json) | Configuração geral do projeto | `ProjectConfig` |
| [`modelos.json`](modelos.json) | Política de modelos LLM | `ModelPolicy` |
| [`ambientes.json`](ambientes.json) | Referências de secrets por ambiente | `EnvironmentsConfig` |

---

## projeto.json

Configuração principal do projeto:

```json
{
  "name": "nome-do-projeto",
  "version": "0.1.0",
  "owners": ["CTO"],
  "environment": "dev|stage|prod",
  "tenant_id": "",
  "deadlines": {},
  "kpis": [],
  "acceptance_criteria": [],
  "constraints": [],
  "budgets": {
    "run_usd": 0,
    "daily_usd": 0,
    "project_usd": 0
  },
  "slo": {
    "latency_s": 8,
    "critical_error_rate_max": 0.01,
    "daily_budget_usd": 0
  },
  "instrumentation": {
    "provider": "none|langfuse|helicone|datadog",
    "enabled": false,
    "notes": ""
  }
}
```

**Regras**:
- `environment` em `stage/prod` requer `instrumentation.enabled = true`
- `budgets` devem ser definidos antes de produção

---

## modelos.json

Política de roteamento de modelos:

```json
{
  "version": "1.0.0",
  "pricing_version": "2026-01",
  "thresholds": {
    "latency_s_p95_max": 8,
    "daily_budget_usd_max": 100
  },
  "defaults": {
    "architecture": { "temperature": 0.2, "top_p": 0.9 },
    "extraction": { "temperature": 0.1, "top_p": 1.0 },
    "controlled_generation": { "temperature": 0.5, "top_p": 0.95 }
  },
  "routing": [
    {
      "task_class": "architecture|compliance|context_long",
      "preferred": ["gpt-5.2-codex", "opus-4.5", "sonnet-4.5"],
      "fallback": ["gpt-4o", "gpt-4o-mini"],
      "max_temperature": 0.3
    }
  ]
}
```

**Regras**:
- `pricing_version` deve ser atualizado quando preços mudarem
- Fallbacks devem ser definidos para resiliência

---

## ambientes.json

Referências de secrets por ambiente:

```json
{
  "dev": {
    "refs": {
      "OPENAI_API_KEY": "env:OPENAI_API_KEY",
      "DATABASE_URL": "env:DATABASE_URL"
    }
  },
  "stage": {
    "refs": {
      "OPENAI_API_KEY": "vault:secret/stage/openai",
      "DATABASE_URL": "vault:secret/stage/db"
    }
  },
  "prod": {
    "refs": {
      "OPENAI_API_KEY": "vault:secret/prod/openai",
      "DATABASE_URL": "vault:secret/prod/db"
    }
  }
}
```

**Regras**:
- NUNCA commitar valores reais de secrets
- Apenas referências (prefixos: `env:`, `vault:`, `aws:`, `gcp:`, `azure:`)

---

## Validação

Os arquivos devem ser validados manualmente:

```bash
# Validar configs
# Revisar JSON e comparar com os requisitos deste documento

# Erros comuns:
# - Campo obrigatório faltando
# - Tipo de dado incorreto
# - Valor fora do range permitido
# - Instrumentation disabled em stage/prod
```

---

## Schemas

Os schemas de configuração são mantidos no repositório da ferramenta `tech-agentes`.

---

## Referências

- [Políticas de Segurança](../docs/seguranca/politicas.md)
- [Padrões do Projeto](../docs/padrões/padroes_projeto.md)
