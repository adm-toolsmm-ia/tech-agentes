# Template: QA Checklist

> **Versão**: 1.0.0
> **Categoria**: Qualidade
> **Uso**: Checklist de qualidade por fase do projeto

---

## Metadados

| Campo | Valor |
|-------|-------|
| **Projeto** | [Nome do Projeto] |
| **Versão/Release** | [X.Y.Z] |
| **Data** | [YYYY-MM-DD] |
| **QA Responsável** | [Nome] |
| **Status** | `Em Progresso` / `Aprovado` / `Reprovado` |

---

## 1. Checklist de Desenvolvimento (Dev)

### 1.1 Código

| Item | Status | Notas |
|------|--------|-------|
| [ ] Código segue padrões do projeto (lint passa) | | |
| [ ] Type hints/annotations presentes | | |
| [ ] Sem TODOs/FIXMEs bloqueantes | | |
| [ ] Código revisado por peer | | |
| [ ] Commits seguem conventional commits | | |

### 1.2 Testes Unitários

| Item | Status | Notas |
|------|--------|-------|
| [ ] Testes unitários escritos para nova funcionalidade | | |
| [ ] Coverage >= 80% no código novo | | |
| [ ] Todos os testes passando | | |
| [ ] Testes são determinísticos (não flaky) | | |
| [ ] Edge cases cobertos | | |

### 1.3 Documentação Dev

| Item | Status | Notas |
|------|--------|-------|
| [ ] Docstrings em funções públicas | | |
| [ ] README atualizado se necessário | | |
| [ ] CHANGELOG atualizado | | |
| [ ] Comentários em lógica complexa | | |

### 1.4 Segurança Básica

| Item | Status | Notas |
|------|--------|-------|
| [ ] Sem secrets hardcoded | | |
| [ ] Inputs validados | | |
| [ ] Queries parametrizadas | | |
| [ ] Dependências sem vulnerabilidades críticas | | |

---

## 2. Checklist de Staging

### 2.1 Deploy

| Item | Status | Notas |
|------|--------|-------|
| [ ] Pipeline CI passou (lint, build, test) | | |
| [ ] Deploy em staging bem-sucedido | | |
| [ ] Migrations executadas sem erro | | |
| [ ] Rollback testado | | |

### 2.2 Testes de Integração

| Item | Status | Notas |
|------|--------|-------|
| [ ] Testes de integração passando | | |
| [ ] APIs respondendo corretamente | | |
| [ ] Integrações externas funcionando | | |
| [ ] Fluxos principais testados end-to-end | | |

### 2.3 Performance

| Item | Status | Notas |
|------|--------|-------|
| [ ] Latência P95 dentro do SLO | | |
| [ ] Sem memory leaks detectados | | |
| [ ] Load test executado (se aplicável) | | |
| [ ] Queries otimizadas (sem N+1) | | |

### 2.4 Segurança Staging

| Item | Status | Notas |
|------|--------|-------|
| [ ] Security scan passou | | |
| [ ] OWASP Top 10 verificado | | |
| [ ] Autenticação funcionando | | |
| [ ] Autorização correta por role | | |
| [ ] HTTPS configurado | | |

### 2.5 Observabilidade

| Item | Status | Notas |
|------|--------|-------|
| [ ] Logs estruturados e corretos | | |
| [ ] Métricas sendo coletadas | | |
| [ ] Traces funcionando | | |
| [ ] Alertas configurados | | |

---

## 3. Checklist de Produção

### 3.1 Pré-Deploy

| Item | Status | Notas |
|------|--------|-------|
| [ ] Aprovação de Tech Lead | | |
| [ ] Aprovação de CTO | | |
| [ ] Janela de deploy confirmada | | |
| [ ] Comunicação enviada (se necessário) | | |
| [ ] Backup verificado | | |
| [ ] Plano de rollback documentado | | |

### 3.2 Deploy

| Item | Status | Notas |
|------|--------|-------|
| [ ] Deploy executado com sucesso | | |
| [ ] Health checks passando | | |
| [ ] Smoke tests passando | | |
| [ ] Sem erros novos nos logs | | |

### 3.3 Pós-Deploy (Verificação 15 min)

| Item | Status | Notas |
|------|--------|-------|
| [ ] Error rate estável | | |
| [ ] Latência dentro do esperado | | |
| [ ] Sem alertas disparados | | |
| [ ] Funcionalidade principal testada | | |

### 3.4 Pós-Deploy (Verificação 1 hora)

| Item | Status | Notas |
|------|--------|-------|
| [ ] Métricas de negócio estáveis | | |
| [ ] Feedback de usuários OK | | |
| [ ] Sem degradação de performance | | |
| [ ] Logs sem anomalias | | |

