# MCP Supabase - Model Context Protocol

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-20

---

## Visão Geral

O **MCP (Model Context Protocol)** do Supabase permite que os agentes de IA interajam diretamente com o banco de dados e Edge Functions do projeto, sem necessidade de comandos manuais no dashboard ou CLI.

---

## Ferramentas Disponíveis

### Database

| Ferramenta | Descrição |
|------------|-----------|
| `mcp_supabase_list_tables` | Lista todas as tabelas em um schema |
| `mcp_supabase_execute_sql` | Executa SQL arbitrário (consultas) |
| `mcp_supabase_apply_migration` | Aplica uma migration DDL |
| `mcp_supabase_list_migrations` | Lista migrations existentes |
| `mcp_supabase_generate_typescript_types` | Gera tipos TypeScript a partir do schema |

### Edge Functions

| Ferramenta | Descrição |
|------------|-----------|
| `mcp_supabase_list_edge_functions` | Lista Edge Functions deployadas |
| `mcp_supabase_get_edge_function` | Obtém código de uma Edge Function |
| `mcp_supabase_deploy_edge_function` | Deploy/atualiza uma Edge Function |

### Monitoramento

| Ferramenta | Descrição |
|------------|-----------|
| `mcp_supabase_get_logs` | Obtém logs de serviços (api, postgres, auth, etc) |
| `mcp_supabase_get_advisors` | Verifica alertas de segurança/performance |
| `mcp_supabase_get_project_url` | Obtém URL do projeto |
| `mcp_supabase_get_publishable_keys` | Obtém chaves públicas |

### Branches (Pro)

| Ferramenta | Descrição |
|------------|-----------|
| `mcp_supabase_create_branch` | Cria branch de desenvolvimento |
| `mcp_supabase_list_branches` | Lista branches |
| `mcp_supabase_merge_branch` | Merge para produção |
| `mcp_supabase_delete_branch` | Remove branch |

### Documentação

| Ferramenta | Descrição |
|------------|-----------|
| `mcp_supabase_search_docs` | Busca na documentação oficial |

---

## Configuração

O MCP é configurado no Cursor IDE. Para habilitar:

1. Abrir configurações do Cursor
2. Ir em MCP Servers
3. Adicionar servidor Supabase com project_ref

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase", "--project-ref", "zldadtirkhlkzdviqqwd"]
    }
  }
}
```

---

## Uso pelos Agentes

### Eng. Software / Arquiteto

O agente de engenharia pode usar o MCP para:

- Aplicar migrations (`apply_migration`)
- Verificar estrutura do banco (`list_tables`)
- Deploy de Edge Functions (`deploy_edge_function`)
- Gerar tipos TypeScript (`generate_typescript_types`)

**Exemplo:**
```
"Aplique a migration para adicionar campos na tabela apis"
→ Agente usa mcp_supabase_apply_migration
```

### Segurança & Compliance

O agente de segurança pode usar o MCP para:

- Verificar advisories (`get_advisors`)
- Auditar RLS em tabelas (`list_tables` + `execute_sql`)
- Verificar logs de auth (`get_logs`)

**Exemplo:**
```
"Verifique se há alertas de segurança no projeto"
→ Agente usa mcp_supabase_get_advisors
```

### QA / Evals

O agente de QA pode usar o MCP para:

- Verificar dados de teste (`execute_sql`)
- Testar Edge Functions (`get_edge_function`, `deploy_edge_function`)
- Validar migrations

**Exemplo:**
```
"Verifique se a tabela solicitacoes tem RLS habilitado"
→ Agente usa mcp_supabase_list_tables e verifica rls_enabled
```

---

## Boas Práticas

### Migrations

1. **Sempre usar `apply_migration`** para DDL (CREATE, ALTER, DROP)
2. **Usar `execute_sql`** apenas para consultas ou DML simples
3. **Nomear migrations** em snake_case descritivo

```
apply_migration(
  name="add_api_espaider_fields",
  query="ALTER TABLE apis ADD COLUMN identificador TEXT..."
)
```

### Edge Functions

1. **Sempre incluir import do edge-runtime** no início:
   ```typescript
   import "jsr:@supabase/functions-js/edge-runtime.d.ts";
   ```

2. **Usar `Deno.serve()`** em vez de `serve()` do std

3. **Configurar `verify_jwt`** corretamente:
   - `true`: Requer autenticação (padrão)
   - `false`: Apenas para webhooks externos

### Segurança

1. **Nunca** executar SQL com dados não sanitizados
2. **Sempre** verificar advisories após mudanças de RLS
3. **Logar** operações sensíveis no changelog

---

## Troubleshooting

### "MCP server not responding"

1. Verificar se o Cursor está conectado
2. Reiniciar o Cursor
3. Verificar project_ref no config

### "Permission denied"

1. Verificar se o access token do Supabase está válido
2. Verificar permissões do projeto

### "Migration failed"

1. Verificar sintaxe SQL
2. Verificar dependências (views, constraints)
3. Usar CASCADE se necessário para drops

---

## Referências

- [Supabase MCP Documentation](https://supabase.com/docs/guides/ai/mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Cursor MCP Setup](https://docs.cursor.com/context/model-context-protocol)
