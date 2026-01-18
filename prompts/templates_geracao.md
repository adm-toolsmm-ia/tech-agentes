# Templates de Geração

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18
> **Categoria**: Geração de Conteúdo

---

## Índice de Templates

1. [Geração de Código](#1-geração-de-código)
2. [Geração de Documentação](#2-geração-de-documentação)
3. [Geração de Testes](#3-geração-de-testes)
4. [Geração de Dados](#4-geração-de-dados)
5. [Geração de Comunicação](#5-geração-de-comunicação)

---

## Princípios de Geração

### Configuração por Tipo

| Tipo de Geração | Temperature | Top-p | Notas |
|-----------------|-------------|-------|-------|
| Código | 0.2 - 0.3 | 0.9 | Precisão > criatividade |
| Documentação | 0.3 - 0.5 | 0.95 | Clareza + variação |
| Testes | 0.2 | 0.9 | Cobertura sistemática |
| Dados sintéticos | 0.5 - 0.7 | 0.95 | Diversidade |
| Comunicação | 0.5 - 0.7 | 0.95 | Tom natural |

### Validação Obrigatória

- **Código**: Lint + type check + testes unitários
- **Documentação**: Revisão humana para precisão técnica
- **Testes**: Execução em CI
- **Dados**: Validação de schema + constraints

---

## 1. Geração de Código

### Objetivo
Gerar código funcional, testável e aderente aos padrões do projeto.

### Quando Usar
- Implementação de features
- Refatoração guiada
- Scaffolding de componentes

### Formato de Entrada
```
Requisito/especificação:
[REQUISITO]

Linguagem/framework:
[STACK]

Padrões do projeto:
[PADROES]

Código existente relacionado (opcional):
[CODIGO_EXISTENTE]

Constraints:
[CONSTRAINTS]
```

### Formato de Saída (Schema)
```json
{
  "arquivos": [
    {
      "caminho": "string",
      "conteudo": "string",
      "linguagem": "string",
      "tipo": "implementacao|teste|config|tipo",
      "descricao": "string"
    }
  ],
  "dependencias": {
    "adicionar": ["package@version"],
    "atualizar": ["package@version"],
    "remover": ["package"]
  },
  "instrucoes": {
    "pre_requisitos": ["string"],
    "passos_instalacao": ["string"],
    "como_testar": ["string"],
    "notas": ["string"]
  },
  "decisoes_tecnicas": [
    {
      "decisao": "string",
      "justificativa": "string",
      "alternativas_consideradas": ["string"]
    }
  ]
}
```

### Exemplo (Few-Shot)

**Input**:
```
Requisito: Criar um endpoint REST para listar usuários com paginação

Stack: Python + FastAPI + SQLAlchemy

Padrões:
- Usar Pydantic para validação
- Repository pattern para acesso a dados
- Responses em formato padrão da API

Constraints:
- Máximo 100 itens por página
- Ordenação por created_at desc por padrão
```

**Output**:
```json
{
  "arquivos": [
    {
      "caminho": "app/schemas/user.py",
      "conteudo": "from pydantic import BaseModel, Field\nfrom datetime import datetime\nfrom typing import Optional\n\nclass UserResponse(BaseModel):\n    id: int\n    email: str\n    name: str\n    created_at: datetime\n    \n    class Config:\n        from_attributes = True\n\nclass UserListParams(BaseModel):\n    page: int = Field(default=1, ge=1)\n    page_size: int = Field(default=20, ge=1, le=100)\n    order_by: str = Field(default=\"created_at\")\n    order_dir: str = Field(default=\"desc\", pattern=\"^(asc|desc)$\")",
      "linguagem": "python",
      "tipo": "tipo",
      "descricao": "Schemas Pydantic para request/response de usuários"
    },
    {
      "caminho": "app/repositories/user_repository.py",
      "conteudo": "from sqlalchemy.orm import Session\nfrom sqlalchemy import desc, asc\nfrom app.models.user import User\nfrom app.schemas.user import UserListParams\n\nclass UserRepository:\n    def __init__(self, db: Session):\n        self.db = db\n    \n    def list_users(self, params: UserListParams) -> tuple[list[User], int]:\n        query = self.db.query(User)\n        \n        # Ordenação\n        order_func = desc if params.order_dir == \"desc\" else asc\n        query = query.order_by(order_func(getattr(User, params.order_by)))\n        \n        # Contagem total\n        total = query.count()\n        \n        # Paginação\n        offset = (params.page - 1) * params.page_size\n        users = query.offset(offset).limit(params.page_size).all()\n        \n        return users, total",
      "linguagem": "python",
      "tipo": "implementacao",
      "descricao": "Repository para acesso a dados de usuários"
    },
    {
      "caminho": "app/routers/users.py",
      "conteudo": "from fastapi import APIRouter, Depends, Query\nfrom sqlalchemy.orm import Session\nfrom app.database import get_db\nfrom app.repositories.user_repository import UserRepository\nfrom app.schemas.user import UserResponse, UserListParams\nfrom app.schemas.common import PaginatedResponse\n\nrouter = APIRouter(prefix=\"/users\", tags=[\"users\"])\n\n@router.get(\"\", response_model=PaginatedResponse[UserResponse])\ndef list_users(\n    page: int = Query(default=1, ge=1),\n    page_size: int = Query(default=20, ge=1, le=100),\n    order_by: str = Query(default=\"created_at\"),\n    order_dir: str = Query(default=\"desc\", regex=\"^(asc|desc)$\"),\n    db: Session = Depends(get_db)\n):\n    params = UserListParams(\n        page=page,\n        page_size=page_size,\n        order_by=order_by,\n        order_dir=order_dir\n    )\n    \n    repo = UserRepository(db)\n    users, total = repo.list_users(params)\n    \n    return PaginatedResponse(\n        data=[UserResponse.model_validate(u) for u in users],\n        total=total,\n        page=params.page,\n        page_size=params.page_size,\n        total_pages=(total + params.page_size - 1) // params.page_size\n    )",
      "linguagem": "python",
      "tipo": "implementacao",
      "descricao": "Router FastAPI com endpoint de listagem"
    }
  ],
  "dependencias": {
    "adicionar": [],
    "atualizar": [],
    "remover": []
  },
  "instrucoes": {
    "pre_requisitos": [
      "Model User deve existir em app/models/user.py",
      "Schema PaginatedResponse deve existir em app/schemas/common.py"
    ],
    "passos_instalacao": [
      "Adicionar router em app/main.py: app.include_router(users.router)"
    ],
    "como_testar": [
      "GET /users - lista primeira página",
      "GET /users?page=2&page_size=10 - paginação customizada",
      "GET /users?order_by=name&order_dir=asc - ordenação"
    ],
    "notas": [
      "Considerar adicionar filtros (search, status) em versão futura"
    ]
  },
  "decisoes_tecnicas": [
    {
      "decisao": "Usar Repository Pattern",
      "justificativa": "Seguindo padrão do projeto para separar lógica de acesso a dados",
      "alternativas_consideradas": ["Query direta no router", "Service layer"]
    },
    {
      "decisao": "Validação de page_size no schema",
      "justificativa": "Prevenir queries muito grandes conforme constraint de max 100",
      "alternativas_consideradas": ["Validação apenas no router", "Config global"]
    }
  ]
}
```

### Critérios de Sucesso
- [ ] Código compila/executa sem erros
- [ ] Segue padrões especificados
- [ ] Inclui tratamento de erros básico
- [ ] Documentação inline quando necessário
- [ ] Decisões técnicas justificadas

### Guardrails (Anti-alucinação)
- NÃO usar bibliotecas não especificadas
- NÃO inventar APIs de frameworks
- NÃO assumir estrutura de projeto não informada
- PERGUNTAR quando padrão não estiver claro

---

## 2. Geração de Documentação

### Objetivo
Gerar documentação técnica clara, precisa e útil.

### Quando Usar
- Documentação de APIs
- READMEs de projeto
- Guias de contribuição
- Documentação de arquitetura

### Formato de Entrada
```
Código/sistema a documentar:
[CODIGO]

Tipo de documentação:
[TIPO]

Audiência:
[AUDIENCIA]

Tom/estilo:
[ESTILO]
```

### Formato de Saída (Schema)
```json
{
  "documento": {
    "titulo": "string",
    "tipo": "readme|api|guia|arquitetura|changelog",
    "conteudo_markdown": "string",
    "secoes": [
      {
        "titulo": "string",
        "nivel": 1-6,
        "conteudo": "string"
      }
    ]
  },
  "metadados": {
    "audiencia": "string",
    "nivel_tecnico": "iniciante|intermediario|avancado",
    "tempo_leitura_min": 0,
    "pre_requisitos": ["string"]
  },
  "sugestoes": {
    "melhorias": ["string"],
    "documentos_relacionados": ["string"]
  }
}
```

### Critérios de Sucesso
- [ ] Informações tecnicamente corretas
- [ ] Estrutura clara e navegável
- [ ] Exemplos funcionais incluídos
- [ ] Adequado à audiência especificada

### Guardrails (Anti-alucinação)
- NÃO inventar funcionalidades não presentes
- NÃO documentar comportamentos assumidos
- MARCAR seções que precisam de validação
- BASEAR exemplos em código real

---

## 3. Geração de Testes

### Objetivo
Gerar testes automatizados com boa cobertura e casos relevantes.

### Quando Usar
- TDD: antes da implementação
- Cobertura: após implementação
- Regressão: após bugs

### Formato de Entrada
```
Código a testar:
[CODIGO]

Tipo de testes:
[TIPO]

Framework de testes:
[FRAMEWORK]

Cenários prioritários:
[CENARIOS]
```

### Formato de Saída (Schema)
```json
{
  "arquivos_teste": [
    {
      "caminho": "string",
      "conteudo": "string",
      "framework": "string",
      "tipo": "unit|integration|e2e"
    }
  ],
  "casos_teste": [
    {
      "nome": "string",
      "descricao": "string",
      "tipo": "happy_path|edge_case|error|boundary",
      "prioridade": "alta|media|baixa",
      "input": "string",
      "output_esperado": "string",
      "setup_necessario": "string"
    }
  ],
  "cobertura_estimada": {
    "linhas": "X%",
    "branches": "X%",
    "funcoes": "X%"
  },
  "casos_nao_cobertos": [
    {
      "descricao": "string",
      "motivo": "string",
      "sugestao": "string"
    }
  ]
}
```

### Exemplo (Few-Shot)

**Input**:
```python
# Código a testar
def calculate_discount(price: float, discount_percent: float) -> float:
    if price < 0:
        raise ValueError("Price cannot be negative")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

**Output**:
```json
{
  "arquivos_teste": [
    {
      "caminho": "tests/test_discount.py",
      "conteudo": "import pytest\nfrom app.pricing import calculate_discount\n\nclass TestCalculateDiscount:\n    \"\"\"Testes para função calculate_discount\"\"\"\n    \n    # Happy Path\n    def test_discount_10_percent(self):\n        assert calculate_discount(100, 10) == 90.0\n    \n    def test_discount_50_percent(self):\n        assert calculate_discount(200, 50) == 100.0\n    \n    def test_no_discount(self):\n        assert calculate_discount(100, 0) == 100.0\n    \n    def test_full_discount(self):\n        assert calculate_discount(100, 100) == 0.0\n    \n    # Edge Cases\n    def test_zero_price(self):\n        assert calculate_discount(0, 50) == 0.0\n    \n    def test_decimal_values(self):\n        result = calculate_discount(99.99, 15.5)\n        assert abs(result - 84.49155) < 0.01\n    \n    # Error Cases\n    def test_negative_price_raises_error(self):\n        with pytest.raises(ValueError, match=\"Price cannot be negative\"):\n            calculate_discount(-10, 10)\n    \n    def test_negative_discount_raises_error(self):\n        with pytest.raises(ValueError, match=\"Discount must be between 0 and 100\"):\n            calculate_discount(100, -5)\n    \n    def test_discount_over_100_raises_error(self):\n        with pytest.raises(ValueError, match=\"Discount must be between 0 and 100\"):\n            calculate_discount(100, 150)\n    \n    # Boundary Values\n    def test_discount_at_boundary_0(self):\n        assert calculate_discount(100, 0) == 100.0\n    \n    def test_discount_at_boundary_100(self):\n        assert calculate_discount(100, 100) == 0.0",
      "framework": "pytest",
      "tipo": "unit"
    }
  ],
  "casos_teste": [
    {"nome": "test_discount_10_percent", "descricao": "Desconto padrão de 10%", "tipo": "happy_path", "prioridade": "alta", "input": "price=100, discount=10", "output_esperado": "90.0", "setup_necessario": "nenhum"},
    {"nome": "test_negative_price_raises_error", "descricao": "Preço negativo deve gerar erro", "tipo": "error", "prioridade": "alta", "input": "price=-10, discount=10", "output_esperado": "ValueError", "setup_necessario": "nenhum"}
  ],
  "cobertura_estimada": {
    "linhas": "100%",
    "branches": "100%",
    "funcoes": "100%"
  },
  "casos_nao_cobertos": []
}
```

### Critérios de Sucesso
- [ ] Testes executam sem erro
- [ ] Happy paths cobertos
- [ ] Edge cases identificados
- [ ] Error handling testado
- [ ] Assertions são específicos

### Guardrails (Anti-alucinação)
- NÃO testar comportamentos não implementados
- NÃO assumir retornos não especificados
- BASEAR assertions no código real
- INCLUIR testes negativos/erro

---

## 4. Geração de Dados

### Objetivo
Gerar dados sintéticos realistas para testes, demos ou desenvolvimento.

### Quando Usar
- Seed de banco de dados
- Testes de carga
- Demonstrações
- Treinamento de modelos

### Formato de Entrada
```
Schema dos dados:
[SCHEMA]

Quantidade:
[QUANTIDADE]

Constraints:
[CONSTRAINTS]

Características desejadas:
[CARACTERISTICAS]
```

### Formato de Saída (Schema)
```json
{
  "dados": [{}],
  "schema_utilizado": {},
  "estatisticas": {
    "total_registros": 0,
    "distribuicoes": {},
    "valores_unicos": {}
  },
  "seed": "string",
  "notas": ["string"]
}
```

### Critérios de Sucesso
- [ ] Dados aderem ao schema
- [ ] Constraints respeitadas
- [ ] Distribuição realista
- [ ] Reproduzível via seed

### Guardrails (Anti-alucinação)
- NÃO usar dados reais de pessoas
- NÃO gerar PII válida (CPFs reais, etc.)
- USAR geradores de dados fake
- DOCUMENTAR seed para reprodução

---

## 5. Geração de Comunicação

### Objetivo
Gerar textos de comunicação profissional (emails, mensagens, anúncios).

### Quando Usar
- Comunicação com stakeholders
- Notificações de sistema
- Release notes
- Anúncios internos

### Formato de Entrada
```
Contexto/situação:
[CONTEXTO]

Tipo de comunicação:
[TIPO]

Destinatário:
[DESTINATARIO]

Tom desejado:
[TOM]

Pontos-chave a incluir:
[PONTOS]
```

### Formato de Saída (Schema)
```json
{
  "comunicacao": {
    "tipo": "email|mensagem|anuncio|release_notes",
    "assunto": "string",
    "corpo": "string",
    "tom": "formal|informal|tecnico|executivo",
    "call_to_action": "string"
  },
  "variacoes": [
    {
      "descricao": "string",
      "corpo": "string"
    }
  ],
  "checklist_revisao": [
    {
      "item": "string",
      "status": "ok|revisar"
    }
  ]
}
```

### Critérios de Sucesso
- [ ] Tom adequado à audiência
- [ ] Pontos-chave incluídos
- [ ] Claro e conciso
- [ ] Call-to-action quando aplicável

### Guardrails (Anti-alucinação)
- NÃO inventar fatos/números
- NÃO fazer promessas não autorizadas
- MARCAR seções que precisam de validação
- MANTER tom profissional

---

## Checklist de Qualidade para Geração

### Antes de Entregar

- [ ] Output compila/executa (se código)
- [ ] Segue padrões especificados
- [ ] Não contém placeholder text
- [ ] Decisões técnicas documentadas
- [ ] Warnings/limitações explícitas

### Revisão Humana Recomendada

| Tipo | Nível de Revisão |
|------|------------------|
| Código de produção | Obrigatório |
| Testes | Recomendado |
| Documentação técnica | Obrigatório |
| Dados sintéticos | Amostragem |
| Comunicação externa | Obrigatório |
