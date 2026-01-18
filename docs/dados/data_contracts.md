# Data Contracts

> **Template padrão tech-agentes** — Contratos de dados para integrações e ETL.
> **Versão**: 1.0.0 | **Última atualização**: [DATA]

---

## 1. Visão Geral

Este documento define os contratos de dados do projeto, garantindo:
- **Clareza**: Estrutura e tipos bem definidos
- **Consistência**: Padrões uniformes entre sistemas
- **Rastreabilidade**: Origem e transformações documentadas
- **Compliance**: Classificação de dados para LGPD

---

## 2. Padrão de Contrato

### 2.1 Estrutura Obrigatória

Cada contrato de dados deve conter:

```yaml
contract:
  name: string          # Nome único do contrato
  version: semver       # Versão semântica (1.0.0)
  owner: string         # Time/pessoa responsável
  description: string   # Descrição do propósito

source:
  system: string        # Sistema de origem
  entity: string        # Entidade/tabela de origem
  frequency: string     # real-time | hourly | daily | on-demand

target:
  system: string        # Sistema de destino
  entity: string        # Entidade/tabela de destino

schema:
  fields: []            # Lista de campos (ver 2.2)

quality:
  rules: []             # Regras de validação
  sla: object           # SLAs de qualidade

metadata:
  classification: string # PII | sensitive | internal | public
  retention: string      # Política de retenção
  created_at: datetime
  updated_at: datetime
```

### 2.2 Definição de Campos

```yaml
fields:
  - name: string              # Nome do campo
    type: string              # Tipo de dado (string, int, float, bool, datetime, json)
    required: boolean         # Obrigatório?
    nullable: boolean         # Aceita null?
    description: string       # Descrição do campo
    classification: string    # PII | sensitive | internal | public
    transform: string         # Transformação aplicada (se houver)
    validation: string        # Regex ou regra de validação
    example: any              # Exemplo de valor
```

---

## 3. Contratos do Projeto

### 3.1 [Nome do Contrato 1]

```yaml
contract:
  name: "exemplo-contato-crm"
  version: "1.0.0"
  owner: "time-dados"
  description: "Sincronização de contatos do CRM para Data Warehouse"

source:
  system: "crm-salesforce"
  entity: "Contact"
  frequency: "hourly"

target:
  system: "data-warehouse"
  entity: "dim_contacts"

schema:
  fields:
    - name: id
      type: string
      required: true
      nullable: false
      description: "ID único do contato no CRM"
      classification: internal
      example: "003xx000004TmiUAAS"

    - name: email
      type: string
      required: true
      nullable: false
      description: "Email do contato"
      classification: PII
      transform: "lowercase(trim(value))"
      validation: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
      example: "contato@empresa.com"

    - name: name
      type: string
      required: true
      nullable: false
      description: "Nome completo do contato"
      classification: PII
      transform: "trim(value)"
      example: "João Silva"

    - name: created_at
      type: datetime
      required: true
      nullable: false
      description: "Data de criação do registro"
      classification: internal
      transform: "to_utc(value)"
      example: "2026-01-18T10:30:00Z"

quality:
  rules:
    - name: "email_unique"
      type: "uniqueness"
      field: "email"
      threshold: 1.0

    - name: "email_valid"
      type: "regex"
      field: "email"
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
      threshold: 0.99

    - name: "name_not_empty"
      type: "not_null"
      field: "name"
      threshold: 1.0

  sla:
    freshness_hours: 2
    completeness_percent: 99
    accuracy_percent: 99

metadata:
  classification: PII
  retention: "5 years"
  created_at: "2026-01-18T00:00:00Z"
  updated_at: "2026-01-18T00:00:00Z"
```

### 3.2 [Nome do Contrato 2]

> Adicionar mais contratos conforme necessidade do projeto.

```yaml
contract:
  name: "[nome-do-contrato]"
  version: "1.0.0"
  owner: "[owner]"
  description: "[descrição]"
  # ... completar conforme template
```

---

## 4. Transformações Padrão

### 4.1 Funções de Transformação

| Função | Descrição | Exemplo |
|--------|-----------|---------|
| `trim(value)` | Remove espaços | " texto " → "texto" |
| `lowercase(value)` | Converte para minúsculas | "TEXTO" → "texto" |
| `uppercase(value)` | Converte para maiúsculas | "texto" → "TEXTO" |
| `to_utc(value)` | Converte para UTC | "2026-01-18T10:00:00-03:00" → "2026-01-18T13:00:00Z" |
| `mask_pii(value)` | Mascara PII | "joao@email.com" → "j***@e***.com" |
| `hash_sha256(value)` | Hash SHA256 | "texto" → "hash..." |
| `default(value, default)` | Valor padrão se null | null → "N/A" |

