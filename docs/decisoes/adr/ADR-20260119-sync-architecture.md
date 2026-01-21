# ADR-002: Arquitetura de Sincronização com Espaider

> **Status**: Aprovado
> **Data**: 2026-01-19
> **Autor**: Agente Eng. Software / Arquiteto IA & DevOps
> **Aprovador**: CTO

---

## Contexto

O Portal Tech Arauz precisa sincronizar dados de solicitações, entregas, cronogramas e requisitos do ERP Espaider. A sincronização deve ser:

- **Confiável**: Dados sempre atualizados, sem perda
- **Resiliente**: Tolerante a falhas da API externa
- **Auditável**: Logs completos de cada execução
- **Segura**: Tokens nunca expostos, sanitização de erros

### Requisitos do Brief

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-SYNC-01 | Sincronização automática diária | Must |
| RF-SYNC-02 | Sincronização manual sob demanda | Must |
| RF-SYNC-03 | Logs de execução com detalhes | Should |
| RF-SYNC-04 | Retry automático em falhas | Must |
| RF-SYNC-05 | Circuit breaker para proteção | Should |

---

## Decisão

Implementar arquitetura de sincronização usando **Supabase Edge Functions** com políticas de resiliência (retry + circuit breaker) e agendamento via **pg_cron**.

### Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Tarefas    │  │    Logs      │  │  Dashboard   │              │
│  │    Page      │  │    Page      │  │  Tecnologia  │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                       │
│         └────────────────┬┴─────────────────┘                       │
│                          │                                          │
│                   React Query Hooks                                 │
└──────────────────────────┼──────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────────┐
│                    SUPABASE                                         │
│                          │                                          │
│  ┌───────────────────────▼───────────────────────────┐             │
│  │              Edge Functions                        │             │
│  │  ┌─────────────────┐  ┌─────────────────┐         │             │
│  │  │ sync-solicit.   │  │ test-connection │         │             │
│  │  │ - Retry logic   │  │ - Health check  │         │             │
│  │  │ - Circuit break │  │                 │         │             │
│  │  └────────┬────────┘  └─────────────────┘         │             │
│  └───────────┼───────────────────────────────────────┘             │
│              │                                                      │
│  ┌───────────▼───────────┐  ┌────────────────────────┐             │
│  │   PostgreSQL          │  │       pg_cron          │             │
│  │  ┌─────────────────┐  │  │  ┌──────────────────┐  │             │
│  │  │ solicitacoes    │  │  │  │ sync-diaria      │  │             │
│  │  │ tarefas_sync    │  │  │  │ 08:00 daily      │  │             │
│  │  │ logs_execucao   │  │  │  └──────────────────┘  │             │
│  │  └─────────────────┘  │  └────────────────────────┘             │
│  └───────────────────────┘                                          │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API ESPAIDER                                   │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │  GET /api/solicitacoes                                         ││
│  │  GET /api/solicitacoes/{id}/entregas                           ││
│  │  GET /api/solicitacoes/{id}/cronogramas                        ││
│  └────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## Componentes

### 1. Tabelas de Suporte

#### tarefas_sincronizacao

Armazena configuração dos jobs de sincronização.

