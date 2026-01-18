# Integrações

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém as especificações e contratos de integrações externas para o framework tech-agentes.

---

## Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| [`inventario_sistemas.json`](inventario_sistemas.json) | Inventário de sistemas integrados |
| [`mapeamentos_schemas.json`](mapeamentos_schemas.json) | Mapeamento de dados entre sistemas |
| [`specs_endpoints.md`](specs_endpoints.md) | Especificações de endpoints e padrões |

---

## Inventário de Sistemas

O arquivo `inventario_sistemas.json` mantém um registro de todos os sistemas externos integrados:

```json
{
  "systems": [
    {
      "name": "nome-sistema",
      "category": "llm|crm|erp|database|api",
      "owner": "responsável",
      "criticality": "high|medium|low",
      "auth": {
        "type": "api_key|oauth|jwt",
        "notes": "Ref em configs/ambientes.json"
      },
      "data_sensitivity": {
        "contains_pii": false,
        "notes": ""
      }
    }
  ]
}
```

---

## Adicionando Nova Integração

### 1. Adicionar ao Inventário

```json
// inventario_sistemas.json
{
  "name": "novo-sistema",
  "category": "api",
  "owner": "time-x",
  "criticality": "medium",
  "auth": {
    "type": "api_key",
    "notes": "NOVO_SISTEMA_API_KEY em configs/ambientes.json"
  },
  "data_sensitivity": {
    "contains_pii": false,
    "notes": ""
  },
  "endpoints_doc": "integrations/specs/novo-sistema.yaml"
}
```

### 2. Configurar Credenciais

```json
// configs/ambientes.json
{
  "dev": {
    "refs": {
      "NOVO_SISTEMA_API_KEY": "env:NOVO_SISTEMA_API_KEY"
    }
  },
  "stage": {
    "refs": {
      "NOVO_SISTEMA_API_KEY": "vault:secret/stage/novo-sistema"
    }
  }
}
```

### 3. Criar Especificação

Seguir template em [`specs_endpoints.md`](specs_endpoints.md) ou criar arquivo YAML/OpenAPI em `integrations/specs/`.

### 4. Definir Mapeamentos (se ETL)

```json
// mapeamentos_schemas.json
{
  "mappings": [
    {
      "source": {
        "system": "novo-sistema",
        "entity": "Contact",
        "field": "email"
      },
      "target": {
        "system": "interno",
        "entity": "users",
        "field": "email"
      },
      "transform": "lowercase(trim(value))"
    }
  ]
}
```

### 5. Testes de Contrato

Criar testes em `tests/integration/test_novo_sistema.py`:

```python
import pytest
from tech_agents.integrations import NovoSistemaClient

class TestNovoSistemaIntegration:
    def test_health_check(self, client: NovoSistemaClient):
        assert client.health_check().status == 200

    def test_endpoint_contract(self, client: NovoSistemaClient):
        response = client.get_resource("123")
        assert "id" in response
        assert "data" in response
```

---

## Padrões Obrigatórios

### Autenticação

- **NUNCA** commitar credenciais
- Usar refs em `configs/ambientes.json`
- Rotacionar credenciais a cada 90 dias (prod)

### Retry e Resiliência

```python
# Padrão mínimo
retry_config = {
    "max_attempts": 3,
    "backoff": "exponential",
    "retryable_statuses": [429, 500, 502, 503, 504]
}
```

### Logging

```python
# Campos obrigatórios
log_fields = {
    "run_id": run_id,
    "tenant_id": tenant_id,
    "integration": system_name,
    "endpoint": endpoint,
    "method": method,
    "status": response.status,
    "latency_ms": latency
}
# NÃO logar: api_keys, tokens, PII
```

### Timeouts

| Tipo | Padrão | Máximo |
|------|--------|--------|
| Connect | 5s | 10s |
| Read | 30s | 120s |
| Total | 60s | 180s |

---

## Referências

- [Políticas de Segurança](../docs/seguranca/politicas.md)
- [Template de Integração](../templates/integrations/01_api_integration_spec.md)
- [Plano de Logging](../templates/observability/01_logging_metrics_plan.md)
