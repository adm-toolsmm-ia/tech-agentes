# Templates de Extração

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18
> **Categoria**: Extração Estruturada

---

## Índice de Templates

1. [Extração de Entidades](#1-extração-de-entidades)
2. [Extração de Dados Tabulares](#2-extração-de-dados-tabulares)
3. [Extração de Metadados](#3-extração-de-metadados)
4. [Extração de Ações/Tarefas](#4-extração-de-açõestarefas)
5. [Extração de Configurações](#5-extração-de-configurações)

---

## Princípios de Extração

### Configuração Recomendada
- **Temperature**: 0.0 - 0.1 (máxima precisão)
- **Top-p**: 1.0
- **Formato**: JSON com schema fixo

### Validação Obrigatória
Toda extração deve passar por validação pós-processo:
```python
from pydantic import BaseModel, ValidationError

def validate_extraction(data: dict, schema: type[BaseModel]) -> BaseModel:
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        # Log erro e retornar para revisão humana
        raise ExtractionError(f"Extração inválida: {e}")
```

---

## 1. Extração de Entidades

### Objetivo
Extrair entidades nomeadas (pessoas, organizações, datas, valores, etc.) de texto não estruturado.

### Quando Usar
- Processamento de documentos
- Análise de contratos
- Parsing de emails/mensagens

### Formato de Entrada
```
Texto para extração:
[TEXTO]

Tipos de entidades a extrair:
[TIPOS]

Contexto adicional (opcional):
[CONTEXTO]
```

### Formato de Saída (Schema)
```json
{
  "entidades": [
    {
      "tipo": "pessoa|organizacao|data|valor_monetario|endereco|email|telefone|documento|produto|outro",
      "valor": "string",
      "valor_normalizado": "string|null",
      "posicao": {
        "inicio": 0,
        "fim": 0
      },
      "confianca": 0.0-1.0,
      "contexto": "string"
    }
  ],
  "texto_original": "string",
  "metadados": {
    "total_entidades": 0,
    "tipos_encontrados": ["string"],
    "avisos": ["string"]
  }
}
```

### Exemplo (Few-Shot)

**Input**:
```
Texto: "O contrato nº 2024/001 foi assinado por João Silva (CPF: 123.456.789-00)
em 15/01/2024, no valor de R$ 50.000,00. Contato: joao@empresa.com"

Tipos: pessoa, documento, data, valor_monetario, email
```

**Output**:
```json
{
  "entidades": [
    {
      "tipo": "documento",
      "valor": "2024/001",
      "valor_normalizado": "2024/001",
      "posicao": {"inicio": 14, "fim": 22},
      "confianca": 0.95,
      "contexto": "número do contrato"
    },
    {
      "tipo": "pessoa",
      "valor": "João Silva",
      "valor_normalizado": "JOAO SILVA",
      "posicao": {"inicio": 42, "fim": 52},
      "confianca": 0.98,
      "contexto": "signatário do contrato"
    },
    {
      "tipo": "documento",
      "valor": "123.456.789-00",
      "valor_normalizado": "12345678900",
      "posicao": {"inicio": 59, "fim": 73},
      "confianca": 0.99,
      "contexto": "CPF do signatário"
    },
    {
      "tipo": "data",
      "valor": "15/01/2024",
      "valor_normalizado": "2024-01-15",
      "posicao": {"inicio": 79, "fim": 89},
      "confianca": 0.99,
      "contexto": "data de assinatura"
    },
    {
      "tipo": "valor_monetario",
      "valor": "R$ 50.000,00",
      "valor_normalizado": "50000.00",
      "posicao": {"inicio": 104, "fim": 116},
      "confianca": 0.99,
      "contexto": "valor do contrato"
    },
    {
      "tipo": "email",
      "valor": "joao@empresa.com",
      "valor_normalizado": "joao@empresa.com",
      "posicao": {"inicio": 127, "fim": 143},
      "confianca": 0.99,
      "contexto": "contato do signatário"
    }
  ],
  "texto_original": "O contrato nº 2024/001...",
  "metadados": {
    "total_entidades": 6,
    "tipos_encontrados": ["documento", "pessoa", "data", "valor_monetario", "email"],
    "avisos": []
  }
}
```

### Critérios de Sucesso
- [ ] Todas as entidades solicitadas extraídas
- [ ] Valores normalizados em formato padrão
- [ ] Confiança < 0.8 sinalizada para revisão
- [ ] Posições corretas no texto original

### Guardrails (Anti-alucinação)
- NÃO inventar entidades não presentes no texto
- NÃO inferir valores não explícitos
- SINALIZAR baixa confiança quando ambíguo
- RETORNAR lista vazia se nenhuma entidade encontrada

---

## 2. Extração de Dados Tabulares

### Objetivo
Extrair dados estruturados em formato tabular a partir de texto, PDFs ou imagens.

### Quando Usar
- Processamento de relatórios
- Extração de tabelas de documentos
- Conversão de dados não estruturados

### Formato de Entrada
```
Conteúdo com dados tabulares:
[CONTEUDO]

Colunas esperadas (opcional):
[COLUNAS]

Formato de saída desejado:
[FORMATO]
```

### Formato de Saída (Schema)
```json
{
  "tabela": {
    "nome": "string",
    "colunas": [
      {
        "nome": "string",
        "tipo": "string|number|date|boolean",
        "descricao": "string"
      }
    ],
    "linhas": [
      {
        "valores": {},
        "linha_original": "string",
        "confianca": 0.0-1.0
      }
    ]
  },
  "metadados": {
    "total_linhas": 0,
    "linhas_com_erro": 0,
    "colunas_inferidas": false,
    "avisos": ["string"]
  }
}
```

### Exemplo (Few-Shot)

**Input**:
```
Relatório de Vendas - Janeiro 2024

Vendedor    | Região  | Vendas    | Meta      | Atingimento
------------|---------|-----------|-----------|------------
Ana Costa   | Sul     | 45.000    | 40.000    | 112%
Bruno Lima  | Norte   | 32.500    | 35.000    | 93%
Carla Dias  | Centro  | 58.200    | 50.000    | 116%
```

**Output**:
```json
{
  "tabela": {
    "nome": "Relatório de Vendas - Janeiro 2024",
    "colunas": [
      {"nome": "vendedor", "tipo": "string", "descricao": "Nome do vendedor"},
      {"nome": "regiao", "tipo": "string", "descricao": "Região de atuação"},
      {"nome": "vendas", "tipo": "number", "descricao": "Valor de vendas em reais"},
      {"nome": "meta", "tipo": "number", "descricao": "Meta em reais"},
      {"nome": "atingimento", "tipo": "number", "descricao": "Percentual de atingimento"}
    ],
    "linhas": [
      {
        "valores": {
          "vendedor": "Ana Costa",
          "regiao": "Sul",
          "vendas": 45000,
          "meta": 40000,
          "atingimento": 112
        },
        "linha_original": "Ana Costa   | Sul     | 45.000    | 40.000    | 112%",
        "confianca": 0.98
      },
      {
        "valores": {
          "vendedor": "Bruno Lima",
          "regiao": "Norte",
          "vendas": 32500,
          "meta": 35000,
          "atingimento": 93
        },
        "linha_original": "Bruno Lima  | Norte   | 32.500    | 35.000    | 93%",
        "confianca": 0.98
      },
      {
        "valores": {
          "vendedor": "Carla Dias",
          "regiao": "Centro",
          "vendas": 58200,
          "meta": 50000,
          "atingimento": 116
        },
        "linha_original": "Carla Dias  | Centro  | 58.200    | 50.000    | 116%",
        "confianca": 0.98
      }
    ]
  },
  "metadados": {
    "total_linhas": 3,
    "linhas_com_erro": 0,
    "colunas_inferidas": false,
    "avisos": []
  }
}
```

### Critérios de Sucesso
- [ ] Colunas corretamente identificadas
- [ ] Tipos de dados corretos
- [ ] Valores numéricos parseados corretamente
- [ ] Linhas com erro sinalizadas

### Guardrails (Anti-alucinação)
- NÃO inventar dados não presentes
- NÃO preencher células vazias com inferências
- MANTER null para valores ausentes
- SINALIZAR linhas mal formatadas

---

## 3. Extração de Metadados

### Objetivo
Extrair metadados estruturados de documentos, código ou artefatos.

### Quando Usar
- Catalogação de documentos
- Indexação de conteúdo
- Análise de código-fonte

### Formato de Entrada
```
Artefato para análise:
[ARTEFATO]

Metadados a extrair:
[METADADOS]
```

### Formato de Saída (Schema)
```json
{
  "artefato": {
    "tipo": "documento|codigo|config|imagem|outro",
    "nome": "string",
    "caminho": "string"
  },
  "metadados": {
    "titulo": "string",
    "descricao": "string",
    "autor": "string",
    "data_criacao": "ISO8601",
    "data_modificacao": "ISO8601",
    "versao": "string",
    "tags": ["string"],
    "idioma": "string",
    "tamanho": "string",
    "formato": "string",
    "dependencias": ["string"],
    "referencias": ["string"],
    "custom": {}
  },
  "qualidade": {
    "completude": 0.0-1.0,
    "campos_ausentes": ["string"],
    "avisos": ["string"]
  }
}
```

### Critérios de Sucesso
- [ ] Metadados principais extraídos
- [ ] Datas em formato ISO8601
- [ ] Tags relevantes identificadas
- [ ] Campos ausentes sinalizados

### Guardrails (Anti-alucinação)
- NÃO inventar autores ou datas
- NÃO inferir versões sem evidência
- USAR null para campos não encontrados

---

## 4. Extração de Ações/Tarefas

### Objetivo
Extrair action items, tarefas e compromissos de textos como atas, emails ou conversas.

### Quando Usar
- Processamento de atas de reunião
- Análise de threads de email
- Extração de follow-ups de conversas

### Formato de Entrada
```
Texto com ações/tarefas:
[TEXTO]

Participantes conhecidos (opcional):
[PARTICIPANTES]

Contexto do projeto (opcional):
[CONTEXTO]
```

### Formato de Saída (Schema)
```json
{
  "acoes": [
    {
      "id": "ACTION-001",
      "descricao": "string",
      "responsavel": "string",
      "prazo": "ISO8601|null",
      "prazo_texto_original": "string",
      "prioridade": "alta|media|baixa|indefinida",
      "status": "pendente|em_andamento|concluida|cancelada",
      "contexto": "string",
      "dependencias": ["ACTION-XXX"],
      "confianca": 0.0-1.0
    }
  ],
  "decisoes": [
    {
      "descricao": "string",
      "decidido_por": "string",
      "data": "ISO8601|null",
      "contexto": "string"
    }
  ],
  "perguntas_abertas": ["string"],
  "metadados": {
    "total_acoes": 0,
    "acoes_sem_responsavel": 0,
    "acoes_sem_prazo": 0,
    "fonte": "string"
  }
}
```

### Exemplo (Few-Shot)

**Input**:
```
Ata da Reunião de Planejamento - 15/01/2024

Participantes: Ana (PM), Bruno (Dev), Carla (Design)

Discussões:
- Decidimos usar React para o frontend
- Bruno vai configurar o ambiente de desenvolvimento até sexta
- Carla precisa entregar os wireframes na próxima semana
- Ana ficou de agendar reunião com o cliente (urgente)
- Pendente: definir stack de backend
```

**Output**:
```json
{
  "acoes": [
    {
      "id": "ACTION-001",
      "descricao": "Configurar ambiente de desenvolvimento",
      "responsavel": "Bruno",
      "prazo": "2024-01-19",
      "prazo_texto_original": "até sexta",
      "prioridade": "media",
      "status": "pendente",
      "contexto": "Setup inicial do projeto",
      "dependencias": [],
      "confianca": 0.95
    },
    {
      "id": "ACTION-002",
      "descricao": "Entregar wireframes",
      "responsavel": "Carla",
      "prazo": "2024-01-22",
      "prazo_texto_original": "na próxima semana",
      "prioridade": "media",
      "status": "pendente",
      "contexto": "Design do projeto",
      "dependencias": [],
      "confianca": 0.90
    },
    {
      "id": "ACTION-003",
      "descricao": "Agendar reunião com o cliente",
      "responsavel": "Ana",
      "prazo": null,
      "prazo_texto_original": null,
      "prioridade": "alta",
      "status": "pendente",
      "contexto": "Alinhamento com stakeholder",
      "dependencias": [],
      "confianca": 0.95
    }
  ],
  "decisoes": [
    {
      "descricao": "Usar React para o frontend",
      "decidido_por": "Equipe",
      "data": "2024-01-15",
      "contexto": "Definição de stack"
    }
  ],
  "perguntas_abertas": [
    "Definir stack de backend"
  ],
  "metadados": {
    "total_acoes": 3,
    "acoes_sem_responsavel": 0,
    "acoes_sem_prazo": 1,
    "fonte": "Ata da Reunião de Planejamento - 15/01/2024"
  }
}
```

### Critérios de Sucesso
- [ ] Ações têm responsável identificado
- [ ] Prazos convertidos para ISO8601
- [ ] Prioridades inferidas do contexto
- [ ] Decisões separadas de ações

### Guardrails (Anti-alucinação)
- NÃO inventar responsáveis não mencionados
- NÃO inferir prazos sem base textual
- USAR "indefinida" para prioridade não clara
- MANTER prazo_texto_original para auditoria

---

## 5. Extração de Configurações

### Objetivo
Extrair parâmetros de configuração de documentos, código ou especificações.

### Quando Usar
- Migração de configurações
- Documentação de sistemas
- Análise de dependências

### Formato de Entrada
```
Fonte de configuração:
[FONTE]

Tipo de configuração:
[TIPO]

Schema esperado (opcional):
[SCHEMA]
```

### Formato de Saída (Schema)
```json
{
  "configuracoes": [
    {
      "chave": "string",
      "valor": "any",
      "tipo": "string|number|boolean|array|object",
      "obrigatorio": true,
      "padrao": "any|null",
      "descricao": "string",
      "validacao": "string|null",
      "sensivel": false,
      "fonte": "string"
    }
  ],
  "grupos": [
    {
      "nome": "string",
      "descricao": "string",
      "configuracoes": ["string"]
    }
  ],
  "metadados": {
    "total_configs": 0,
    "configs_sensiveis": 0,
    "configs_sem_padrao": 0,
    "formato_origem": "string"
  }
}
```

### Critérios de Sucesso
- [ ] Tipos corretamente inferidos
- [ ] Valores sensíveis marcados
- [ ] Agrupamento lógico aplicado
- [ ] Validações identificadas

### Guardrails (Anti-alucinação)
- NÃO inventar valores padrão
- NÃO assumir obrigatoriedade sem evidência
- MARCAR como sensível na dúvida
- PRESERVAR valores originais exatos

---

## Boas Práticas de Extração

### Validação em Pipeline

```python
def extraction_pipeline(text: str, template: str) -> dict:
    # 1. Extração via LLM
    raw_result = llm_extract(text, template)

    # 2. Parse JSON
    try:
        parsed = json.loads(raw_result)
    except json.JSONDecodeError:
        return {"error": "JSON inválido", "raw": raw_result}

    # 3. Validação de schema
    try:
        validated = Schema.model_validate(parsed)
    except ValidationError as e:
        return {"error": "Schema inválido", "details": str(e)}

    # 4. Validações de negócio
    warnings = business_validations(validated)

    return {"data": validated.model_dump(), "warnings": warnings}
```

### Tratamento de Erros

| Cenário | Ação |
|---------|------|
| JSON malformado | Retry com prompt de correção |
| Schema inválido | Log + revisão humana |
| Confiança < 0.7 | Flag para revisão |
| Dados sensíveis | Mascarar antes de logar |

### Métricas de Qualidade

- **Precision**: % de extrações corretas
- **Recall**: % de entidades encontradas
- **F1-Score**: Média harmônica
- **Confidence Calibration**: Confiança vs. acurácia real
