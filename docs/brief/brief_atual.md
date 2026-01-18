# Brief do Projeto

> **Template padrão tech-agentes** — Preencha conforme o contexto do projeto.
> **Versão**: 1.0.0 | **Última atualização**: [DATA]

---

## 1. Identificação

| Campo | Valor |
|-------|-------|
| **Nome do Projeto** | [Nome] |
| **Código/ID** | [ID interno] |
| **Tenant** | [ID do tenant se multi-tenant] |
| **Owner** | [Responsável técnico] |
| **Stakeholders** | [Lista de interessados] |
| **Data de Início** | [YYYY-MM-DD] |
| **Deadline** | [YYYY-MM-DD ou "Sem prazo definido"] |

---

## 2. Contexto e Problema

### 2.1 Situação Atual
> Descreva o estado atual, dores e limitações.

[Descrever aqui]

### 2.2 Problema a Resolver
> Qual problema específico este projeto resolve?

[Descrever aqui]

### 2.3 Impacto do Problema
> Quantifique o impacto (tempo perdido, custo, risco, etc.)

| Métrica | Valor Atual | Meta |
|---------|-------------|------|
| [Métrica 1] | [Valor] | [Meta] |
| [Métrica 2] | [Valor] | [Meta] |

---

## 3. Objetivos e Escopo

### 3.1 Objetivo Principal
> Uma frase clara do que o projeto entrega.

[Objetivo]

### 3.2 Objetivos Secundários
- [ ] [Objetivo 2]
- [ ] [Objetivo 3]

### 3.3 Escopo Incluído
- [Item incluído 1]
- [Item incluído 2]

### 3.4 Escopo Excluído (Out of Scope)
- [Item excluído 1]
- [Item excluído 2]

---

## 4. Requisitos

### 4.1 Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|------------|-------------------|
| RF01 | [Descrição] | Must/Should/Could | [Como validar] |
| RF02 | [Descrição] | Must/Should/Could | [Como validar] |

### 4.2 Requisitos Não-Funcionais

| ID | Requisito | Métrica | Target |
|----|-----------|---------|--------|
| RNF01 | Performance | Latência P95 | < 500ms |
| RNF02 | Disponibilidade | Uptime | 99.9% |
| RNF03 | Segurança | [Métrica] | [Target] |

### 4.3 Restrições

| Tipo | Restrição | Impacto |
|------|-----------|---------|
| Técnica | [Ex: Deve usar Python 3.11+] | [Impacto] |
| Negócio | [Ex: Budget máximo R$ X] | [Impacto] |
| Prazo | [Ex: Go-live até data X] | [Impacto] |

---

## 5. KPIs e Métricas de Sucesso

### 5.1 KPIs Principais

| KPI | Baseline | Meta | Prazo |
|-----|----------|------|-------|
| [KPI 1] | [Valor atual] | [Meta] | [Data] |
| [KPI 2] | [Valor atual] | [Meta] | [Data] |

### 5.2 Critérios de Aceite do Projeto

```markdown
## Critérios de Aceite (Definition of Done)

- [ ] Todos os requisitos "Must" implementados
- [ ] Testes passando (cobertura mínima: X%)
- [ ] Documentação atualizada
- [ ] Code review aprovado
- [ ] Deploy em staging validado
- [ ] Aprovação do stakeholder principal
```

---

## 6. Dados e Integrações

### 6.1 Fontes de Dados

| Sistema | Tipo | Dados | Frequência | Owner |
|---------|------|-------|------------|-------|
| [Sistema 1] | API/DB/File | [Descrição] | Real-time/Batch | [Owner] |

### 6.2 Integrações Necessárias

| Sistema | Direção | Protocolo | Status |
|---------|---------|-----------|--------|
| [Sistema 1] | IN/OUT/BOTH | REST/GraphQL/Webhook | A definir |

### 6.3 Classificação de Dados

| Dado | Classificação | Controles Necessários |
|------|---------------|----------------------|
| [Dado 1] | PII/Sensível/Interno/Público | [Controles] |

> Referência: `docs/seguranca/politicas.md`

---

## 7. Arquitetura e Tecnologia

### 7.1 Stack Tecnológico

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Backend | [Ex: Python + FastAPI] | [Razão] |
| Frontend | [Ex: React + TypeScript] | [Razão] |
| Database | [Ex: PostgreSQL] | [Razão] |
| Infra | [Ex: AWS/GCP/Azure] | [Razão] |
| AI/LLM | [Ex: GPT-4o, Claude] | [Razão] |

### 7.2 Decisões Arquiteturais

> Listar ADRs relevantes ou decisões pendentes.

- ADR-XXX: [Título] — [Status: Aprovado/Pendente]

---

## 8. Riscos e Dependências

### 8.1 Riscos Identificados

| ID | Risco | Probabilidade | Impacto | Mitigação |
|----|-------|---------------|---------|-----------|
| R01 | [Descrição] | Alta/Média/Baixa | Alto/Médio/Baixo | [Ação] |

### 8.2 Dependências

| Dependência | Tipo | Status | Responsável |
|-------------|------|--------|-------------|
| [Dep 1] | Técnica/Negócio/Externa | Resolvida/Pendente | [Nome] |

---

## 9. Cronograma e Milestones

### 9.1 Fases do Projeto

| Fase | Início | Fim | Entregáveis |
|------|--------|-----|-------------|
| Discovery | [Data] | [Data] | Brief aprovado |
| MVP | [Data] | [Data] | Funcionalidades core |
| Beta | [Data] | [Data] | Versão testada |
| Go-Live | [Data] | [Data] | Produção |

### 9.2 Milestones Críticos

- [ ] **M1** [Data]: [Entregável]
- [ ] **M2** [Data]: [Entregável]
- [ ] **M3** [Data]: [Entregável]

---

## 10. Time e Responsabilidades

| Papel | Nome | Responsabilidades |
|-------|------|-------------------|
| Product Owner | [Nome] | Priorização, aceite |
| Tech Lead | [Nome] | Arquitetura, decisões técnicas |
| Desenvolvedor | [Nome] | Implementação |
| QA | [Nome] | Testes, qualidade |
| DevOps | [Nome] | Infra, deploy |

---

## 11. Perguntas Abertas

> Lista de questões que precisam ser respondidas antes de avançar.

| ID | Pergunta | Responsável | Prazo | Status |
|----|----------|-------------|-------|--------|
| Q01 | [Pergunta] | [Nome] | [Data] | Aberta/Respondida |

---

## 12. Anexos e Referências

- [Link para documentos complementares]
- [Link para Figma/protótipos]
- [Link para specs técnicas]

---

## Histórico de Atualizações

| Data | Autor | Mudança |
|------|-------|---------|
| [Data] | [Nome] | Criação inicial |
