# Integração API Espaider

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-21
> **Agente responsável**: Eng. Software / Arquiteto IA & DevOps

---

## Visão Geral

A integração com o **Espaider** permite sincronizar solicitações/projetos do ERP para o Portal Tech Arauz. A API Espaider é um serviço WCF que retorna dados em um formato específico de `ListaRegistros` + `ListaCampos`.

---

## Arquitetura

```
┌────────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│   Portal Tech      │     │   Edge Function     │     │   API Espaider   │
│   (React/Vite)     │────▶│  sync-solicitacoes  │────▶│   (WCF/REST)     │
│                    │     │                     │     │                  │
└────────────────────┘     └─────────────────────┘     └──────────────────┘
         │                          │
         │                          ▼
         │                 ┌─────────────────────┐
         └────────────────▶│     Supabase DB     │
                           │   (solicitacoes)    │
                           └─────────────────────┘
```

---

## Configuração da API

### Campos Importantes

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `nome` | Nome identificador da API | Espaider Exportação - Projetos |
| `tipo` | Tipo da API (sempre `espaider`) | espaider |
| `recurso` | Módulo de destino no sistema | projetos |
| `url_base` | URL base do serviço WCF | https://espaider.com.br/.../ExportaDados |
| `identificador` | Parâmetro `Identificador` da API | BI_SOLICITACOES_SUPORTEESPAIDER |
| `tipo_autenticacao` | Método de autenticação | QueryParam |
| `token` | Token de autenticação | (criptografado) |

### Diferença entre `recurso` e `identificador`

- **`recurso`**: Define onde os dados serão importados no sistema (projetos, entregas, cronogramas)
- **`identificador`**: Parâmetro enviado à API Espaider para especificar qual dataset retornar

---

## Estrutura de Dados do Espaider

### Resposta da API (padrão WCF)

```json
{
  "Situacao": "S",
  "MensagemRetorno": null,
  "ListaRegistros": [
    {
      "IDEspaider": 116727,
      "Identificador": "BI_SOLICITACOES_SUPORTEESPAIDER",
      "ListaCampos": [
        {"Identificador": "NOME", "Valor": "Integração Sênior - Folha de pagamento"},
        {"Identificador": "CODIGO", "Valor": "ESPDR.00204/20"},
        {"Identificador": "STATUSPROJETO", "Valor": "Projeto futuro"},
        {"Identificador": "PRIORIDADE", "Valor": "Normal"},
        {"Identificador": "TIPOCHAMADO", "Valor": "Melhoria futura"},
        {"Identificador": "TIPOASSUNTO", "Valor": "RH"},
        {"Identificador": "SITUACAOATUAL", "Valor": "Em aprovação"},
        {"Identificador": "RESPONSAVELPROJETO", "Valor": "João Silva"},
        {"Identificador": "PRAZOFINAL", "Valor": "31/03/2026"},
        {"Identificador": "DATAINICIOAPROVACAO", "Valor": "19/05/2025 - 18:53:00"}
      ]
    }
  ],
  "URLPaginacao": null,
  "ListaURLFilhos": []
}
```

### Mapeamento de Campos

| Campo Espaider | Campo Sistema | Tipo |
|----------------|---------------|------|
| IDEspaider | id_espaider | integer |
| NOME | titulo | text |
| CODIGO | codigo_espaider | text |
| STATUSPROJETO | status_projeto | text |
| SITUACAOATUAL | status_id | uuid (lookup) |
| PRIORIDADE | prioridade_id | uuid (lookup) |
| TIPOCHAMADO | tipo_id | uuid (lookup) |
| TIPOASSUNTO | area_id | uuid (lookup) |
| PRAZOFINAL | data_previsao | timestamp |
| ENCERRADOEM | data_conclusao | timestamp |
| DATAINICIOAPROVACAO | data_abertura | timestamp |
| RESPONSAVELPROJETO | responsavel_nome | text |
| PASTACONSULTIVO | pasta_consultivo | text |

---

## Tabelas de Mapeamento

### espaider_field_mapping

Tabela para configurar mapeamentos dinâmicos entre campos do Espaider e do sistema.

```sql
CREATE TABLE espaider_field_mapping (
  id UUID PRIMARY KEY,
  campo_espaider TEXT NOT NULL,
  campo_sistema TEXT NOT NULL,
  tabela_lookup TEXT,  -- Se preenchido, faz lookup nesta tabela
  ativo BOOLEAN DEFAULT true
);
```

### codigo_externo nas tabelas de lookup

As tabelas de lookup (`status`, `prioridades`, `tipos`, `areas`) possuem um campo `codigo_externo` para mapear valores do Espaider:

```sql
-- Exemplo de mapeamento de status
UPDATE status SET codigo_externo = 'Em aprovação' WHERE nome = 'Aberto';
UPDATE status SET codigo_externo = 'Em execução' WHERE nome = 'Em Andamento';
```

---

## Edge Function: sync-solicitacoes

### Fluxo de Execução

