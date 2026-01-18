# Especificações de Endpoints e Integrações

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este documento define os padrões e contratos para integrações de API no framework tech-agentes. Todas as integrações devem seguir estas especificações.

---

## 1. Padrões Globais

### 1.1 Autenticação

| Método | Uso | Configuração |
|--------|-----|--------------|
| API Key | APIs simples | Header `X-API-Key` ou query param |
| OAuth 2.0 | APIs com escopos | Bearer token + refresh |
| JWT | Serviços internos | Header `Authorization: Bearer` |
| mTLS | Alta segurança | Certificados client/server |

**Regra**: Credenciais NUNCA em código. Usar refs em `configs/ambientes.json`.

### 1.2 Formato de Dados

- **Request/Response**: JSON (UTF-8)
- **Datas**: ISO 8601 (`2026-01-18T10:30:00Z`)
- **IDs**: UUID v4 ou string alfanumérica
- **Valores monetários**: Inteiros em centavos ou decimais com 2 casas

### 1.3 Versionamento de API

```
# URL-based (preferido)
https://api.exemplo.com/v1/recursos

# Header-based (alternativa)
Accept: application/vnd.exemplo.v1+json
```

### 1.4 Padrões de Retry

```python
# Exponential backoff com jitter
import random
import time

def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except RetryableError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

### 1.5 Circuit Breaker

```yaml
circuit_breaker:
  failure_threshold: 5      # Falhas para abrir
  success_threshold: 2      # Sucessos para fechar
  timeout_seconds: 30       # Tempo em estado aberto
  half_open_requests: 1     # Requests em half-open
```

### 1.6 Rate Limiting

| Cenário | Limite Padrão | Ação quando excedido |
|---------|---------------|---------------------|
| Por segundo | 10 req/s | Retry com backoff |
| Por minuto | 100 req/min | Queue local |
| Por hora | 1000 req/h | Alertar + circuit break |

---

## 2. Especificação por Sistema

### 2.1 Template de Especificação

```yaml
# integrations/specs/[sistema].yaml

metadata:
  name: "Nome do Sistema"
  version: "1.0.0"
  owner: "Time responsável"
  criticality: "high|medium|low"
  documentation: "URL da documentação oficial"

auth:
  method: "api_key|oauth|jwt|basic"
  config_ref: "configs/ambientes.json → {env}.refs.SISTEMA_AUTH"
  scopes: ["read", "write"]  # se OAuth

endpoints:
  - name: "Nome do Endpoint"
    method: "GET|POST|PUT|PATCH|DELETE"
    path: "/v1/recursos/{id}"
    description: "Descrição do endpoint"

    request:
      headers:
        Content-Type: "application/json"
        X-Request-ID: "{run_id}"
      path_params:
        - name: "id"
          type: "string"
          required: true
      query_params:
        - name: "page"
          type: "integer"
          default: 1
      body_schema:
        type: "object"
        properties:
          field1:
            type: "string"
            required: true
        example:
          field1: "value"

    response:
      success:
        status: 200
        schema:
          type: "object"
          properties:
            id:
              type: "string"
            data:
              type: "object"
        example:
          id: "uuid-123"
          data: {}

      errors:
        - status: 400
          code: "INVALID_REQUEST"
          description: "Request malformado"
        - status: 401
          code: "UNAUTHORIZED"
          description: "Credenciais inválidas"
        - status: 404
          code: "NOT_FOUND"
          description: "Recurso não encontrado"
        - status: 429
          code: "RATE_LIMITED"
          description: "Limite de requests excedido"
        - status: 500
          code: "INTERNAL_ERROR"
          description: "Erro interno do servidor"

    retry:
      enabled: true
      max_attempts: 3
      retryable_statuses: [429, 500, 502, 503, 504]
      backoff: "exponential"

    idempotency:
      enabled: true  # Para POST/PUT
      key_header: "Idempotency-Key"

    timeout_seconds: 30

    logging:
      log_request: true
      log_response: true
      mask_fields: ["password", "token", "api_key"]

health_check:
  endpoint: "/health"
  expected_status: 200
  interval_seconds: 60
  timeout_seconds: 5

dependencies:
  - name: "Outro Sistema"
    criticality: "high"

notes: |
  Observações importantes sobre a integração.
```

---

## 3. Integrações de LLM

### 3.1 OpenAI

```yaml
metadata:
  name: "OpenAI API"
  version: "2024-01"
  documentation: "https://platform.openai.com/docs/api-reference"

auth:
  method: "api_key"
  config_ref: "configs/ambientes.json → {env}.refs.OPENAI_API_KEY"
  header: "Authorization: Bearer {key}"

