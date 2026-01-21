# Tarefas de Sincronização

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-21
> **Agente responsável**: Eng. Software / Arquiteto IA & DevOps

---

## Visão Geral

O módulo de **Tarefas de Sincronização** permite configurar e executar sincronizações periódicas ou manuais com sistemas externos (como o Espaider). Cada tarefa pode ser parametrizada com periodicidade, prioridade e API alvo.

---

## Estrutura de Dados

### Tabela: `tarefas_sincronizacao`

```sql
CREATE TABLE tarefas_sincronizacao (
  id UUID PRIMARY KEY,
  nome TEXT NOT NULL,
  descricao TEXT,
  tipo TEXT NOT NULL, -- espaider, webhook, custom
  endpoint TEXT,
  frequencia TEXT NOT NULL, -- manual, diaria, semanal, mensal
  horario TIME,
  dias_semana INTEGER[],
  dia_mes INTEGER,
  ativo BOOLEAN DEFAULT true,
  config JSONB DEFAULT '{}',
  api_id UUID REFERENCES apis(id), -- Nova: API associada
  cron_schedule TEXT, -- Nova: Expressão cron
  timezone TEXT DEFAULT 'America/Sao_Paulo', -- Nova: Fuso horário
  prioridade INTEGER DEFAULT 5, -- Nova: 1 (alta) a 10 (baixa)
  ultima_execucao TIMESTAMPTZ,
  proxima_execucao TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

---

## Configuração de Tarefa

### Campos Principais

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `nome` | text | Nome identificador | Sim |
| `tipo` | text | Tipo: espaider, webhook, custom | Sim |
| `api_id` | uuid | API Espaider associada (se tipo=espaider) | Sim (se espaider) |
| `frequencia` | text | manual, diaria, semanal, mensal | Sim |
| `cron_schedule` | text | Expressão cron (ex: `0 6 * * *`) | Não (gerado automaticamente) |
| `timezone` | text | Fuso horário | Não (padrão: America/Sao_Paulo) |
| `prioridade` | integer | 1 (alta) a 10 (baixa) | Não (padrão: 5) |
| `ativo` | boolean | Se a tarefa está ativa | Não (padrão: true) |

### Conversão de Frequência para Cron

| Frequência | Cron Gerado | Exemplo |
|------------|-------------|---------|
| `manual` | `null` | - |
| `diaria` | `${minute} ${hour} * * *` | `0 6 * * *` (06:00) |
| `semanal` | `${minute} ${hour} * * 1` | `0 6 * * 1` (Segunda 06:00) |
| `mensal` | `${minute} ${hour} 1 * *` | `0 6 1 * *` (Dia 1, 06:00) |

---

## Execução de Tarefa

### Via UI

1. Acesse `/tarefas`
2. Clique no botão **Executar** (ícone Play) na tarefa desejada
3. A execução será registrada em `logs_execucao`

### Via Edge Function

```typescript
const { data, error } = await supabase.functions.invoke('sync-solicitacoes', {
  body: {
    tarefa_id: 'uuid-da-tarefa',
    api_id: 'uuid-da-api', // Opcional, pode vir da tarefa
  }
});
```

---

## Logs de Execução

### Tabela: `logs_execucao`

Todos os logs são armazenados com informações completas:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | uuid | ID único do log |
| `tarefa_id` | uuid | ID da tarefa executada |
| `status` | text | executando, sucesso, erro, parcial, cancelado |
| `iniciado_em` | timestamptz | Início da execução |
| `finalizado_em` | timestamptz | Fim da execução |
| `duracao_ms` | integer | Duração em milissegundos |
| `registros_processados` | integer | Total de registros processados |
| `registros_novos` | integer | Registros criados |
| `registros_atualizados` | integer | Registros atualizados |
| `registros_erros` | integer | Registros com erro |
| `mensagem_erro` | text | Mensagem de erro (se houver) |
| `detalhes` | jsonb | Metadados extras |

### Consulta de Logs

```sql
-- Últimas execuções de uma tarefa
SELECT 
  status,
  registros_processados,
  registros_novos,
  registros_atualizados,
  registros_erros,
  duracao_ms,
  iniciado_em,
  finalizado_em
FROM logs_execucao
WHERE tarefa_id = 'uuid-da-tarefa'
ORDER BY iniciado_em DESC
LIMIT 10;

-- Taxa de sucesso por tarefa
SELECT 
  t.nome,
  COUNT(*) as total_execucoes,
  COUNT(*) FILTER (WHERE l.status = 'sucesso') as sucessos,
  COUNT(*) FILTER (WHERE l.status = 'erro') as erros,
  ROUND(
    COUNT(*) FILTER (WHERE l.status = 'sucesso')::numeric / COUNT(*) * 100,
    2
  ) as taxa_sucesso_percent
FROM tarefas_sincronizacao t
LEFT JOIN logs_execucao l ON l.tarefa_id = t.id
GROUP BY t.id, t.nome;
```

---

## Prioridade

A prioridade determina a ordem de execução quando múltiplas tarefas são agendadas:

- **1-3**: Alta prioridade (executadas primeiro)
- **4-7**: Média prioridade
- **8-10**: Baixa prioridade (executadas por último)

A ordenação é feita por `prioridade ASC` (menor número = maior prioridade).

---

## Agendamento Automático (Futuro)

Para agendamento automático via `pg_cron`, será necessário:

1. Habilitar extensão `pg_cron` no Supabase
2. Criar função `create_sync_job` (já existe em `sync_cron.sql`)
3. Atualizar tarefa ao salvar para criar/atualizar job no pg_cron

**Status**: Implementação futura (MVP usa execução manual)

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Tarefa não executa | Verificar se `ativo = true` e `api_id` está preenchido |
| Erro "API não encontrada" | Verificar se a API está ativa e o `api_id` está correto |
| Logs não aparecem | Verificar permissões RLS na tabela `logs_execucao` |
| Cron não funciona | Verificar formato da expressão cron (5 campos) |

---

## Referências

- [Integração Espaider](espaider_api.md)
- [Edge Function sync-solicitacoes](../devops/mcp_supabase.md#edge-functions)
