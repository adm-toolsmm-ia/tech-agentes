# Prompts

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém templates de prompts padronizados para uso com agentes AI no framework tech-agentes. Os templates são organizados por categoria de tarefa e seguem uma estrutura consistente para maximizar eficiência e qualidade.

---

## Catálogo de Templates

| Arquivo | Categoria | Descrição |
|---------|-----------|-----------|
| [`templates_analise.md`](templates_analise.md) | Análise | Requisitos, riscos, gaps, viabilidade, comparação |
| [`templates_extracao.md`](templates_extracao.md) | Extração | Entidades, dados tabulares, metadados, ações, configs |
| [`templates_geracao.md`](templates_geracao.md) | Geração | Código, documentação, testes, dados, comunicação |
| [`templates_decisao.md`](templates_decisao.md) | Decisão | ADRs, priorização, trade-offs, go/no-go |

---

## Estrutura Padrão de Template

Cada template segue a estrutura:

```markdown
# Template: [Nome]

## Objetivo
O que o template faz e qual problema resolve.

## Quando Usar
Situações em que este template é apropriado.

## Formato de Entrada
Estrutura esperada do input.

## Formato de Saída (Schema)
JSON schema do output esperado.

## Exemplo (Few-Shot)
Input e output de exemplo para guiar o modelo.

## Critérios de Sucesso
Checklist de qualidade do output.

## Guardrails (Anti-alucinação)
Regras para evitar outputs incorretos ou inventados.
```

---

## Como Usar

### 1. Seleção de Template

```
Tipo de Tarefa → Categoria → Template Específico

Exemplo:
- Preciso extrair dados de um documento → Extração → Extração de Entidades
- Preciso decidir entre tecnologias → Decisão → ADR ou Trade-off Analysis
```

### 2. Preparação do Input

1. Leia a seção "Formato de Entrada" do template
2. Prepare os dados no formato especificado
3. Inclua contexto relevante

### 3. Configuração do Modelo

| Categoria | Temperature | Top-p | Notas |
|-----------|-------------|-------|-------|
| Extração | 0.0 - 0.1 | 1.0 | Máxima precisão |
| Análise | 0.2 - 0.3 | 0.9 | Precisão com leve variação |
| Geração | 0.3 - 0.5 | 0.95 | Balanceado |
| Decisão | 0.2 - 0.3 | 0.9 | Consistência |

### 4. Validação do Output

1. Verifique se output é JSON válido (quando aplicável)
2. Valide contra schema esperado
3. Revise critérios de sucesso
4. Confirme guardrails respeitados

---

## Composição de Templates

Templates podem ser combinados em pipelines:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Análise de      │────▶│ Análise de      │────▶│ Decisão         │
│ Requisitos      │     │ Riscos          │     │ Go/No-Go        │
└─────────────────┘     └─────────────────┘     └─────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Extração de     │────▶│ Geração de      │────▶│ Geração de      │
│ Entidades       │     │ Código          │     │ Testes          │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Validação Pós-Processo

### Para Extração (JSON)

```python
from pydantic import BaseModel, ValidationError

def validate_extraction(data: dict, schema: type[BaseModel]) -> BaseModel:
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        raise ExtractionError(f"Extração inválida: {e}")
```

### Para Geração de Código

```bash
# 1. Lint
ruff check generated_code.py

# 2. Type check
mypy generated_code.py

# 3. Testes
pytest tests/test_generated.py
```

---

## Versionamento

### Política de Versão

- **Patch (0.0.X)**: Correções de typos, melhorias de exemplos
- **Minor (0.X.0)**: Novos templates, novos campos opcionais
- **Major (X.0.0)**: Mudanças breaking em schemas

### Processo de Mudança

1. Criar branch `prompt/[nome-mudanca]`
2. Atualizar template com nova versão
3. Rodar golden sets para validar
4. PR com evidência de testes
5. Aprovação do CTO para mudanças major

---

## Golden Sets

Os templates devem ser validados contra golden sets em [`evals/golden_sets.json`](../evals/golden_sets.json).

### Rodando Validação

```bash
# Validar todos os templates
# CLI tech-agentes não faz parte deste repositório
# Use o processo de validação descrito em docs/evals/README.md
```

---

## Troubleshooting

### Output não é JSON válido

1. Verificar se prompt inclui instrução explícita de formato JSON
2. Reduzir temperature para 0.0-0.1
3. Adicionar exemplo de output no prompt

### Modelo "alucina" dados

1. Verificar guardrails do template
2. Adicionar instrução explícita: "Se não souber, diga que não sabe"
3. Reduzir temperatura
4. Adicionar mais exemplos few-shot

### Output incompleto

1. Verificar limite de tokens do modelo
2. Dividir tarefa em partes menores
3. Usar template de continuação

### Inconsistência entre execuções

1. Fixar temperatura em 0.0 para reprodutibilidade
2. Usar seed quando disponível no modelo
3. Aumentar especificidade do prompt

---

## Contribuindo

### Criando Novo Template

1. Identificar categoria apropriada
2. Seguir estrutura padrão
3. Incluir pelo menos 1 exemplo few-shot
4. Definir schema de output
5. Criar golden set para validação
6. Documentar guardrails

### Revisando Template Existente

1. Verificar se mudança é breaking
2. Atualizar versão apropriadamente
3. Rodar golden sets
4. Atualizar exemplos se necessário

---

## Referências

- [Guia de Modelos](../docs/modelos/guia_modelos.md)
- [Políticas de Segurança](../docs/seguranca/politicas.md)
- [Golden Sets](../evals/golden_sets.json)
- [Rubricas de Avaliação](../evals/rubricas.json)