endpoints:
  - name: "Chat Completions"
    method: "POST"
    path: "/v1/chat/completions"

    request:
      body_schema:
        model:
          type: "string"
          required: true
          enum: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]
        messages:
          type: "array"
          required: true
        temperature:
          type: "number"
          default: 0.7
          min: 0
          max: 2
        max_tokens:
          type: "integer"
        response_format:
          type: "object"

    response:
      success:
        status: 200
        schema:
          id: "string"
          choices: "array"
          usage:
            prompt_tokens: "integer"
            completion_tokens: "integer"
            total_tokens: "integer"

    retry:
      enabled: true
      max_attempts: 3
      retryable_statuses: [429, 500, 502, 503]
      backoff: "exponential"
      rate_limit_header: "x-ratelimit-remaining-requests"

    timeout_seconds: 120

    logging:
      log_request: true
      log_response: true
      mask_fields: []
      # NÃO logar conteúdo de mensagens se contiver PII
```

### 3.2 Anthropic (Claude)

```yaml
metadata:
  name: "Anthropic API"
  version: "2024-01"
  documentation: "https://docs.anthropic.com/en/api"

auth:
  method: "api_key"
  config_ref: "configs/ambientes.json → {env}.refs.ANTHROPIC_API_KEY"
  header: "x-api-key: {key}"

endpoints:
  - name: "Messages"
    method: "POST"
    path: "/v1/messages"

    request:
      headers:
        anthropic-version: "2024-01-01"
      body_schema:
        model:
          type: "string"
          required: true
          enum: ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
        messages:
          type: "array"
          required: true
        max_tokens:
          type: "integer"
          required: true
        temperature:
          type: "number"
          default: 1.0

    response:
      success:
        status: 200
        schema:
          id: "string"
          content: "array"
          usage:
            input_tokens: "integer"
            output_tokens: "integer"
```

---

## 4. Logging de Integrações

### 4.1 Formato de Log

```json
{
  "timestamp": "2026-01-18T10:30:00.123Z",
  "level": "INFO",
  "event": "integration_request",
  "run_id": "uuid-xxx",
  "tenant_id": "tenant-123",
  "integration": {
    "name": "openai",
    "endpoint": "/v1/chat/completions",
    "method": "POST"
  },
  "request": {
    "model": "gpt-4o"
  },
  "response": {
    "status": 200,
    "latency_ms": 1234,
    "tokens_used": 678
  },
  "error": null
}
```

> **Nota**: O campo `tokens_used` em `response` reflete o valor **real** retornado pela API, não uma estimativa. Nunca registre estimativas não instrumentadas conforme política em `observability/README.md`.

### 4.2 O que NÃO logar

- Conteúdo de mensagens com PII
- API keys ou tokens
- Dados sensíveis do usuário

---

## 5. Tratamento de Erros

### 5.1 Classificação de Erros

| Código | Classe | Retry | Ação |
|--------|--------|-------|------|
| 400 | Client Error | Não | Logar e falhar |
| 401 | Auth Error | Não | Renovar token e retry 1x |
| 403 | Forbidden | Não | Logar e escalar |
| 404 | Not Found | Não | Depende do contexto |
| 429 | Rate Limit | Sim | Backoff exponencial |
| 500-504 | Server Error | Sim | Backoff + circuit breaker |

### 5.2 Fallback

```python
class IntegrationClient:
    def call_with_fallback(self, request):
        try:
            return self.primary_provider.call(request)
        except (RateLimitError, ServiceUnavailable) as e:
            logger.warning(f"Primary failed: {e}, trying fallback")
            return self.fallback_provider.call(request)
```

---

## 6. Contratos de API (OpenAPI)

### 6.1 Localização

Para cada integração, manter arquivo OpenAPI em:
```
integrations/openapi/[sistema].yaml
```

### 6.2 Validação

```bash
# Validar spec OpenAPI
npx @redocly/cli lint integrations/openapi/*.yaml

# Gerar client (opcional)
openapi-generator-cli generate \
  -i integrations/openapi/sistema.yaml \
  -g python \
  -o src/clients/sistema/
```

---

## 7. Checklist de Nova Integração

- [ ] Spec criada em `integrations/specs/[sistema].yaml`
- [ ] Credenciais em `configs/ambientes.json` (apenas refs)
- [ ] Adicionado em `integrations/inventario_sistemas.json`
- [ ] Mapeamento de dados em `integrations/mapeamentos_schemas.json`
- [ ] Retry e circuit breaker configurados
- [ ] Logging implementado (sem PII)
- [ ] Testes de contrato criados
- [ ] Health check configurado
- [ ] Documentação em `integrations/README.md`

---

## Referências

- [Inventário de Sistemas](inventario_sistemas.json)
- [Mapeamentos de Schema](mapeamentos_schemas.json)
- [Template de Integração](../templates/integrations/01_api_integration_spec.md)
- [Políticas de Segurança](../docs/seguranca/politicas.md)