```sql
CREATE TABLE tarefas_sincronizacao (
  id UUID PRIMARY KEY,
  nome TEXT NOT NULL,
  descricao TEXT,
  tipo TEXT DEFAULT 'espaider',
  endpoint TEXT,
  frequencia TEXT CHECK (frequencia IN ('manual', 'diaria', 'semanal', 'mensal')),
  horario TIME,
  dias_semana INTEGER[],
  dia_mes INTEGER,
  ativo BOOLEAN DEFAULT true,
  config JSONB DEFAULT '{}',
  ultima_execucao TIMESTAMPTZ,
  proxima_execucao TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

#### logs_execucao

Histórico completo de cada execução.

```sql
CREATE TABLE logs_execucao (
  id UUID PRIMARY KEY,
  tarefa_id UUID REFERENCES tarefas_sincronizacao(id),
  status TEXT CHECK (status IN ('executando', 'sucesso', 'erro', 'cancelado')),
  registros_processados INTEGER DEFAULT 0,
  registros_novos INTEGER DEFAULT 0,
  registros_atualizados INTEGER DEFAULT 0,
  registros_erros INTEGER DEFAULT 0,
  mensagem_erro TEXT,
  detalhes JSONB,
  duracao_ms INTEGER,
  iniciado_em TIMESTAMPTZ NOT NULL,
  finalizado_em TIMESTAMPTZ
);
```

### 2. Edge Function: sync-solicitacoes

Responsável por executar a sincronização com resiliência.

```typescript
// supabase/functions/sync-solicitacoes/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const RETRY_CONFIG = {
  maxRetries: 3,
  baseDelay: 1000,
  maxDelay: 10000,
};

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  // 1. Criar log de execução
  const { data: log } = await supabase
    .from('logs_execucao')
    .insert({ status: 'executando', iniciado_em: new Date() })
    .select()
    .single();

  try {
    // 2. Buscar configuração da API
    const { data: api } = await supabase
      .from('apis')
      .select('url, token')
      .eq('tipo', 'espaider')
      .eq('status', 'ativo')
      .single();

    if (!api) throw new Error('API Espaider não configurada');

    // 3. Fetch com retry
    const data = await fetchWithRetry(
      `${api.url}/solicitacoes`,
      { headers: { Authorization: `Bearer ${api.token}` } }
    );

    // 4. Upsert dados
    const { count } = await supabase
      .from('solicitacoes')
      .upsert(data.map(mapEspaiderToLocal), {
        onConflict: 'id_espaider',
      });

    // 5. Atualizar log
    await supabase
      .from('logs_execucao')
      .update({
        status: 'sucesso',
        registros_processados: data.length,
        finalizado_em: new Date(),
        duracao_ms: Date.now() - log.iniciado_em,
      })
      .eq('id', log.id);

    return new Response(JSON.stringify({ success: true, count }));

  } catch (error) {
    await supabase
      .from('logs_execucao')
      .update({
        status: 'erro',
        mensagem_erro: error.message,
        detalhes: { stack_trace: error.stack },
        finalizado_em: new Date(),
      })
      .eq('id', log.id);

    return new Response(JSON.stringify({ error: error.message }), { status: 500 });
  }
});
```

### 3. Políticas de Resiliência

#### Retry com Backoff Exponencial

```typescript
async function fetchWithRetry(url: string, options: RequestInit) {
  let lastError: Error;

  for (let attempt = 0; attempt < RETRY_CONFIG.maxRetries; attempt++) {
    try {
      const response = await fetch(url, {
        ...options,
        signal: AbortSignal.timeout(30000),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      lastError = error;
      console.log(`Attempt ${attempt + 1} failed: ${error.message}`);

      if (attempt < RETRY_CONFIG.maxRetries - 1) {
        const delay = Math.min(
          RETRY_CONFIG.baseDelay * Math.pow(2, attempt),
          RETRY_CONFIG.maxDelay
        );
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }

  throw lastError;
}
```

#### Circuit Breaker (Simplificado)

Para MVP, usamos um circuit breaker baseado em estado no banco:

```sql
-- Verificar se circuit está aberto (5+ falhas consecutivas)
CREATE OR REPLACE FUNCTION is_circuit_open(p_tarefa_id UUID)
RETURNS BOOLEAN AS $$
  SELECT COUNT(*) >= 5
  FROM (
    SELECT status
    FROM logs_execucao
    WHERE tarefa_id = p_tarefa_id
    ORDER BY iniciado_em DESC
    LIMIT 5
  ) recent
  WHERE status = 'erro';
$$ LANGUAGE sql;
```

### 4. Agendamento com pg_cron

```sql
-- Requer Supabase Pro ou self-hosted
CREATE EXTENSION IF NOT EXISTS pg_cron;
CREATE EXTENSION IF NOT EXISTS pg_net;

-- Agendar sync diária às 08:00
SELECT cron.schedule(
  'sync-diaria-espaider',
  '0 8 * * *',
  $$
  SELECT net.http_post(
    url := current_setting('app.supabase_url') || '/functions/v1/sync-solicitacoes',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || current_setting('app.service_role_key'),
      'Content-Type', 'application/json'
    ),
    body := jsonb_build_object('source', 'cron', 'tarefa_id', NULL)
  )
  $$
);
```

---

## Justificativa

### Por que Edge Functions?

| Alternativa | Prós | Contras |
|-------------|------|---------|
| Edge Functions | Serverless, integrado, logs | Limitado a 150s |
| External Worker | Sem limites de tempo | Complexidade, custo |
| pg_cron direto | Simples | Sem retry, sem logs |

**Decisão**: Edge Functions cobrem 99% dos casos. Para syncs longas, usar paginação.

### Por que pg_cron?

- Nativo do PostgreSQL
- Gerenciado pelo Supabase (Pro)
- Sem infraestrutura adicional
- Confiável e auditável

### Por que Retry + Circuit Breaker?

- **Retry**: APIs externas falham temporariamente (rede, timeout)
- **Circuit Breaker**: Evita sobrecarga quando API está offline prolongado
- **Exponential Backoff**: Reduz pressão em momentos de instabilidade

---

## Consequências

### Positivas

- Sincronização confiável e resiliente
- Logs completos para troubleshooting
- Execução manual e automática
- Proteção contra falhas em cascata

### Negativas

- Requer Supabase Pro para pg_cron
- Limite de 150s por execução de Edge Function
- Complexidade adicional vs fetch simples

### Mitigações

- Paginação para grandes volumes
- Fallback para sync manual se cron falhar
- Alertas via Slack/Email em falhas críticas

---

## Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| API Espaider offline | Média | Alto | Circuit breaker + alertas |
| Timeout em syncs grandes | Baixa | Médio | Paginação de 100 registros |
| Token expirado | Baixa | Alto | Teste de conexão antes de sync |
| Dados corrompidos | Muito Baixa | Alto | Validação Zod antes de upsert |

---

## Monitoramento

### Métricas a Acompanhar

- Taxa de sucesso de syncs (meta: >95%)
- Tempo médio de sync (meta: <30s)
- Registros sincronizados por dia
- Erros por tipo (timeout, auth, parse)

### Alertas Recomendados

```sql
-- Alerta: 3+ falhas consecutivas
SELECT * FROM logs_execucao
WHERE status = 'erro'
  AND iniciado_em > now() - interval '1 hour'
GROUP BY tarefa_id
HAVING COUNT(*) >= 3;
```

---

## Decisões Relacionadas

- **ADR-001**: Feature-Based Architecture (estrutura de código)
- **ADR-003** (futuro): Estratégia de cache para dados do Espaider

---

## Referências

- [Supabase Edge Functions](https://supabase.com/docs/guides/functions)
- [pg_cron Documentation](https://github.com/citusdata/pg_cron)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Exponential Backoff](https://cloud.google.com/iot/docs/how-tos/exponential-backoff)

---

*ADR criado pelo Agente Eng. Software / Arquiteto em 2026-01-19*
