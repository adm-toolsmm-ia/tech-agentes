# Resultados de Avaliações

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório armazena os resultados de execuções de golden sets e avaliações de qualidade. Estes resultados são **obrigatórios como evidência** antes de promover para stage/prod.

---

## Estrutura de Arquivos

```
resultados/
├── README.md                          # Este arquivo
├── YYYY-MM-DD_HH-MM-SS_[env].json    # Resultado de execução
├── latest_dev.json                    # Link para último resultado dev
├── latest_stage.json                  # Link para último resultado stage
└── latest_prod.json                   # Link para último resultado prod
```

---

## Formato de Resultado

```json
{
  "execution_id": "uuid",
  "timestamp": "2026-01-18T10:30:00Z",
  "environment": "dev|stage|prod",
  "version": {
    "framework": "1.0.0",
    "golden_sets": "1.0.0",
    "rubricas": "1.0.0"
  },
  "config": {
    "model": "gpt-5.2-codex",
    "temperature": 0.1
  },
  "summary": {
    "total_cases": 10,
    "passed": 9,
    "failed": 1,
    "skipped": 0,
    "pass_rate": 0.90,
    "duration_seconds": 45
  },
  "results": [
    {
      "case_id": "extraction-json-001",
      "status": "passed|failed|skipped",
      "rubric_scores": {
        "json_validity": 1.0,
        "grounding_no_hallucination": 1.0,
        "extraction_completeness": 0.95
      },
      "latency_ms": 1234,
      "tokens_used": {
        "input": 500,
        "output": 200
      },
      "output": {},
      "expected": {},
      "diff": null,
      "notes": ""
    }
  ],
  "gate_status": {
    "golden_sets_pass": true,
    "can_promote": true
  }
}
```

---

## Política de Retenção

| Ambiente | Retenção |
|----------|----------|
| Dev | 30 dias |
| Stage | 90 dias |
| Prod | 1 ano |

---

## Como Gerar Resultados

### Via CLI

```bash
# Rodar todos os golden sets com outputs externos
tech-agents eval . --outputs-json outputs_eval.json --env dev

# Rodar casos específicos
tech-agents eval . --cases extraction-json-001,analysis-requirements-001 --outputs-json outputs_eval.json

# Smoke test (usa expected_output como saída)
tech-agents eval . --use-expected --allow-skip-llm-judge
```

### Via Código

```python
from tech_agents.evals import EvalRunner

runner = EvalRunner(
    golden_sets_path="evals/golden_sets.json",
    rubricas_path="evals/rubricas.json",
    output_dir="evals/resultados/",
)

results = runner.run_all(
    environment="dev",
    outputs_path="outputs_eval.json",
)
print(results["summary"])
```

---

## Gates de Promoção

### Dev → Stage

- [ ] Pass rate >= 90%
- [ ] Nenhum caso crítico falhou
- [ ] Latência dentro do SLO

### Stage → Prod

- [ ] Pass rate >= 95%
- [ ] Nenhum caso crítico falhou
- [ ] Latência dentro do SLO
- [ ] Aprovação do QA Lead
- [ ] Resultado salvo em `evals/resultados/`

---

## Analisando Falhas

### Verificar Resultado Específico

```bash
# Listar resultados recentes
ls -la evals/resultados/

# Ver detalhes de um resultado
cat evals/resultados/2026-01-18_10-30-00_dev.json | jq '.results[] | select(.status == "failed")'
```

### Ações por Tipo de Falha

| Rubrica Falhando | Ação |
|------------------|------|
| `json_validity` | Verificar prompt para garantir formato JSON |
| `grounding_no_hallucination` | Adicionar guardrails explícitos |
| `extraction_completeness` | Melhorar exemplos few-shot |
| `code_safety` | Adicionar validações de segurança |
| `security_prompt_injection` | Fortalecer separação system/user |

---

## Referências

- [Golden Sets](../golden_sets.json)
- [Rubricas](../rubricas.json)
- [Padrões de Projeto](../../docs/padrões/padroes_projeto.md)
