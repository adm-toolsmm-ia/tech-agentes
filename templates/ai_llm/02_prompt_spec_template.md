# Template: Especificação de Prompt

> **Versão**: 1.0.0
> **Categoria**: AI/LLM
> **Uso**: Documentar prompts críticos de forma estruturada

---

## Metadados do Prompt

| Campo | Valor |
|-------|-------|
| **ID** | `PROMPT-[CATEGORIA]-[NUMERO]` |
| **Nome** | [Nome descritivo] |
| **Versão** | [X.Y.Z] |
| **Status** | `draft` / `review` / `approved` / `deprecated` |
| **Owner** | [Responsável] |
| **Data Criação** | [YYYY-MM-DD] |
| **Última Atualização** | [YYYY-MM-DD] |

---

## 1. Objetivo

### 1.1 Propósito
[Descrição clara do que o prompt deve realizar]

### 1.2 Casos de Uso
- [ ] Caso 1: [Descrição]
- [ ] Caso 2: [Descrição]
- [ ] Caso 3: [Descrição]

### 1.3 Não-Objetivos (Out of Scope)
- [O que este prompt NÃO deve fazer]
- [Limitações intencionais]

---

## 2. Contexto de Uso

### 2.1 Quando Usar
| Situação | Usar? | Notas |
|----------|-------|-------|
| [Situação 1] | ✅ | [Notas] |
| [Situação 2] | ✅ | [Notas] |
| [Situação 3] | ❌ | [Usar outro prompt] |

### 2.2 Pré-requisitos
- [Dados/contexto necessário antes de usar]
- [Validações que devem ocorrer antes]

### 2.3 Dependências
- **Prompts relacionados**: [Lista]
- **Dados externos**: [Lista]
- **Ferramentas/APIs**: [Lista]

---

## 3. Especificação do Prompt

### 3.1 System Prompt

```
[SYSTEM PROMPT COMPLETO]

Você é [PERSONA/PAPEL].

Seu objetivo é [OBJETIVO].

Regras:
1. [Regra 1]
2. [Regra 2]
3. [Regra 3]

Formato de resposta:
[FORMATO]

Restrições:
- [Restrição 1]
- [Restrição 2]
```

### 3.2 User Prompt Template

```
[USER PROMPT TEMPLATE]

Contexto:
{contexto}

Tarefa:
{tarefa}

Dados de entrada:
{dados}

Instruções adicionais:
{instrucoes}
```

### 3.3 Variáveis

| Variável | Tipo | Obrigatório | Descrição | Exemplo |
|----------|------|-------------|-----------|---------|
| `{contexto}` | string | Sim | Contexto do projeto/situação | "Sistema de e-commerce B2C" |
| `{tarefa}` | string | Sim | Tarefa específica a realizar | "Analisar requisitos" |
| `{dados}` | string/JSON | Sim | Dados de entrada | `{"doc": "..."}` |
| `{instrucoes}` | string | Não | Instruções específicas | "Foco em segurança" |

---

## 4. Formato de Saída