### 3.5 Pós-Deploy (Verificação 24 horas)

| Item | Status | Notas |
|------|--------|-------|
| [ ] Nenhum incidente relacionado | | |
| [ ] Métricas dentro do baseline | | |
| [ ] Jobs batch executados com sucesso | | |
| [ ] Release notes publicadas | | |

---

## 4. Checklist Específico por Tipo

### 4.1 Feature Nova

| Item | Status | Notas |
|------|--------|-------|
| [ ] Requisitos atendidos conforme spec | | |
| [ ] UX/UI conforme design (se aplicável) | | |
| [ ] Feature flag configurada | | |
| [ ] Documentação de usuário atualizada | | |
| [ ] Analytics/eventos configurados | | |

### 4.2 Bug Fix

| Item | Status | Notas |
|------|--------|-------|
| [ ] Bug reproduzido antes do fix | | |
| [ ] Fix resolve o problema | | |
| [ ] Teste de regressão adicionado | | |
| [ ] Não introduz novos bugs | | |
| [ ] Ticket atualizado | | |

### 4.3 Refactoring

| Item | Status | Notas |
|------|--------|-------|
| [ ] Comportamento externo inalterado | | |
| [ ] Testes existentes ainda passam | | |
| [ ] Performance não degradada | | |
| [ ] Documentação atualizada se API mudou | | |

### 4.4 Hotfix

| Item | Status | Notas |
|------|--------|-------|
| [ ] Aprovação de emergência obtida | | |
| [ ] Fix mínimo e focado | | |
| [ ] Testado em staging (mesmo que brevemente) | | |
| [ ] Monitoramento intensivo pós-deploy | | |
| [ ] Post-mortem agendado | | |

### 4.5 Migração de Dados

| Item | Status | Notas |
|------|--------|-------|
| [ ] Backup antes da migração | | |
| [ ] Migration testada em staging com dados reais | | |
| [ ] Rollback de migration possível | | |
| [ ] Tempo de execução estimado e comunicado | | |
| [ ] Validação de dados pós-migração | | |

---

## 5. Checklist de AI/LLM

### 5.1 Prompts

| Item | Status | Notas |
|------|--------|-------|
| [ ] Prompt especificado em template formal | | |
| [ ] Golden sets definidos | | |
| [ ] Rubricas de avaliação aplicadas | | |
| [ ] Anti-alucinação verificado | | |
| [ ] Output validado contra schema | | |

### 5.2 Segurança AI

| Item | Status | Notas |
|------|--------|-------|
| [ ] Prompt injection testado | | |
| [ ] Output sanitizado antes de uso | | |
| [ ] Rate limiting configurado | | |
| [ ] PII mascarada em logs | | |
| [ ] Custos estimados e budgets definidos | | |

### 5.3 Qualidade de Output

| Item | Status | Notas |
|------|--------|-------|
| [ ] Precision/Recall aceitáveis | | |
| [ ] Confidence scores calibrados | | |
| [ ] Fallback para casos de baixa confiança | | |
| [ ] Revisão humana para casos críticos | | |

---

## 6. Métricas de Qualidade

### 6.1 Critérios de Aceitação

| Métrica | Threshold | Atual | Status |
|---------|-----------|-------|--------|
| Test Coverage | >= 80% | | |
| Bugs Críticos | 0 | | |
| Bugs Altos | <= 2 | | |
| Security Issues | 0 críticos | | |
| Performance Regression | 0 | | |

### 6.2 Definição de Pronto (DoD)

**Uma feature está "pronta" quando**:
- [ ] Código revisado e aprovado
- [ ] Testes escritos e passando
- [ ] Documentação atualizada
- [ ] Deploy em staging bem-sucedido
- [ ] Testes de aceitação passando
- [ ] Sem bugs críticos ou altos

---

## 7. Sign-off

### 7.1 Aprovações Necessárias

| Papel | Nome | Assinatura | Data |
|-------|------|------------|------|
| Dev Lead | | | |
| QA Lead | | | |
| Tech Lead | | | |
| CTO (prod) | | | |

### 7.2 Notas Finais

```
[Espaço para observações, riscos aceitos, débitos técnicos, etc.]
```

---

## 8. Histórico

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0.0 | YYYY-MM-DD | [Nome] | Versão inicial |

---

## Anexo: Comandos Úteis

### Rodar Testes
```bash
# Unitários
pytest tests/unit -v --cov=src

# Integração
pytest tests/integration -v

# E2E
pytest tests/e2e -v --headed
```

### Verificar Coverage
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Security Scan
```bash
# Dependências
pip-audit

# Código
bandit -r src/
```

### Performance Test
```bash
# Locust load test
locust -f tests/load/locustfile.py --host=https://staging.exemplo.com
```
