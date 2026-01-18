# Templates de Análise

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18
> **Categoria**: Análise e Avaliação

---

## Índice de Templates

1. [Análise de Requisitos](#1-análise-de-requisitos)
2. [Análise de Riscos](#2-análise-de-riscos)
3. [Análise de Gaps](#3-análise-de-gaps)
4. [Análise de Viabilidade](#4-análise-de-viabilidade)
5. [Análise Comparativa](#5-análise-comparativa)

---

## 1. Análise de Requisitos

### Objetivo
Extrair, estruturar e validar requisitos de negócio e técnicos a partir de documentos, conversas ou especificações.

### Quando Usar
- Início de projeto (discovery)
- Mudança de escopo significativa
- Onboarding de novo membro que precisa entender contexto

### Formato de Entrada
```
Documento/conversa/especificação a ser analisada:
[CONTEÚDO]

Contexto adicional (opcional):
[CONTEXTO]
```

### Formato de Saída (Schema)
```json
{
  "requisitos_funcionais": [
    {
      "id": "RF-001",
      "titulo": "string",
      "descricao": "string",
      "prioridade": "must|should|could|wont",
      "criterios_aceite": ["string"],
      "dependencias": ["RF-XXX"]
    }
  ],
  "requisitos_nao_funcionais": [
    {
      "id": "RNF-001",
      "categoria": "performance|seguranca|usabilidade|escalabilidade|disponibilidade",
      "descricao": "string",
      "metrica": "string",
      "threshold": "string"
    }
  ],
  "restricoes": ["string"],
  "premissas": ["string"],
  "perguntas_abertas": ["string"],
  "riscos_identificados": ["string"]
}
```

### Exemplo (Few-Shot)

**Input**:
```
Precisamos de um sistema de gestão de pedidos que permita aos clientes
fazerem pedidos online, acompanharem o status e receberem notificações.
O sistema deve suportar pelo menos 1000 pedidos simultâneos e ter
disponibilidade de 99.9%. Integração com o ERP SAP é obrigatória.
```

**Output**:
```json
{
  "requisitos_funcionais": [
    {
      "id": "RF-001",
      "titulo": "Cadastro de Pedidos Online",
      "descricao": "Permitir que clientes criem pedidos através de interface web",
      "prioridade": "must",
      "criterios_aceite": [
        "Cliente autenticado pode criar pedido",
        "Pedido recebe número único",
        "Confirmação enviada por email"
      ],
      "dependencias": []
    },
    {
      "id": "RF-002",
      "titulo": "Acompanhamento de Status",
      "descricao": "Exibir status atualizado do pedido para o cliente",
      "prioridade": "must",
      "criterios_aceite": [
        "Status visível na área do cliente",
        "Histórico de mudanças de status disponível"
      ],
      "dependencias": ["RF-001"]
    },
    {
      "id": "RF-003",
      "titulo": "Sistema de Notificações",
      "descricao": "Enviar notificações automáticas sobre mudanças de status",
      "prioridade": "must",
      "criterios_aceite": [
        "Notificação por email em mudança de status",
        "Cliente pode configurar preferências"
      ],
      "dependencias": ["RF-002"]
    },
    {
      "id": "RF-004",
      "titulo": "Integração SAP",
      "descricao": "Sincronizar pedidos com ERP SAP",
      "prioridade": "must",
      "criterios_aceite": [
        "Pedidos sincronizados em tempo real",
        "Erros de sincronização logados e alertados"
      ],
      "dependencias": ["RF-001"]
    }
  ],
  "requisitos_nao_funcionais": [
    {
      "id": "RNF-001",
      "categoria": "escalabilidade",
      "descricao": "Suportar carga de pedidos simultâneos",
      "metrica": "pedidos_simultaneos",
      "threshold": ">=1000"
    },
    {
      "id": "RNF-002",
      "categoria": "disponibilidade",
      "descricao": "Alta disponibilidade do sistema",
      "metrica": "uptime_percentual",
      "threshold": ">=99.9%"
    }
  ],
  "restricoes": [
    "Integração obrigatória com SAP existente"
  ],
  "premissas": [
    "SAP possui API disponível para integração",
    "Clientes já possuem cadastro no sistema atual"
  ],
  "perguntas_abertas": [
    "Qual versão do SAP está em uso?",
    "Quais canais de notificação além de email?",
    "Existe limite de itens por pedido?"
  ],
  "riscos_identificados": [
    "Dependência de disponibilidade da API SAP",
    "Complexidade de migração de dados existentes"
  ]
}
```

### Critérios de Sucesso
- [ ] Todos os requisitos têm ID único
- [ ] Priorização MoSCoW aplicada
- [ ] Critérios de aceite são testáveis
- [ ] Dependências mapeadas
- [ ] Perguntas abertas identificadas

### Guardrails (Anti-alucinação)
- NÃO inventar requisitos não mencionados no input
- NÃO assumir tecnologias não especificadas
- DECLARAR explicitamente quando informação está faltando
- PERGUNTAR quando houver ambiguidade crítica

---

## 2. Análise de Riscos

### Objetivo
Identificar, classificar e propor mitigações para riscos de projeto, técnicos ou de negócio.

### Quando Usar
- Planejamento de projeto/sprint
- Antes de mudanças significativas
- Revisões periódicas de portfólio

### Formato de Entrada
```
Contexto do projeto/situação:
[CONTEXTO]

Escopo da análise:
[ESCOPO]

Riscos já conhecidos (opcional):
[RISCOS_CONHECIDOS]
```

### Formato de Saída (Schema)
```json
{
  "riscos": [
    {
      "id": "RISK-001",
      "categoria": "tecnico|negocio|operacional|compliance|externo",
      "titulo": "string",
      "descricao": "string",
      "probabilidade": "baixa|media|alta",
      "impacto": "baixo|medio|alto|critico",
      "score": 1-25,
      "gatilhos": ["string"],
      "mitigacoes": [
        {
          "acao": "string",
          "responsavel": "string",
          "prazo": "string",
          "custo_estimado": "string"
        }
      ],
      "plano_contingencia": "string",
      "status": "identificado|mitigando|aceito|fechado"
    }
  ],
  "matriz_resumo": {
    "criticos": 0,
    "altos": 0,
    "medios": 0,
    "baixos": 0
  },
  "recomendacoes_priorizadas": ["string"]
}
```

### Exemplo (Few-Shot)

**Input**:
```
Projeto de migração de banco de dados Oracle para PostgreSQL.
Sistema crítico de faturamento com 5 anos de dados históricos.
Prazo: 3 meses. Equipe: 2 devs + 1 DBA.
```

**Output**:
```json
{
  "riscos": [
    {
      "id": "RISK-001",
      "categoria": "tecnico",
      "titulo": "Incompatibilidade de tipos de dados",
      "descricao": "Tipos específicos do Oracle podem não ter equivalente direto no PostgreSQL",
      "probabilidade": "alta",
      "impacto": "alto",
      "score": 16,
      "gatilhos": ["Erros de conversão durante migração", "Dados truncados"],
      "mitigacoes": [
        {
          "acao": "Mapear todos os tipos de dados antes da migração",
          "responsavel": "DBA",
          "prazo": "Semana 1",
          "custo_estimado": "16h"
        },
        {
          "acao": "Criar testes de validação de dados",
          "responsavel": "Dev",
          "prazo": "Semana 2",
          "custo_estimado": "24h"
        }
      ],
      "plano_contingencia": "Manter Oracle em paralelo por 30 dias após migração",
      "status": "identificado"
    },
    {
      "id": "RISK-002",
      "categoria": "operacional",
      "titulo": "Prazo insuficiente",
      "descricao": "3 meses pode ser agressivo para 5 anos de dados com equipe reduzida",
      "probabilidade": "media",
      "impacto": "critico",
      "score": 15,
      "gatilhos": ["Atrasos nas primeiras sprints", "Descoberta de complexidades"],
      "mitigacoes": [
        {
          "acao": "Migração em fases (dados recentes primeiro)",
          "responsavel": "Tech Lead",
          "prazo": "Planejamento",
          "custo_estimado": "8h"
        }
      ],
      "plano_contingencia": "Negociar extensão de prazo ou escopo reduzido",
      "status": "identificado"
    }
  ],
  "matriz_resumo": {
    "criticos": 0,
    "altos": 2,
    "medios": 0,
    "baixos": 0
  },
  "recomendacoes_priorizadas": [
    "1. Realizar PoC de migração com amostra de dados na semana 1",
    "2. Definir critérios de go/no-go antes de migração completa",
    "3. Considerar contratar DBA adicional temporariamente"
  ]
}
```

### Critérios de Sucesso
- [ ] Riscos categorizados corretamente
- [ ] Probabilidade e impacto justificados
- [ ] Mitigações são acionáveis
- [ ] Plano de contingência definido para riscos altos/críticos

### Guardrails (Anti-alucinação)
- NÃO minimizar riscos óbvios
- NÃO inventar probabilidades sem base
- BASEAR análise em evidências do contexto
- DECLARAR incertezas explicitamente

---

## 3. Análise de Gaps

### Objetivo
Comparar estado atual vs. estado desejado e identificar lacunas a serem endereçadas.

### Quando Usar
- Diagnóstico de maturidade
- Planejamento de melhorias
- Avaliação de conformidade

### Formato de Entrada
```
Estado atual:
[ESTADO_ATUAL]

Estado desejado/referência:
[ESTADO_DESEJADO]

Critérios de avaliação (opcional):
[CRITERIOS]
```

### Formato de Saída (Schema)
```json
{
  "dimensoes": [
    {
      "nome": "string",
      "estado_atual": {
        "descricao": "string",
        "score": 0-10,
        "evidencias": ["string"]
      },
      "estado_desejado": {
        "descricao": "string",
        "score": 0-10,
        "criterios": ["string"]
      },
      "gap": {
        "magnitude": "pequeno|medio|grande|critico",
        "descricao": "string",
        "impacto": "string"
      },
      "acoes_recomendadas": [
        {
          "acao": "string",
          "esforco": "P|M|G",
          "prioridade": "alta|media|baixa",
          "prazo_sugerido": "string"
        }
      ]
    }
  ],
  "resumo": {
    "score_atual": 0-10,
    "score_desejado": 0-10,
    "gaps_criticos": 0,
    "gaps_grandes": 0
  },
  "roadmap_sugerido": ["string"]
}
```

### Critérios de Sucesso
- [ ] Dimensões relevantes identificadas
- [ ] Scores justificados com evidências
- [ ] Ações são específicas e mensuráveis
- [ ] Roadmap é realista

### Guardrails (Anti-alucinação)
- NÃO assumir estado atual sem evidência
- NÃO propor ações genéricas sem contexto
- BASEAR scores em critérios explícitos

---

## 4. Análise de Viabilidade

### Objetivo
Avaliar se uma iniciativa é viável do ponto de vista técnico, financeiro e operacional.

### Quando Usar
- Avaliação de novas iniciativas
- Go/no-go decisions
- Comparação de alternativas

### Formato de Entrada
```
Iniciativa proposta:
[INICIATIVA]

Recursos disponíveis:
[RECURSOS]

Restrições conhecidas:
[RESTRICOES]
```

### Formato de Saída (Schema)
```json
{
  "iniciativa": "string",
  "viabilidade_tecnica": {
    "score": 0-10,
    "fatores_positivos": ["string"],
    "fatores_negativos": ["string"],
    "dependencias_tecnicas": ["string"],
    "riscos_tecnicos": ["string"]
  },
  "viabilidade_financeira": {
    "score": 0-10,
    "custo_estimado": "string",
    "roi_estimado": "string",
    "payback_period": "string",
    "riscos_financeiros": ["string"]
  },
  "viabilidade_operacional": {
    "score": 0-10,
    "capacidade_equipe": "string",
    "impacto_operacoes": "string",
    "change_management": "string",
    "riscos_operacionais": ["string"]
  },
  "viabilidade_temporal": {
    "score": 0-10,
    "prazo_estimado": "string",
    "marcos_criticos": ["string"],
    "riscos_de_prazo": ["string"]
  },
  "veredito": {
    "recomendacao": "aprovar|aprovar_com_ressalvas|reprovar|investigar_mais",
    "justificativa": "string",
    "condicoes": ["string"],
    "proximos_passos": ["string"]
  }
}
```

### Critérios de Sucesso
- [ ] Todas as dimensões avaliadas
- [ ] Scores justificados
- [ ] Riscos mapeados por dimensão
- [ ] Recomendação clara com condições

### Guardrails (Anti-alucinação)
- NÃO estimar custos/ROI sem dados
- NÃO garantir viabilidade sem evidência
- DECLARAR limitações da análise
- RECOMENDAR investigação quando dados insuficientes

---

## 5. Análise Comparativa

### Objetivo
Comparar opções/alternativas de forma estruturada para suportar decisão.

### Quando Usar
- Seleção de tecnologia/ferramenta
- Comparação de fornecedores
- Trade-off entre abordagens

### Formato de Entrada
```
Opções a comparar:
[OPCOES]

Critérios de avaliação:
[CRITERIOS]

Pesos dos critérios (opcional):
[PESOS]

Contexto da decisão:
[CONTEXTO]
```

### Formato de Saída (Schema)
```json
{
  "criterios": [
    {
      "nome": "string",
      "peso": 1-5,
      "descricao": "string"
    }
  ],
  "opcoes": [
    {
      "nome": "string",
      "avaliacoes": [
        {
          "criterio": "string",
          "score": 0-10,
          "justificativa": "string"
        }
      ],
      "score_ponderado": 0-10,
      "pros": ["string"],
      "cons": ["string"]
    }
  ],
  "ranking": [
    {
      "posicao": 1,
      "opcao": "string",
      "score": 0-10
    }
  ],
  "recomendacao": {
    "escolha": "string",
    "justificativa": "string",
    "ressalvas": ["string"],
    "alternativa_se": "string"
  }
}
```

### Critérios de Sucesso
- [ ] Critérios são relevantes e mensuráveis
- [ ] Pesos refletem prioridades do contexto
- [ ] Avaliações são justificadas
- [ ] Recomendação considera trade-offs

### Guardrails (Anti-alucinação)
- NÃO favorecer opção sem justificativa
- NÃO omitir cons de opções preferidas
- BASEAR avaliações em fatos verificáveis
- DECLARAR quando comparação é inconclusiva

---

## Uso Geral dos Templates

### Como Aplicar

1. **Selecione o template** adequado ao tipo de análise
2. **Prepare o input** no formato especificado
3. **Execute a análise** usando o prompt completo
4. **Valide o output** contra os critérios de sucesso
5. **Revise guardrails** para garantir qualidade

### Composição de Templates

Templates podem ser combinados. Exemplo:
- Análise de Requisitos → identifica escopo
- Análise de Riscos → mapeia riscos do escopo
- Análise de Viabilidade → valida se é factível

### Versionamento

Alterações significativas nestes templates devem:
1. Incrementar versão (semver)
2. Documentar mudança em changelog
3. Rodar golden sets para validar
4. Obter aprovação do CTO se crítico
