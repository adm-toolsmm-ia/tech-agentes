# Template: Plano de Logging e Métricas

> **Versão**: 1.0.0
> **Categoria**: Observabilidade
> **Uso**: Definir estratégia de logging, métricas e tracing para o projeto

---

## Metadados

| Campo | Valor |
|-------|-------|
| **Projeto** | [Nome do Projeto] |
| **Data** | [YYYY-MM-DD] |
| **Responsável** | [Nome] |
| **Stack de Observabilidade** | [Datadog/Grafana/ELK/etc] |

---

## 1. Visão Geral

### 1.1 Objetivos

| Objetivo | Descrição |
|----------|-----------|
| **Debugging** | Identificar e diagnosticar problemas rapidamente |
| **Monitoramento** | Acompanhar saúde e performance do sistema |
| **Alerting** | Detectar anomalias antes que impactem usuários |
| **Analytics** | Entender comportamento e tendências |
| **Compliance** | Auditoria e rastreabilidade |

### 1.2 Pilares da Observabilidade

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILIDADE                          │
├───────────────────┬───────────────────┬───────────────────┤
│      LOGS         │     METRICS       │     TRACES        │
│                   │                   │                   │
│ • Eventos         │ • Counters        │ • Request flow    │
│ • Erros           │ • Gauges          │ • Latência        │
│ • Contexto        │ • Histograms      │ • Dependências    │
│ • Debugging       │ • Aggregations    │ • Bottlenecks     │
└───────────────────┴───────────────────┴───────────────────┘
```

---

## 2. Logging

### 2.1 Padrão de Log (Estruturado JSON)

```json
{
  "timestamp": "2026-01-18T10:30:00.123Z",
  "level": "INFO",
  "service": "api-gateway",
  "version": "1.2.3",
  "environment": "production",
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "tenant-123",
  "trace_id": "abc123def456",
  "span_id": "xyz789",
  "user_id": "user-456",
  "event": "http_request",
  "message": "Request completed",
  "data": {
    "method": "POST",
    "path": "/api/orders",
    "status": 201,
    "latency_ms": 145,
    "request_size": 1024,
    "response_size": 512
  },
  "error": null
}
```

### 2.2 Campos Obrigatórios

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `timestamp` | ISO8601 | Momento do evento | `2026-01-18T10:30:00.123Z` |
| `level` | string | Severidade | `DEBUG/INFO/WARN/ERROR/FATAL` |
| `service` | string | Nome do serviço | `api-gateway` |
| `environment` | string | Ambiente | `dev/stage/prod` |
| `run_id` | UUID | Correlação de execução | UUID v4 |
| `event` | string | Tipo do evento | `http_request` |
| `message` | string | Descrição legível | `Request completed` |

### 2.3 Campos Condicionais

| Campo | Quando Usar | Descrição |
|-------|-------------|-----------|
| `tenant_id` | Multi-tenant | Identificador do tenant |
| `user_id` | Autenticado | ID do usuário (nunca PII) |
| `trace_id` | Distributed tracing | ID de trace |
| `error` | Em erros | Detalhes do erro |
| `data` | Contexto adicional | Dados específicos do evento |

### 2.4 Níveis de Log

| Nível | Quando Usar | Retenção |
|-------|-------------|----------|
| `DEBUG` | Desenvolvimento, troubleshooting detalhado | 7 dias (dev only) |
| `INFO` | Eventos operacionais normais | 30 dias |
| `WARN` | Situações anômalas não críticas | 90 dias |
| `ERROR` | Erros que afetam funcionalidade | 1 ano |
| `FATAL` | Sistema não pode continuar | 2 anos |

### 2.5 O Que NÃO Logar (Compliance)

```python
# ❌ NUNCA logar:
- Senhas (mesmo hashes)
- Tokens de acesso
- Números de cartão de crédito
- CPF/RG completos
- Dados de saúde
- Conteúdo de mensagens privadas

# ✅ Mascaramento quando necessário:
email: "j***@example.com"
cpf: "***.***.789-00"
card: "****-****-****-1234"
```

### 2.6 Implementação Python

```python
import structlog
import logging
from datetime import datetime
from uuid import uuid4

# Configuração
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# Uso
logger = structlog.get_logger()

