# KPIs e Requisitos de Negócio

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18
> **Responsável**: CTO / Product Owner

---

## Visão Geral

Este diretório contém definições de KPIs de negócio e requisitos de projeto. Diferentemente de `observability/` (métricas técnicas), aqui documentamos indicadores de sucesso do ponto de vista de negócio.

---

## 1. Propósito

| Diretório | Foco | Exemplos |
|-----------|------|----------|
| `dashboards/` | KPIs de Negócio | ROI, adoção, satisfação, conversão |
| `observability/` | Métricas Técnicas | Latência, tokens, custos, error rate |

---

## 2. Framework de KPIs

### 2.1 Categorias de KPIs

| Categoria | Descrição | Frequência de Medição |
|-----------|-----------|----------------------|
| **Eficiência** | Redução de tempo/custo em processos | Semanal |
| **Qualidade** | Precisão e confiabilidade dos outputs | Por release |
| **Adoção** | Uso efetivo pelos times | Mensal |
| **Impacto** | Valor gerado para o negócio | Trimestral |

### 2.2 Template de KPI

```yaml
kpi:
  id: KPI-001
  nome: "Nome descritivo do KPI"
  categoria: "eficiencia|qualidade|adocao|impacto"
  definicao: "O que este KPI mede"
  formula: "Como calcular"
  unidade: "%, horas, R$, etc."
  baseline: "Valor inicial/anterior"
  meta: "Valor alvo"
  prazo: "Quando atingir a meta"
  fonte_dados: "De onde vêm os dados"
  responsavel: "Quem acompanha"
  frequencia: "Quando medir"
```

---

## 3. KPIs do Framework Tech-Agentes

### 3.1 Eficiência

| ID | KPI | Baseline | Meta | Status |
|----|-----|----------|------|--------|
| KPI-E01 | Tempo médio de setup de projeto | 4h | 30min | 🟡 Em progresso |
| KPI-E02 | Redução de código boilerplate | 0% | 80% | 🟢 Atingido |
| KPI-E03 | Tempo de onboarding de devs | 2 dias | 4h | 🟡 Em progresso |

### 3.2 Qualidade

| ID | KPI | Baseline | Meta | Status |
|----|-----|----------|------|--------|
| KPI-Q01 | Taxa de conformidade com padrões | 40% | 95% | 🟡 Em progresso |
| KPI-Q02 | Pass rate de golden sets | - | 95% | 🟢 Atingido |
| KPI-Q03 | Cobertura de documentação | 30% | 90% | 🟢 Atingido |

### 3.3 Adoção

| ID | KPI | Baseline | Meta | Status |
|----|-----|----------|------|--------|
| KPI-A01 | Projetos usando o framework | 0 | 5 | 🔴 Pendente |
| KPI-A02 | Satisfação dos desenvolvedores | - | 4.5/5 | 🔴 Pendente |
| KPI-A03 | % de projetos novos usando padrão | 0% | 100% | 🔴 Pendente |

### 3.4 Impacto

| ID | KPI | Baseline | Meta | Status |
|----|-----|----------|------|--------|
| KPI-I01 | ROI do framework | - | 5x | 🔴 Pendente |
| KPI-I02 | Redução de incidentes em prod | - | 50% | 🔴 Pendente |
| KPI-I03 | Tempo de go-live de projetos | 3 meses | 1 mês | 🔴 Pendente |

---

## 4. Detalhamento de KPIs Prioritários

### KPI-E01: Tempo de Setup de Projeto

```yaml
id: KPI-E01
nome: "Tempo médio de setup de projeto"
categoria: eficiencia
definicao: >
  Tempo desde o início de um novo projeto até ter estrutura
  básica funcionando (configs, docs, pipeline CI).
formula: "média(tempo_setup_projetos_novos)"
unidade: "minutos"
baseline: 240  # 4 horas
meta: 30  # 30 minutos
prazo: "2026-Q1"
fonte_dados: "Logs do CLI tech-agents init"
responsavel: "DevOps Lead"
frequencia: "Por projeto"
como_medir:
  - "Executar `tech-agents init` em projeto novo"
  - "Registrar tempo até validação passar"
  - "Incluir tempo de ajustes manuais"
```

### KPI-Q01: Taxa de Conformidade

```yaml
id: KPI-Q01
nome: "Taxa de conformidade com padrões"
categoria: qualidade
definicao: >
  Percentual de projetos que passam validação completa
  do framework sem erros críticos.
formula: "(projetos_validos / total_projetos) * 100"
unidade: "%"
baseline: 40
meta: 95
prazo: "2026-Q2"
fonte_dados: "Resultado de `tech-agents validate`"
responsavel: "QA Lead"
frequencia: "Semanal"
como_medir:
  - "Executar validação em todos os projetos ativos"
  - "Registrar erros por categoria"
  - "Calcular % de projetos sem erros críticos"
```

---

## 5. Dashboard de Acompanhamento

### 5.1 Visão Executiva

```
┌─────────────────────────────────────────────────────────────────┐
│                    KPIs - Tech-Agentes                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EFICIÊNCIA          QUALIDADE           ADOÇÃO                │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐          │
│  │  30min  │         │   95%   │         │ 0 proj  │          │
│  │ setup   │         │ conform │         │ usando  │          │
│  │ ▼ 87%   │         │ ▲ 55pp  │         │ meta: 5 │          │
│  └─────────┘         └─────────┘         └─────────┘          │
│                                                                 │
│  IMPACTO                                                        │
│  ┌─────────────────────────────────────────────┐              │
│  │  ROI: Pendente medição após adoção          │              │
│  └─────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Relatórios Periódicos

| Relatório | Frequência | Destinatários | Conteúdo |
|-----------|------------|---------------|----------|
| Semanal | Segundas | Tech Leads | Métricas técnicas + KPIs E/Q |
| Mensal | Dia 1 | CTO + PMs | Todos os KPIs + tendências |
| Trimestral | Fim Q | Diretoria | Impacto + ROI + roadmap |

---

## 6. Coleta de Dados

### 6.1 Fontes Automatizadas

| KPI | Fonte | Automação |
|-----|-------|-----------|
| Tempo de setup | CLI logs | `tech-agents` telemetria |
| Conformidade | Validação | `tech-agents validate` |
| Uso de modelos | Observability | Langfuse/Helicone |

### 6.2 Fontes Manuais

| KPI | Fonte | Responsável |
|-----|-------|-------------|
| Satisfação | Surveys | Product Owner |
| ROI | Cálculo financeiro | Finance + CTO |
| Incidentes | Incident tracker | DevOps |

---

## 7. Integração com Observability

Para métricas técnicas que alimentam KPIs de negócio:

```
dashboards/requisitos_kpis.md          observability/dashboards.json
         │                                       │
         │   KPI-E01 ◄───────────────── llm_request_duration
         │   KPI-Q01 ◄───────────────── eval_golden_set_pass_rate
         │   KPI-I02 ◄───────────────── error_rate
         │                                       │
         ▼                                       ▼
    [Relatório Executivo]                [Dashboard Técnico]
```

---

## Referências

- [Observabilidade Técnica](../observability/README.md)
- [Dashboards JSON](../observability/dashboards.json)
- [Relatórios Periódicos](../observability/relatorios_periodicos.md)
- [Padrões do Projeto](../docs/padrões/padroes_projeto.md)

---

## Histórico

| Data | Autor | Mudança |
|------|-------|---------|
| 2026-01-18 | CTO | Criação inicial com KPIs base |