1. Recebe parâmetros (opcional: `api_id`, `tarefa_id`)
2. Busca configuração da API Espaider
3. Cria registro de log de execução
4. Constrói URL com token e identificador (query params)
5. Faz requisição POST para API Espaider
6. Valida `Situacao == "S"` (erro se diferente)
7. Pagina usando `URLPaginacao` quando disponível
8. Parseia `ListaRegistros` → `ListaCampos` para objeto plano
7. Mapeia lookups (status, prioridade, tipo, área)
8. Converte datas do formato BR para ISO
9. Executa UPSERT baseado em `id_espaider`
10. Atualiza log de execução com resultado

### Invocação

```typescript
// Via UI (botão Sincronizar)
const { data, error } = await supabase.functions.invoke('sync-solicitacoes', {
  body: { api_id: 'uuid-da-api' }
});

// Via agendamento (pg_cron)
SELECT cron.schedule('sync-espaider', '0 */4 * * *', $$
  SELECT net.http_post(
    url := 'https://xxx.supabase.co/functions/v1/sync-solicitacoes',
    headers := '{"Authorization": "Bearer xxx"}'::jsonb
  )
$$);
```

### Tratamento de Erros

- **Retry automático**: 3 tentativas com exponential backoff
- **Timeout**: 60 segundos por requisição
- **Erro de negócio**: `Situacao != "S"` gera erro com `MensagemRetorno`
- **Log detalhado**: Erros são armazenados em `logs_execucao.detalhes.errors`
- **Status parcial**: Se alguns registros falharem, marca como `parcial`

---

## Segurança

### Considerações

- Token da API nunca é exposto no frontend (view `apis_safe` mascara)
- Edge Function usa `SERVICE_ROLE_KEY` para bypass RLS
- Validação de JWT habilitada para todas as chamadas
- Logs sanitizados (sem dados PII)

### RLS

A tabela `espaider_field_mapping` possui RLS:
- Admins podem gerenciar mapeamentos
- Todos usuários autenticados podem visualizar

---

## Monitoramento

### Logs de Execução

```sql
SELECT
  status,
  registros_processados,
  registros_novos,
  registros_atualizados,
  registros_erros,
  duracao_ms,
  created_at
FROM logs_execucao
WHERE detalhes->>'tipo' = 'sync_espaider'
ORDER BY created_at DESC
LIMIT 10;
```

### Última Sincronização

```sql
SELECT nome, ultima_sincronizacao
FROM apis
WHERE tipo = 'espaider';
```

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Token inválido | Verificar token no Espaider, atualizar na API |
| Campos não mapeados | Adicionar em `espaider_field_mapping` |
| Status não encontrado | Adicionar `codigo_externo` na tabela `status` |
| Timeout | Aumentar `RETRY_CONFIG.timeout` na Edge Function |
| Registros duplicados | Verificar se `id_espaider` está único |

---

## Teste de API

O teste de conexão da API é feito via Edge Function `test-api` para evitar problemas de CORS:

```typescript
// Via UI (botão Testar)
const { data, error } = await supabase.functions.invoke('test-api', {
  body: { api_id: 'uuid-da-api', include_raw: true }
});
```

A função retorna:
- `success`: boolean indicando se a conexão foi bem-sucedida
- `status`: código HTTP da resposta
- `statusText`: texto do status HTTP
- `registros_encontrados`: quantidade retornada no teste (se disponível)
- `raw`: JSON completo da resposta (quando `include_raw = true`)

---

## Tarefas de Sincronização

### Configuração de Tarefa

Cada tarefa de sincronização pode ser configurada com:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `nome` | Nome identificador da tarefa | Sync Projetos Espaider |
| `tipo` | Tipo da tarefa | espaider |
| `api_id` | API Espaider associada | UUID da API |
| `frequencia` | Frequência de execução | manual, diaria, semanal, mensal |
| `cron_schedule` | Expressão cron customizada | `0 6 * * *` |
| `timezone` | Fuso horário | America/Sao_Paulo |
| `prioridade` | Prioridade (1=alta, 10=baixa) | 5 |
| `ativo` | Se a tarefa está ativa | true |

### Execução Manual

Para executar uma tarefa manualmente (sem agendamento):

1. Acesse a tela de **Tarefas de Sync** (`/tarefas`)
2. Clique no botão **Executar** (ícone Play) na tarefa desejada
3. A execução será registrada em `logs_execucao` com:
   - Status (sucesso, erro, parcial)
   - Duração em milissegundos
   - Quantidade de registros processados/criados/atualizados/erros
   - Mensagem de erro (se houver)

### Logs de Execução

Todos os logs são armazenados na tabela `logs_execucao` com:

- **Tempo**: `iniciado_em`, `finalizado_em`, `duracao_ms`
- **Status**: `executando`, `sucesso`, `erro`, `parcial`, `cancelado`
- **Métricas**: `registros_processados`, `registros_novos`, `registros_atualizados`, `registros_erros`
- **Erros**: `mensagem_erro` e `detalhes` (JSONB)

---

## Próximos Passos

- [x] Teste de API via Edge Function (evita CORS)
- [x] Configuração parametrizável de tarefas
- [x] Execução manual de tarefas
- [x] Logs completos de execução
- [ ] Implementar sincronização de Entregas
- [ ] Implementar sincronização de Cronogramas
- [ ] Implementar sincronização de Requisitos
- [ ] Integração com pg_cron para agendamento automático
- [ ] Dashboard de métricas de sincronização