def process_request(request):
    log = logger.bind(
        run_id=str(uuid4()),
        tenant_id=request.tenant_id,
        user_id=request.user_id,
    )

    log.info("request_started", path=request.path, method=request.method)

    try:
        result = do_work(request)
        log.info("request_completed", status=200, latency_ms=result.latency)
        return result
    except Exception as e:
        log.error("request_failed",
                  error=str(e),
                  error_type=type(e).__name__,
                  status=500)
        raise
```

---

## 3. Métricas

### 3.1 Tipos de Métricas

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| **Counter** | Valor cumulativo | `http_requests_total` |
| **Gauge** | Valor instantâneo | `active_connections` |
| **Histogram** | Distribuição de valores | `http_request_duration_seconds` |
| **Summary** | Percentis pré-calculados | `request_latency_p99` |

### 3.2 Métricas Obrigatórias

#### RED (Request-oriented)

| Métrica | Tipo | Labels | SLO |
|---------|------|--------|-----|
| `http_requests_total` | Counter | method, path, status | - |
| `http_request_duration_seconds` | Histogram | method, path | P95 < 500ms |
| `http_request_errors_total` | Counter | method, path, error_type | < 1% |

#### USE (Resource-oriented)

| Métrica | Tipo | Labels | Threshold |
|---------|------|--------|-----------|
| `cpu_usage_percent` | Gauge | instance | < 80% |
| `memory_usage_bytes` | Gauge | instance | < 85% |
| `disk_usage_percent` | Gauge | instance, mount | < 70% |
| `network_io_bytes` | Counter | instance, direction | - |

#### Negócio

| Métrica | Tipo | Labels | Descrição |
|---------|------|--------|-----------|
| `orders_created_total` | Counter | tenant, status | Pedidos criados |
| `order_value_dollars` | Histogram | tenant | Valor dos pedidos |
| `active_users` | Gauge | tenant | Usuários ativos |

### 3.3 Naming Convention

```
# Formato: {namespace}_{subsystem}_{name}_{unit}

# Exemplos:
api_http_requests_total
api_http_request_duration_seconds
db_query_duration_seconds
cache_hit_ratio
queue_messages_pending
```

### 3.4 Labels/Tags

```python
# ✅ Boas práticas:
- Cardinalidade baixa (< 100 valores únicos)
- Útil para agregação/filtragem
- Estável ao longo do tempo

# Labels recomendadas:
- service
- environment
- method (GET, POST, etc.)
- status (2xx, 4xx, 5xx)
- tenant_id (se multi-tenant)

# ❌ Evitar:
- user_id (alta cardinalidade)
- request_id (cardinalidade infinita)
- timestamps em labels
```

### 3.5 Implementação Python (Prometheus)

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Definição de métricas
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'path', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'path'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

ACTIVE_REQUESTS = Gauge(
    'http_active_requests',
    'Active HTTP requests',
    ['method']
)

# Uso
@REQUEST_LATENCY.labels(method='GET', path='/api/users').time()
def get_users():
    REQUEST_COUNT.labels(method='GET', path='/api/users', status='200').inc()
    return users

# Expor métricas
start_http_server(9090)  # /metrics endpoint
```

---

## 4. Tracing Distribuído

### 4.1 Conceitos

| Conceito | Descrição |
|----------|-----------|
| **Trace** | Jornada completa de uma requisição |
| **Span** | Unidade de trabalho dentro de um trace |
| **Context** | Informações propagadas entre serviços |

### 4.2 Propagação de Contexto

```
┌─────────────────────────────────────────────────────────────┐
│ Trace ID: abc123                                            │
│                                                             │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│ │ Span: API   │───▶│ Span: Auth  │───▶│ Span: DB    │      │
│ │ ID: span-1  │    │ ID: span-2  │    │ ID: span-3  │      │
│ │ 0-100ms     │    │ 20-40ms     │    │ 50-80ms     │      │
│ └─────────────┘    └─────────────┘    └─────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Headers de Propagação

```http
# W3C Trace Context (recomendado)
traceparent: 00-abc123def456...-span123-01
tracestate: vendor=value

# Ou B3 (Zipkin)
X-B3-TraceId: abc123def456...
X-B3-SpanId: span123
X-B3-ParentSpanId: parent456
```

### 4.4 Implementação Python (OpenTelemetry)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configuração
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://collector:4317")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Uso
@tracer.start_as_current_span("process_order")
def process_order(order_id):
    span = trace.get_current_span()
    span.set_attribute("order.id", order_id)

    with tracer.start_as_current_span("validate_order"):
        validate(order_id)

    with tracer.start_as_current_span("save_to_db"):
        save(order_id)
```