### 4.2 Composição de Transformações

```yaml
transform: "lowercase(trim(value))"  # Aplicado em ordem: trim primeiro, depois lowercase
```

---

## 5. Regras de Qualidade

### 5.1 Tipos de Validação

| Tipo | Descrição | Parâmetros |
|------|-----------|------------|
| `not_null` | Campo não pode ser null | threshold |
| `uniqueness` | Valores únicos | threshold |
| `regex` | Valida contra regex | pattern, threshold |
| `range` | Valor dentro de range | min, max, threshold |
| `enum` | Valor em lista permitida | values, threshold |
| `referential` | Referência existe | target_system, target_field |

### 5.2 Thresholds

- **1.0 (100%)**: Regra deve passar em todos os registros
- **0.99 (99%)**: Tolera até 1% de falhas
- **0.95 (95%)**: Tolera até 5% de falhas

---

## 6. Classificação de Dados (LGPD)

### 6.1 Categorias

| Classificação | Descrição | Controles Obrigatórios |
|---------------|-----------|------------------------|
| **PII** | Identifica pessoa física | Criptografia, acesso restrito, logs |
| **sensitive** | Dados confidenciais de negócio | Acesso restrito, logs |
| **internal** | Dados operacionais | Autenticação |
| **public** | Dados públicos | Nenhum |

### 6.2 Tratamento por Classificação

```yaml
# PII - Tratamento obrigatório
- Criptografia em repouso (AES-256)
- Criptografia em trânsito (TLS 1.3)
- Mascaramento em logs
- Acesso auditado
- Retenção conforme LGPD

# Sensitive - Tratamento recomendado
- Criptografia em trânsito
- Acesso restrito por papel
- Logs de acesso
```

---

## 7. Versionamento de Contratos

### 7.1 Política de Versão

- **MAJOR (X.0.0)**: Breaking changes (remoção de campos, mudança de tipo)
- **MINOR (0.X.0)**: Novos campos opcionais, novas transformações
- **PATCH (0.0.X)**: Correções de documentação, ajustes de threshold

### 7.2 Compatibilidade

| Mudança | Compatível? | Ação Necessária |
|---------|-------------|-----------------|
| Adicionar campo opcional | ✅ Sim | MINOR bump |
| Adicionar campo obrigatório | ❌ Não | MAJOR bump + migração |
| Remover campo | ❌ Não | MAJOR bump + depreciação |
| Mudar tipo de campo | ❌ Não | MAJOR bump + migração |
| Mudar transformação | ⚠️ Depende | Avaliar impacto |

### 7.3 Processo de Mudança

1. Propor mudança em ADR
2. Avaliar impacto nos consumidores
3. Comunicar stakeholders
4. Implementar com período de transição
5. Depreciar versão anterior

---

## 8. SLAs de Dados

### 8.1 Métricas Padrão

| Métrica | Descrição | Target Padrão |
|---------|-----------|---------------|
| **Freshness** | Atraso máximo dos dados | < 2 horas |
| **Completeness** | % de registros completos | > 99% |
| **Accuracy** | % de dados corretos | > 99% |
| **Availability** | Uptime do pipeline | > 99.5% |

### 8.2 Alertas

```yaml
alerts:
  - name: "freshness_breach"
    condition: "freshness_hours > sla.freshness_hours"
    severity: "high"
    notify: ["data-team@empresa.com"]

  - name: "quality_degradation"
    condition: "completeness_percent < 95"
    severity: "critical"
    notify: ["data-team@empresa.com", "cto@empresa.com"]
```

---

## 9. Registro de Contratos

### 9.1 Inventário

| Contrato | Versão | Source | Target | Classificação | Status |
|----------|--------|--------|--------|---------------|--------|
| exemplo-contato-crm | 1.0.0 | CRM | DW | PII | Ativo |
| [outro-contrato] | [versão] | [source] | [target] | [class] | [status] |

### 9.2 Dependências

```mermaid
graph LR
    CRM[CRM Salesforce] -->|exemplo-contato-crm| DW[Data Warehouse]
    DW -->|relatorio-vendas| BI[BI Dashboard]
    ERP[ERP] -->|pedidos| DW
```

---

## Histórico de Atualizações

| Data | Autor | Mudança |
|------|-------|---------|
| [Data] | [Nome] | Criação inicial |