### 4.1 Schema JSON

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["campo1", "campo2"],
  "properties": {
    "campo1": {
      "type": "string",
      "description": "Descrição do campo"
    },
    "campo2": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "subcampo": {"type": "string"}
        }
      }
    }
  }
}
```

### 4.2 Exemplo de Output Esperado

```json
{
  "campo1": "valor exemplo",
  "campo2": [
    {"subcampo": "valor 1"},
    {"subcampo": "valor 2"}
  ]
}
```

---

## 5. Configuração de Modelo

### 5.1 Parâmetros Recomendados

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| **Modelo** | [gpt-5.2-codex / opus-4.5 / sonnet-4.5 / gpt-4o] | [Razão] |
| **Temperature** | [0.0 - 1.0] | [Razão] |
| **Top-p** | [0.0 - 1.0] | [Razão] |
| **Max Tokens** | [número] | [Razão] |
| **Stop Sequences** | [lista] | [Razão] |

### 5.2 Fallback

Se modelo primário indisponível:
1. Fallback 1: [modelo]
2. Fallback 2: [modelo]

---

## 6. Exemplos (Few-Shot)

### 6.1 Exemplo 1: [Nome do Cenário]

**Input**:
```
{contexto}: "..."
{tarefa}: "..."
{dados}: "..."
```

**Output Esperado**:
```json
{
  ...
}
```

**Notas**: [Observações sobre este exemplo]

### 6.2 Exemplo 2: [Nome do Cenário]

**Input**:
```
{contexto}: "..."
{tarefa}: "..."
{dados}: "..."
```

**Output Esperado**:
```json
{
  ...
}
```

### 6.3 Exemplo 3: Edge Case

**Input**:
```
{contexto}: "..."
{tarefa}: "..."
{dados}: "[dados mínimos/ambíguos]"
```

**Output Esperado**:
```json
{
  "status": "incomplete",
  "missing_info": ["..."],
  "partial_result": {...}
}
```

---

## 7. Validação e Qualidade

### 7.1 Critérios de Sucesso

| Critério | Threshold | Métrica |
|----------|-----------|---------|
| Aderência ao schema | 100% | JSON válido |
| Completude | ≥ 90% | Campos preenchidos |
| Precisão | ≥ 95% | Dados corretos |
| Latência | < 10s | Tempo de resposta |

### 7.2 Golden Sets

Referência: [`evals/golden_sets.json`](../../evals/golden_sets.json)

| ID do Caso | Descrição | Status |
|------------|-----------|--------|
| [CASO-001] | [Descrição] | ✅ Passa |
| [CASO-002] | [Descrição] | ✅ Passa |

### 7.3 Rubricas de Avaliação

Referência: [`evals/rubricas.json`](../../evals/rubricas.json)

| Rubrica | Threshold |
|---------|-----------|
| `json_validity` | 1 |
| `grounding_no_hallucination` | 1 |

---

## 8. Guardrails

### 8.1 Anti-Alucinação

- [ ] Prompt inclui instrução "se não souber, dizer que não sabe"
- [ ] Output inclui campo de confiança quando aplicável
- [ ] Prompt restringe fontes de dados aceitas

### 8.2 Segurança

- [ ] Prompt não aceita instruções do usuário que sobrescrevam sistema
- [ ] Output é validado antes de ações (especialmente code execution)
- [ ] PII é mascarada no output quando aplicável

### 8.3 Limites

| Limite | Valor | Ação se Exceder |
|--------|-------|-----------------|
| Input máximo | [tokens] | Truncar/dividir |
| Output máximo | [tokens] | Continuar em nova chamada |
| Tempo máximo | [segundos] | Timeout + retry |

---

## 9. Troubleshooting

### 9.1 Problemas Comuns

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| JSON inválido | Temperature alta | Reduzir para 0.0-0.1 |
| Dados inventados | Falta de grounding | Adicionar guardrail explícito |
| Output truncado | Max tokens baixo | Aumentar limite |
| Inconsistência | Prompt ambíguo | Adicionar exemplos |

### 9.2 Debugging

```python
# Logging para debug
import logging
logger = logging.getLogger("prompt_debug")

def execute_prompt(input_data):
    logger.debug(f"Input: {input_data}")
    # ... chamada ao modelo
    logger.debug(f"Output: {output}")
    logger.debug(f"Tokens: {usage}")
    return output
```

---

## 10. Histórico de Versões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0.0 | YYYY-MM-DD | [Nome] | Versão inicial |
| 1.0.1 | YYYY-MM-DD | [Nome] | [Descrição] |

---

## 11. Aprovações

| Papel | Nome | Data | Status |
|-------|------|------|--------|
| Criador | [Nome] | [Data] | ✅ |
| Reviewer | [Nome] | [Data] | ⏳ |
| CTO | [Nome] | [Data] | ⏳ |

---

## Anexos

### A. Prompt Completo (Copy-Paste Ready)

```
[SYSTEM]
[Cole aqui o system prompt completo]

[USER]
[Cole aqui o user prompt template]
```

### B. Código de Integração

```python
from tech_agents.prompts import PromptTemplate

prompt = PromptTemplate.load("PROMPT-[ID]")
result = prompt.execute(
    contexto="...",
    tarefa="...",
    dados="...",
    model="gpt-5.2-codex",
    temperature=0.1
)
```

### C. Referências

- [Documentação do Modelo]
- [Papers/Artigos relacionados]
- [Prompts relacionados]
