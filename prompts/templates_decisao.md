# Templates de Decisão

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18
> **Categoria**: Suporte a Decisões

---

## Índice de Templates

1. [Decisão Técnica (ADR)](#1-decisão-técnica-adr)
2. [Decisão de Negócio](#2-decisão-de-negócio)
3. [Priorização](#3-priorização)
4. [Trade-off Analysis](#4-trade-off-analysis)
5. [Go/No-Go](#5-gono-go)

---

## Princípios de Decisão

### Framework de Decisão

```
1. DEFINIR: Qual decisão precisa ser tomada?
2. COLETAR: Quais dados/contexto são necessários?
3. ANALISAR: Quais são as opções e trade-offs?
4. DECIDIR: Qual opção escolher e por quê?
5. DOCUMENTAR: Como registrar para futuro?
6. COMUNICAR: Quem precisa saber?
```

### Níveis de Decisão

| Nível | Impacto | Reversibilidade | Aprovadores |
|-------|---------|-----------------|-------------|
| **Operacional** | Baixo | Alta | Auto-aprovado |
| **Tático** | Médio | Média | Tech Lead |
| **Estratégico** | Alto | Baixa | CTO + Stakeholders |

---

## 1. Decisão Técnica (ADR)

### Objetivo
Documentar decisões arquiteturais/técnicas significativas de forma estruturada.

### Quando Usar
- Escolha de tecnologia/framework
- Mudança de arquitetura
- Definição de padrões
- Decisões com impacto em múltiplos sistemas

### Formato de Entrada
```
Contexto do problema:
[CONTEXTO]

Opções consideradas:
[OPCOES]

Critérios de decisão:
[CRITERIOS]

Constraints conhecidos:
[CONSTRAINTS]
```

### Formato de Saída (Schema)
```json
{
  "adr": {
    "id": "ADR-YYYYMMDD-XXX",
    "titulo": "string",
    "status": "proposta|aceita|depreciada|substituida",
    "data": "YYYY-MM-DD",
    "decisores": ["string"],
    "contexto": "string",
    "problema": "string",
    "opcoes": [
      {
        "nome": "string",
        "descricao": "string",
        "pros": ["string"],
        "cons": ["string"],
        "riscos": ["string"],
        "custo_estimado": "string",
        "esforco": "P|M|G"
      }
    ],
    "decisao": {
      "opcao_escolhida": "string",
      "justificativa": "string",
      "criterios_decisivos": ["string"]
    },
    "consequencias": {
      "positivas": ["string"],
      "negativas": ["string"],
      "neutras": ["string"]
    },
    "plano_implementacao": {
      "passos": ["string"],
      "timeline": "string",
      "responsaveis": ["string"]
    },
    "metricas_sucesso": ["string"],
    "revisao": {
      "data_revisao": "YYYY-MM-DD",
      "criterios_revisao": ["string"]
    },
    "relacionados": ["ADR-XXX"]
  }
}
```

### Exemplo (Few-Shot)

**Input**:
```
Contexto: Sistema de e-commerce precisa de solução de cache para reduzir
latência de consultas de catálogo. Atualmente 500ms P95, objetivo 100ms.

Opções: Redis, Memcached, Cache em memória local

Critérios: Performance, complexidade operacional, custo, consistência

Constraints: Time de 2 devs, budget limitado, deploy em Kubernetes
```

**Output**:
```json
{
  "adr": {
    "id": "ADR-20260118-001",
    "titulo": "Solução de Cache para Catálogo de Produtos",
    "status": "proposta",
    "data": "2026-01-18",
    "decisores": ["CTO", "Tech Lead"],
    "contexto": "O sistema de e-commerce apresenta latência elevada (500ms P95) nas consultas ao catálogo de produtos, impactando experiência do usuário e conversão. Objetivo é reduzir para 100ms P95.",
    "problema": "Qual solução de cache adotar para reduzir latência de consultas ao catálogo mantendo consistência aceitável e operação simples?",
    "opcoes": [
      {
        "nome": "Redis",
        "descricao": "Cache distribuído in-memory com persistência opcional",
        "pros": [
          "Alta performance (sub-ms latency)",
          "Estruturas de dados ricas",
          "Suporte a cluster nativo",
          "Ampla adoção e documentação",
          "Helm charts maduros para K8s"
        ],
        "cons": [
          "Complexidade operacional média",
          "Custo de infraestrutura",
          "Requer gestão de memória"
        ],
        "riscos": [
          "Single point of failure sem cluster",
          "Eviction pode causar cache miss storms"
        ],
        "custo_estimado": "$50-100/mês (managed) ou $30/mês (self-hosted)",
        "esforco": "M"
      },
      {
        "nome": "Memcached",
        "descricao": "Cache distribuído simples key-value",
        "pros": [
          "Extremamente simples",
          "Muito rápido para casos simples",
          "Menor footprint de memória"
        ],
        "cons": [
          "Sem persistência",
          "Apenas strings como valor",
          "Menos features que Redis"
        ],
        "riscos": [
          "Limitações futuras de funcionalidade"
        ],
        "custo_estimado": "$30-50/mês",
        "esforco": "P"
      },
      {
        "nome": "Cache em memória local",
        "descricao": "Cache no processo da aplicação (e.g., lru-cache)",
        "pros": [
          "Zero latência de rede",
          "Sem infraestrutura adicional",
          "Simples de implementar"
        ],
        "cons": [
          "Não compartilhado entre instâncias",
          "Inconsistência entre pods",
          "Duplicação de memória"
        ],
        "riscos": [
          "Dados stale em múltiplas instâncias",
          "Memory pressure na aplicação"
        ],
        "custo_estimado": "$0 (incluso na aplicação)",
        "esforco": "P"
      }
    ],
    "decisao": {
      "opcao_escolhida": "Redis",
      "justificativa": "Redis oferece o melhor equilíbrio entre performance, funcionalidades e maturidade operacional. Estruturas de dados como sorted sets serão úteis para rankings e TTL granular. Deploy em K8s é bem suportado.",
      "criterios_decisivos": [
        "Performance atende objetivo de 100ms com margem",
        "Suporte nativo a K8s via Helm",
        "Flexibilidade para casos de uso futuros",
        "Documentação e comunidade robustas"
      ]
    },
    "consequencias": {
      "positivas": [
        "Redução de latência P95 de 500ms para ~50ms esperado",
        "Base para futuros casos de uso (sessions, rate limiting)",
        "Time aprende tecnologia amplamente adotada"
      ],
      "negativas": [
        "Custo adicional de infraestrutura (~$50/mês)",
        "Complexidade operacional adicionada",
        "Necessidade de estratégia de invalidação"
      ],
      "neutras": [
        "Requer definição de TTLs por tipo de dado",
        "Monitoramento adicional necessário"
      ]
    },
    "plano_implementacao": {
      "passos": [
        "1. Deploy Redis via Helm em ambiente dev (2d)",
        "2. Implementar cache layer na aplicação (3d)",
        "3. Definir TTLs e estratégia de invalidação (1d)",
        "4. Testes de carga e ajustes (2d)",
        "5. Deploy em produção com feature flag (1d)",
        "6. Monitoramento e ajuste fino (ongoing)"
      ],
      "timeline": "2 semanas",
      "responsaveis": ["Dev Backend", "DevOps"]
    },
    "metricas_sucesso": [
      "Latência P95 < 100ms em 30 dias",
      "Cache hit rate > 90%",
      "Zero downtime relacionado ao cache em 90 dias"
    ],
    "revisao": {
      "data_revisao": "2026-04-18",
      "criterios_revisao": [
        "Métricas de sucesso atingidas?",
        "Custos dentro do esperado?",
        "Complexidade operacional aceitável?"
      ]
    },
    "relacionados": []
  }
}
```

### Critérios de Sucesso
- [ ] Problema claramente definido
- [ ] Opções viáveis analisadas
- [ ] Trade-offs explícitos
- [ ] Decisão justificada com critérios
- [ ] Consequências mapeadas
- [ ] Métricas de sucesso definidas

### Guardrails (Anti-alucinação)
- NÃO inventar métricas de performance
- NÃO assumir custos sem pesquisa
- BASEAR análise em dados/experiência real
- DECLARAR incertezas explicitamente

---

## 2. Decisão de Negócio

### Objetivo
Estruturar decisões de negócio com análise de impacto e stakeholders.

### Quando Usar
- Mudanças de produto
- Alocação de recursos
- Parcerias e contratos
- Mudanças de processo

### Formato de Entrada
```
Decisão a ser tomada:
[DECISAO]

Contexto de negócio:
[CONTEXTO]

Stakeholders:
[STAKEHOLDERS]

Dados disponíveis:
[DADOS]
```

### Formato de Saída (Schema)
```json
{
  "decisao_negocio": {
    "titulo": "string",
    "tipo": "produto|recurso|parceria|processo|investimento",
    "urgencia": "alta|media|baixa",
    "reversibilidade": "alta|media|baixa",
    "contexto": "string",
    "problema_oportunidade": "string",
    "opcoes": [
      {
        "nome": "string",
        "descricao": "string",
        "impacto_financeiro": {
          "investimento": "string",
          "retorno_esperado": "string",
          "payback": "string"
        },
        "impacto_operacional": "string",
        "impacto_clientes": "string",
        "riscos": ["string"]
      }
    ],
    "analise_stakeholders": [
      {
        "stakeholder": "string",
        "interesse": "string",
        "influencia": "alta|media|baixa",
        "posicao_esperada": "favoravel|neutro|contrario"
      }
    ],
    "recomendacao": {
      "opcao": "string",
      "justificativa": "string",
      "condicoes": ["string"],
      "proximos_passos": ["string"]
    }
  }
}
```

### Critérios de Sucesso
- [ ] Impacto financeiro estimado
- [ ] Stakeholders mapeados
- [ ] Riscos de negócio identificados
- [ ] Recomendação clara

### Guardrails (Anti-alucinação)
- NÃO inventar números financeiros
- NÃO assumir posição de stakeholders
- BASEAR em dados disponíveis
- SINALIZAR quando dados insuficientes

---

## 3. Priorização

### Objetivo
Ordenar itens (features, bugs, projetos) por prioridade objetiva.

### Quando Usar
- Planejamento de sprint
- Roadmap de produto
- Alocação de recursos
- Triage de bugs

### Formato de Entrada
```
Itens a priorizar:
[ITENS]

Critérios de priorização:
[CRITERIOS]

Recursos disponíveis:
[RECURSOS]

Contexto estratégico:
[CONTEXTO]
```

### Formato de Saída (Schema)
```json
{
  "priorizacao": {
    "metodo": "RICE|MoSCoW|WSJF|ICE|Custom",
    "criterios": [
      {
        "nome": "string",
        "peso": 1-10,
        "descricao": "string"
      }
    ],
    "itens": [
      {
        "id": "string",
        "nome": "string",
        "scores": {
          "criterio1": 0-10,
          "criterio2": 0-10
        },
        "score_final": 0-100,
        "justificativa": "string"
      }
    ],
    "ranking": [
      {
        "posicao": 1,
        "item_id": "string",
        "score": 0-100,
        "recomendacao": "fazer_agora|proximo_ciclo|backlog|descartar"
      }
    ],
    "corte_sugerido": {
      "fazer_agora": ["item_id"],
      "proximo_ciclo": ["item_id"],
      "backlog": ["item_id"]
    }
  }
}
```

### Exemplo (Few-Shot) - Método RICE

**Input**:
```
Itens:
1. Dark mode no app
2. Integração com Slack
3. Export para Excel
4. SSO com Google

Critérios: RICE (Reach, Impact, Confidence, Effort)
Contexto: SaaS B2B, 500 clientes, Q1 planning
```

**Output**:
```json
{
  "priorizacao": {
    "metodo": "RICE",
    "criterios": [
      {"nome": "reach", "peso": 1, "descricao": "% de clientes impactados/trimestre"},
      {"nome": "impact", "peso": 1, "descricao": "Impacto por cliente (0.25-3)"},
      {"nome": "confidence", "peso": 1, "descricao": "Confiança nas estimativas (%)"},
      {"nome": "effort", "peso": 1, "descricao": "Pessoa-semanas de esforço"}
    ],
    "itens": [
      {
        "id": "sso-google",
        "nome": "SSO com Google",
        "scores": {"reach": 80, "impact": 2, "confidence": 90, "effort": 3},
        "score_final": 48,
        "justificativa": "Alta demanda de clientes enterprise, esforço moderado, alto impacto em conversão"
      },
      {
        "id": "slack-integration",
        "nome": "Integração com Slack",
        "scores": {"reach": 60, "impact": 1.5, "confidence": 80, "effort": 4},
        "score_final": 18,
        "justificativa": "Demanda consistente, melhora workflow, esforço médio"
      },
      {
        "id": "excel-export",
        "nome": "Export para Excel",
        "scores": {"reach": 40, "impact": 1, "confidence": 95, "effort": 1},
        "score_final": 38,
        "justificativa": "Baixo esforço, atende necessidade pontual, alta confiança"
      },
      {
        "id": "dark-mode",
        "nome": "Dark mode",
        "scores": {"reach": 30, "impact": 0.5, "confidence": 90, "effort": 2},
        "score_final": 6.75,
        "justificativa": "Nice-to-have, baixo impacto em métricas de negócio"
      }
    ],
    "ranking": [
      {"posicao": 1, "item_id": "sso-google", "score": 48, "recomendacao": "fazer_agora"},
      {"posicao": 2, "item_id": "excel-export", "score": 38, "recomendacao": "fazer_agora"},
      {"posicao": 3, "item_id": "slack-integration", "score": 18, "recomendacao": "proximo_ciclo"},
      {"posicao": 4, "item_id": "dark-mode", "score": 6.75, "recomendacao": "backlog"}
    ],
    "corte_sugerido": {
      "fazer_agora": ["sso-google", "excel-export"],
      "proximo_ciclo": ["slack-integration"],
      "backlog": ["dark-mode"]
    }
  }
}
```

### Critérios de Sucesso
- [ ] Método de priorização explícito
- [ ] Scores justificados
- [ ] Ranking claro
- [ ] Corte realista para recursos

### Guardrails (Anti-alucinação)
- NÃO inventar métricas de reach/impact
- BASEAR scores em dados quando disponíveis
- DECLARAR confidence baixo quando estimativa
- NÃO forçar ranking quando itens são equivalentes

---

## 4. Trade-off Analysis

### Objetivo
Analisar trade-offs entre opções concorrentes de forma estruturada.

### Quando Usar
- Decisões com múltiplas dimensões
- Conflitos entre objetivos
- Otimização multi-critério

### Formato de Entrada
```
Opções em análise:
[OPCOES]

Dimensões de trade-off:
[DIMENSOES]

Prioridades/pesos:
[PESOS]

Constraints:
[CONSTRAINTS]
```

### Formato de Saída (Schema)
```json
{
  "tradeoff_analysis": {
    "opcoes": ["string"],
    "dimensoes": [
      {
        "nome": "string",
        "descricao": "string",
        "direcao": "maximizar|minimizar",
        "peso": 1-10
      }
    ],
    "matriz": [
      {
        "opcao": "string",
        "scores": {
          "dimensao1": {"valor": 0-10, "justificativa": "string"},
          "dimensao2": {"valor": 0-10, "justificativa": "string"}
        },
        "score_ponderado": 0-100
      }
    ],
    "conflitos": [
      {
        "dimensoes": ["string", "string"],
        "natureza": "string",
        "implicacao": "string"
      }
    ],
    "pareto_frontier": ["string"],
    "recomendacao": {
      "se_prioridade_X": "opcao_A",
      "se_prioridade_Y": "opcao_B",
      "balanceado": "opcao_C"
    }
  }
}
```

### Critérios de Sucesso
- [ ] Todas as dimensões avaliadas
- [ ] Conflitos identificados
- [ ] Pareto frontier quando aplicável
- [ ] Recomendação por cenário

### Guardrails (Anti-alucinação)
- NÃO esconder trade-offs desfavoráveis
- NÃO favorecer opção sem justificativa
- EXPLICITAR conflitos inerentes
- APRESENTAR múltiplos cenários

---

## 5. Go/No-Go

### Objetivo
Decisão binária estruturada para prosseguir ou não com iniciativa.

### Quando Usar
- Gates de projeto
- Launch decisions
- Aprovação de investimento
- Continuidade de iniciativa

### Formato de Entrada
```
Iniciativa em avaliação:
[INICIATIVA]

Critérios de go:
[CRITERIOS]

Status atual:
[STATUS]

Riscos conhecidos:
[RISCOS]
```

### Formato de Saída (Schema)
```json
{
  "go_nogo": {
    "iniciativa": "string",
    "data_avaliacao": "YYYY-MM-DD",
    "criterios": [
      {
        "nome": "string",
        "peso": "critico|importante|desejavel",
        "threshold": "string",
        "status_atual": "string",
        "atende": true,
        "evidencia": "string"
      }
    ],
    "resumo": {
      "criterios_criticos_atendidos": "X/Y",
      "criterios_importantes_atendidos": "X/Y",
      "criterios_desejaveis_atendidos": "X/Y"
    },
    "riscos_residuais": [
      {
        "risco": "string",
        "severidade": "alta|media|baixa",
        "mitigacao": "string",
        "aceito_por": "string"
      }
    ],
    "decisao": {
      "veredito": "GO|NO-GO|GO_COM_CONDICOES",
      "justificativa": "string",
      "condicoes": ["string"],
      "acoes_pre_go": ["string"],
      "data_reavaliacao": "YYYY-MM-DD|null"
    },
    "aprovadores": [
      {
        "nome": "string",
        "papel": "string",
        "voto": "aprova|reprova|abstem",
        "comentario": "string"
      }
    ]
  }
}
```

### Exemplo (Few-Shot)

**Input**:
```
Iniciativa: Launch do novo módulo de relatórios

Critérios de go:
- Crítico: Testes de regressão passando
- Crítico: Security review aprovado
- Importante: Performance P95 < 2s
- Desejável: Documentação completa

Status: Testes OK, security pending, P95 = 1.8s, docs 80%
Riscos: Security review atrasado 2 dias
```

**Output**:
```json
{
  "go_nogo": {
    "iniciativa": "Launch do novo módulo de relatórios",
    "data_avaliacao": "2026-01-18",
    "criterios": [
      {
        "nome": "Testes de regressão passando",
        "peso": "critico",
        "threshold": "100% green",
        "status_atual": "100% green",
        "atende": true,
        "evidencia": "CI pipeline #1234 - all tests passed"
      },
      {
        "nome": "Security review aprovado",
        "peso": "critico",
        "threshold": "Aprovação formal",
        "status_atual": "Em revisão (ETA: 2 dias)",
        "atende": false,
        "evidencia": "Ticket SEC-456 em análise"
      },
      {
        "nome": "Performance P95 < 2s",
        "peso": "importante",
        "threshold": "< 2000ms",
        "status_atual": "1800ms",
        "atende": true,
        "evidencia": "Load test report 2026-01-17"
      },
      {
        "nome": "Documentação completa",
        "peso": "desejavel",
        "threshold": "100%",
        "status_atual": "80%",
        "atende": false,
        "evidencia": "Faltam seções de troubleshooting"
      }
    ],
    "resumo": {
      "criterios_criticos_atendidos": "1/2",
      "criterios_importantes_atendidos": "1/1",
      "criterios_desejaveis_atendidos": "0/1"
    },
    "riscos_residuais": [
      {
        "risco": "Security review pode identificar issues",
        "severidade": "media",
        "mitigacao": "Rollback plan preparado",
        "aceito_por": "Pendente"
      }
    ],
    "decisao": {
      "veredito": "NO-GO",
      "justificativa": "Critério crítico (security review) não atendido. Não é possível lançar sem aprovação de segurança.",
      "condicoes": [
        "Security review deve ser concluído e aprovado",
        "Documentação pode ser completada pós-launch (não bloqueante)"
      ],
      "acoes_pre_go": [
        "Priorizar conclusão do security review",
        "Preparar comunicação de adiamento se necessário"
      ],
      "data_reavaliacao": "2026-01-20"
    },
    "aprovadores": [
      {
        "nome": "CTO",
        "papel": "Decisor final",
        "voto": "reprova",
        "comentario": "Aguardar security review - critério não negociável"
      }
    ]
  }
}
```

### Critérios de Sucesso
- [ ] Critérios claramente definidos
- [ ] Status atual documentado
- [ ] Evidências para cada critério
- [ ] Decisão justificada
- [ ] Próximos passos claros

### Guardrails (Anti-alucinação)
- NÃO aprovar sem critérios críticos atendidos
- NÃO inventar evidências
- ESCALAR quando decisão é borderline
- DOCUMENTAR quem decide e quando

---

## Boas Práticas

### Documentação de Decisões

1. **Decisões significativas** devem ser documentadas
2. **Contexto** é tão importante quanto a decisão
3. **Alternativas consideradas** mostram rigor
4. **Data de revisão** previne decisões obsoletas

### Comunicação

| Audiência | Foco |
|-----------|------|
| Executivos | Impacto de negócio, custos, timeline |
| Técnicos | Trade-offs, arquitetura, implementação |
| Stakeholders | Benefícios, riscos, próximos passos |

### Anti-patterns a Evitar

- **Analysis Paralysis**: Decidir com informação imperfeita é OK
- **HiPPO**: Highest Paid Person's Opinion não é metodologia
- **Sunk Cost**: Custos passados não justificam continuar
- **Groupthink**: Diversidade de opinião é saudável
