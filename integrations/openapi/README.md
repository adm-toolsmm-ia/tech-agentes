# OpenAPI Specifications

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém especificações OpenAPI (Swagger) para as integrações do projeto.

---

## Estrutura

```
openapi/
├── README.md           # Este arquivo
└── [sistema].yaml      # Spec OpenAPI por sistema integrado
```

---

## Como Usar

### 1. Criar Nova Especificação

Para cada nova integração:

1. Criar arquivo `[nome-sistema].yaml` seguindo OpenAPI 3.0+
2. Validar usando ferramentas como `@redocly/cli`
3. Documentar no `integrations/inventario_sistemas.json`

### 2. Validar Especificações

```bash
# Instalar Redocly CLI
npm install -g @redocly/cli

# Validar todas as specs
npx @redocly/cli lint integrations/openapi/*.yaml

# Validar spec específica
npx @redocly/cli lint integrations/openapi/nome-sistema.yaml
```

### 3. Gerar Documentação

```bash
# Gerar HTML interativo
npx @redocly/cli build-docs integrations/openapi/nome-sistema.yaml -o docs/api/nome-sistema.html
```

### 4. Gerar Cliente (Opcional)

```bash
# Usando OpenAPI Generator
openapi-generator-cli generate \
  -i integrations/openapi/nome-sistema.yaml \
  -g python \
  -o src/clients/nome-sistema/
```

---

## Template de Especificação

```yaml
openapi: 3.0.3
info:
  title: Nome do Sistema API
  version: "1.0.0"
  description: Descrição da API
  contact:
    name: Time Responsável
    email: time@empresa.com

servers:
  - url: https://api.exemplo.com/v1
    description: Produção
  - url: https://api-stage.exemplo.com/v1
    description: Staging

security:
  - apiKey: []

paths:
  /recurso:
    get:
      summary: Listar recursos
      operationId: listRecursos
      tags:
        - recursos
      responses:
        "200":
          description: Lista de recursos
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Recurso"
        "401":
          $ref: "#/components/responses/Unauthorized"

components:
  securitySchemes:
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key

  schemas:
    Recurso:
      type: object
      required:
        - id
        - nome
      properties:
        id:
          type: string
          format: uuid
        nome:
          type: string

  responses:
    Unauthorized:
      description: Credenciais inválidas
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Invalid API key"
```

---

## Convenções

### Nomenclatura de Arquivos
- Use kebab-case: `nome-sistema.yaml`
- Inclua versão se múltiplas versões: `nome-sistema-v2.yaml`

### Versionamento
- Versionar a spec junto com a API
- Manter specs antigas para compatibilidade
- Documentar mudanças em CHANGELOG

### Segurança
- NUNCA incluir credenciais reais nas specs
- Usar placeholders ou exemplos genéricos
- Referenciar `configs/ambientes.json` para configuração real

---

## Referências

- [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3)
- [Redocly CLI](https://redocly.com/docs/cli/)
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Especificações de Endpoints](../specs_endpoints.md)
- [Inventário de Sistemas](../inventario_sistemas.json)
