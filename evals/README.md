# Evals (Avaliações)

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém o sistema de avaliação de qualidade para prompts, modelos e outputs do framework tech-agentes.

---

## Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| [`golden_sets.json`](golden_sets.json) | Casos de teste para regressão |
| [`rubricas.json`](rubricas.json) | Critérios de avaliação |
| [`resultados/`](resultados/) | Resultados de execuções |

---

## Conceitos

### Golden Sets

Conjunto de casos de teste com inputs e outputs esperados. Usados para:

- **Regressão**: Verificar que mudanças não quebram comportamento
- **Validação**: Testar novos prompts antes de produção
- **Benchmark**: Comparar performance entre modelos

### Rubricas

Critérios de avaliação com escalas definidas:

- **Automáticas**: JSON validity, code safety, pattern matching
- **LLM Judge**: Avaliação semântica por outro modelo
- **Estatísticas**: Calibração, latência (requerem batch)

---

## Como Usar

### 1. Rodar Golden Sets

```bash
# Todos os casos (saída externa obrigatória)
# Gere outputs externamente e salve em evals/resultados/outputs_eval.json
# Para casos específicos, gere apenas os case_ids desejados
# Smoke test: usar expected_output como saída para validar estrutura
```

### Formato de outputs externos

Arquivo JSON com `case_id` → `output`:

```json
{
  "extraction-json-001": {
    "entidades": [{"tipo": "documento", "valor": "2024-001", "valor_normalizado": "2024-001"}]
  },
  "analysis-requirements-001": {
    "requisitos_funcionais": [{"id": "RF-001", "titulo": "Agendamento online", "prioridade": "must"}]
  }
}
```

### 2. Verificar Resultados

```bash
# Ver último resultado
cat evals/resultados/latest_dev.json | jq '.summary'

# Ver falhas
cat evals/resultados/latest_dev.json | jq '.results[] | select(.status == "failed")'
```

### 3. Verificar Gate

```bash
# Verificar se pode promover
# Verificar gate manualmente via resumo em evals/resultados/latest_dev.json
#
# Output esperado:
# ✅ Pass rate: 96% (threshold: 95%)
# ✅ Critical cases: 5/5 passed
# ✅ Latency: 2.3s avg (SLO: 8s)
# ✅ GATE PASSED - Can promote to stage
```

---

## Adicionando Novo Caso

### 1. Definir Caso

```json
{
  "id": "unique-id-001",
  "name": "Nome descritivo",
  "task_type": "extraction|analysis|generation|decision|security",
  "criticality": "critical|high|medium|low",
  "description": "O que este caso testa",
  "prompt_template": "templates_*.md#seção",
  "input": {
    "text": "Input do caso",
    "params": {}
  },
  "expected_output": {
    "field": "valor esperado"
  },
  "validation": {
    "type": "json_schema|semantic|code|security",
    "config": {}
  },
  "rubrics": ["rubrica1", "rubrica2"]
}
```

### 2. Adicionar ao golden_sets.json

### 3. Rodar e Validar

```bash
# Execute o novo caso via pipeline de evals do projeto
```

---

## Rubricas Disponíveis

### Formato
- `json_validity`: JSON válido e parseável
- `code_validity`: Código compila/parseia

### Qualidade
- `grounding_no_hallucination`: Sem alucinações
- `extraction_completeness`: Completude da extração
- `extraction_precision`: Precisão da extração
- `analysis_completeness`: Completude da análise
- `decision_completeness`: Estrutura de decisão

### Código
- `code_safety`: Sem padrões inseguros
- `test_coverage`: Cobertura de casos de teste

### Segurança
- `security_prompt_injection`: Resistência a injection

### Performance
- `latency_acceptable`: Latência dentro do SLO

---

## Gates por Ambiente

| Ambiente | Pass Rate | Critical | Latency |
|----------|-----------|----------|---------|
| Dev | >= 80% | N/A | N/A |
| Stage | >= 90% | 100% | < 2x SLO |
| Prod | >= 95% | 100% | < SLO |

---

## Manutenção

### Atualizando Golden Sets

1. Mudanças em prompts → rodar golden sets
2. Se falhar → ajustar prompt OU atualizar expected_output
3. Se atualizar expected → justificar e aprovar

### Revisão Periódica

- **Semanal**: Verificar novos casos necessários
- **Mensal**: Revisar thresholds e rubricas
- **Trimestral**: Auditoria completa

---

## Referências

- [Templates de Prompts](../prompts/)
- [Padrões do Projeto](../docs/padrões/padroes_projeto.md)
- [Workflows](../workflows/)