---

## 5. Alertas

### 5.1 Estratégia de Alertas

| Severidade | Tempo de Resposta | Notificação | Exemplo |
|------------|-------------------|-------------|---------|
| **P1 Critical** | < 5 min | PagerDuty + SMS | Serviço down |
| **P2 High** | < 15 min | Slack + Email | Error rate > 5% |
| **P3 Medium** | < 1 hora | Slack | Latência degradada |
| **P4 Low** | < 24 horas | Email | Disk > 70% |

### 5.2 Alertas Recomendados

| Alerta | Condição | Severidade |
|--------|----------|------------|
| ServiceDown | health_check != 200 for 2m | P1 |
| HighErrorRate | error_rate > 5% for 5m | P1 |
| HighLatency | p95_latency > 1s for 5m | P2 |
| DiskSpaceLow | disk_usage > 85% | P2 |
| MemoryHigh | memory_usage > 90% for 5m | P2 |
| CertExpiring | cert_expiry < 7 days | P3 |

### 5.3 Exemplo de Alerta (Prometheus/Alertmanager)

```yaml
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook_url: "https://runbooks.exemplo.com/high-error-rate"
```

---

## 6. Dashboards

### 6.1 Dashboard Overview

| Painel | Métricas | Propósito |
|--------|----------|-----------|
| Request Rate | `rate(http_requests_total[5m])` | Throughput |
| Error Rate | `rate(http_errors_total[5m])` | Saúde |
| Latency P95 | `histogram_quantile(0.95, ...)` | Performance |
| Active Users | `active_users` | Negócio |

### 6.2 Dashboard por Serviço

```
┌─────────────────────────────────────────────────────────────┐
│ Service: API Gateway                          [Last 1h]     │
├───────────────────────────────┬─────────────────────────────┤
│ Request Rate     │ 1.2k/s    │ Error Rate      │ 0.3%      │
│ ████████████████ │           │ ██              │           │
├───────────────────────────────┼─────────────────────────────┤
│ Latency P50      │ 45ms      │ Latency P99     │ 320ms     │
│ ██████           │           │ ████████████    │           │
├───────────────────────────────┴─────────────────────────────┤
│ [Graph: Request Rate over Time]                             │
│ [Graph: Latency Distribution]                               │
│ [Graph: Error Rate by Endpoint]                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Retenção e Custos

### 7.1 Política de Retenção

| Tipo | Dev | Stage | Prod |
|------|-----|-------|------|
| Logs DEBUG | 3 dias | Não coleta | Não coleta |
| Logs INFO+ | 7 dias | 30 dias | 90 dias |
| Logs ERROR+ | 30 dias | 90 dias | 1 ano |
| Métricas | 7 dias | 30 dias | 2 anos |
| Traces | 7 dias | 14 dias | 30 dias |

### 7.2 Estimativa de Custos

| Item | Volume/mês | Custo Estimado |
|------|------------|----------------|
| Logs | X GB | $Y |
| Métricas | X séries | $Y |
| Traces | X spans | $Y |
| **Total** | | **$Z** |

### 7.3 Otimização de Custos

- [ ] Sampling de traces (ex: 10% em prod)
- [ ] Agregação de logs antes de envio
- [ ] Drop de métricas de baixo valor
- [ ] Compressão habilitada
- [ ] Retenção adequada por ambiente

---

## 8. Implementação

### 8.1 Checklist de Implementação

- [ ] Logging estruturado configurado
- [ ] Métricas RED implementadas
- [ ] Tracing distribuído habilitado
- [ ] Alertas críticos configurados
- [ ] Dashboard principal criado
- [ ] Documentação de runbook linkada
- [ ] Política de retenção definida
- [ ] Custos estimados e aprovados

### 8.2 Stack Recomendada

| Componente | Opção 1 | Opção 2 |
|------------|---------|---------|
| Logs | Datadog | ELK Stack |
| Métricas | Datadog | Prometheus + Grafana |
| Traces | Datadog | Jaeger |
| Alertas | Datadog | Alertmanager + PagerDuty |

---

## Anexo: Comandos Úteis

```bash
# Verificar logs localmente
docker logs -f api --since 5m | jq .

# Testar métricas
curl http://localhost:9090/metrics | grep http_request

# Debug de traces
curl http://localhost:16686/api/traces?service=api
```
