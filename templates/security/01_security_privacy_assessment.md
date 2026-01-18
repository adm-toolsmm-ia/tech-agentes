# Template: Security & Privacy Assessment

> **Versão**: 1.0.0
> **Categoria**: Segurança
> **Uso**: Avaliação de segurança e privacidade para novos projetos/features

---

## Metadados da Avaliação

| Campo | Valor |
|-------|-------|
| **Projeto/Feature** | [Nome] |
| **Data da Avaliação** | [YYYY-MM-DD] |
| **Avaliador** | [Nome] |
| **Status** | `Em Análise` / `Aprovado` / `Aprovado com Ressalvas` / `Reprovado` |
| **Próxima Revisão** | [YYYY-MM-DD] |

---

## 1. Escopo da Avaliação

### 1.1 Descrição do Sistema/Feature
[Descrição breve do que está sendo avaliado]

### 1.2 Componentes em Escopo

| Componente | Tipo | Em Escopo |
|------------|------|-----------|
| [API Backend] | Código | ✅ |
| [Frontend] | Código | ✅ |
| [Database] | Infraestrutura | ✅ |
| [Integrações] | Externa | ✅ |

### 1.3 Fora de Escopo
- [Componentes não avaliados nesta análise]

---

## 2. Classificação de Dados

### 2.1 Inventário de Dados

| Dado | Categoria | Fonte | Destino | Retenção |
|------|-----------|-------|---------|----------|
| Nome do usuário | PII | Input | Database | Conta ativa |
| Email | PII | Input | Database + Email service | Conta ativa |
| CPF | PII Sensível | Input | Database (criptografado) | Legal: 5 anos |
| Logs de acesso | Operacional | Sistema | Log storage | 90 dias |
| Métricas de uso | Analytics | Sistema | Analytics DB | 2 anos |

### 2.2 Fluxo de Dados

```
┌─────────┐    HTTPS    ┌─────────┐    TLS    ┌─────────┐
│ Cliente │────────────▶│   API   │─────────▶│   DB    │
└─────────┘             └─────────┘           └─────────┘
                              │
                              │ TLS
                              ▼
                        ┌─────────┐
                        │ Serviço │
                        │ Externo │
                        └─────────┘
```

### 2.3 Classificação de Criticidade

| Categoria | Dados | Controles Necessários |
|-----------|-------|----------------------|
| **Crítico** | Senhas, tokens, chaves | Criptografia forte, acesso mínimo |
| **Alto** | CPF, dados bancários | Criptografia, mascaramento, auditoria |
| **Médio** | Nome, email, telefone | Controle de acesso, pseudonimização |
| **Baixo** | Preferências, configs | Controle de acesso básico |

---

## 3. Avaliação LGPD

### 3.1 Checklist de Conformidade

| Requisito | Status | Evidência/Notas |
|-----------|--------|-----------------|
| [ ] Base legal identificada para cada tratamento | | |
| [ ] Finalidade específica documentada | | |
| [ ] Minimização de dados aplicada | | |
| [ ] Prazo de retenção definido | | |
| [ ] Consentimento coletado (quando aplicável) | | |
| [ ] Direitos do titular implementados | | |
| [ ] DPO notificado sobre o projeto | | |

### 3.2 Bases Legais Aplicadas

| Tratamento | Base Legal | Justificativa |
|------------|------------|---------------|
| Cadastro de usuário | Execução de contrato | Necessário para prestação do serviço |
| Envio de marketing | Consentimento | Opt-in explícito |
| Logs de segurança | Interesse legítimo | Segurança do sistema |

### 3.3 Direitos do Titular

| Direito | Implementado | Como Exercer |
|---------|--------------|--------------|
| Acesso | ✅ / ❌ | [Endpoint/Processo] |
| Correção | ✅ / ❌ | [Endpoint/Processo] |
| Exclusão | ✅ / ❌ | [Endpoint/Processo] |
| Portabilidade | ✅ / ❌ | [Endpoint/Processo] |
| Revogação | ✅ / ❌ | [Endpoint/Processo] |

### 3.4 DPIA (Data Protection Impact Assessment)

**Necessário DPIA?** [ ] Sim [ ] Não

Critérios para DPIA obrigatório:
- [ ] Avaliação sistemática de aspectos pessoais (profiling)
- [ ] Tratamento em larga escala de dados sensíveis
- [ ] Monitoramento sistemático de área pública
- [ ] Uso de novas tecnologias com alto risco

**Se necessário, link para DPIA**: [URL]

---

## 4. Avaliação de Segurança

### 4.1 OWASP Top 10

| Vulnerabilidade | Risco | Controle | Status |
|-----------------|-------|----------|--------|
| A01: Broken Access Control | | RBAC implementado | ✅ / ❌ |
| A02: Cryptographic Failures | | TLS 1.3, AES-256 | ✅ / ❌ |
| A03: Injection | | Queries parametrizadas | ✅ / ❌ |
| A04: Insecure Design | | Threat modeling | ✅ / ❌ |
| A05: Security Misconfiguration | | Hardening checklist | ✅ / ❌ |
| A06: Vulnerable Components | | Dependency scanning | ✅ / ❌ |
| A07: Auth Failures | | MFA, session mgmt | ✅ / ❌ |
| A08: Software Integrity | | CI/CD signing | ✅ / ❌ |
| A09: Logging Failures | | Structured logging | ✅ / ❌ |
| A10: SSRF | | URL validation | ✅ / ❌ |

### 4.2 Autenticação e Autorização

| Aspecto | Implementação | Status |
|---------|---------------|--------|
| Método de autenticação | [JWT/OAuth/etc] | |
| Força de senha | [Requisitos] | |
| MFA disponível | [Sim/Não] | |
| Session timeout | [X minutos] | |
| Rate limiting login | [X tentativas] | |
| RBAC/ABAC | [Modelo usado] | |

### 4.3 Criptografia

| Aspecto | Implementação | Status |
|---------|---------------|--------|
| Dados em trânsito | TLS 1.3 | |
| Dados em repouso | AES-256 | |
| Hashing de senhas | bcrypt/Argon2 | |
| Gestão de chaves | [Vault/KMS] | |
| Certificados | [Validade/Rotação] | |

### 4.4 Infraestrutura

| Aspecto | Implementação | Status |
|---------|---------------|--------|
| Firewall/WAF | [Configuração] | |
| Network segmentation | [VPC/Subnets] | |
| DDoS protection | [Cloudflare/Shield] | |
| Backup encryption | [Sim/Não] | |
| Disaster recovery | [RPO/RTO] | |

---

## 5. Avaliação de Riscos

### 5.1 Identificação de Ameaças (STRIDE)

| Ameaça | Descrição | Probabilidade | Impacto | Risco |
|--------|-----------|---------------|---------|-------|
| **S**poofing | Atacante se passa por usuário legítimo | | | |
| **T**ampering | Modificação não autorizada de dados | | | |
| **R**epudiation | Negação de ações realizadas | | | |
| **I**nformation Disclosure | Vazamento de dados | | | |
| **D**enial of Service | Indisponibilidade do serviço | | | |
| **E**levation of Privilege | Acesso não autorizado | | | |

### 5.2 Matriz de Risco

| Probabilidade ↓ / Impacto → | Baixo | Médio | Alto | Crítico |
|-----------------------------|-------|-------|------|---------|
| **Alta** | Médio | Alto | Crítico | Crítico |
| **Média** | Baixo | Médio | Alto | Crítico |
| **Baixa** | Baixo | Baixo | Médio | Alto |

### 5.3 Riscos Identificados

| ID | Risco | Classificação | Mitigação | Responsável | Prazo |
|----|-------|---------------|-----------|-------------|-------|
| R01 | [Descrição] | [Crítico/Alto/Médio/Baixo] | [Ação] | [Nome] | [Data] |
| R02 | [Descrição] | [Crítico/Alto/Médio/Baixo] | [Ação] | [Nome] | [Data] |

---

## 6. Segurança de AI/LLM (Se Aplicável)

### 6.1 Riscos Específicos de AI

| Risco | Status | Mitigação |
|-------|--------|-----------|
| Prompt Injection | | Input sanitization, output validation |
| Data Poisoning | | Training data validation |
| Model Extraction | | Rate limiting, watermarking |
| Membership Inference | | Differential privacy |
| Hallucination | | Grounding, confidence thresholds |

### 6.2 Checklist de Segurança AI

| Item | Status |
|------|--------|
| [ ] System prompt não pode ser sobrescrito por user input | |
| [ ] Outputs validados antes de ações (especialmente code execution) | |
| [ ] PII removida/mascarada antes de envio para modelo externo | |
| [ ] Rate limiting por usuário configurado | |
| [ ] Logging de todas as interações (sem PII) | |
| [ ] Fallback para casos de baixa confiança | |

---

## 7. Integrações Externas

### 7.1 Inventário de Integrações

| Serviço | Tipo | Dados Compartilhados | DPA Assinado |
|---------|------|---------------------|--------------|
| [Serviço 1] | [API/SaaS] | [Quais dados] | ✅ / ❌ |
| [Serviço 2] | [API/SaaS] | [Quais dados] | ✅ / ❌ |

### 7.2 Avaliação de Terceiros

| Serviço | SOC2 | ISO27001 | LGPD Compliance | Notas |
|---------|------|----------|-----------------|-------|
| [Serviço 1] | ✅ / ❌ | ✅ / ❌ | ✅ / ❌ | |
| [Serviço 2] | ✅ / ❌ | ✅ / ❌ | ✅ / ❌ | |

---

## 8. Plano de Ação

### 8.1 Ações Necessárias

| ID | Ação | Prioridade | Responsável | Prazo | Status |
|----|------|------------|-------------|-------|--------|
| A01 | [Descrição] | P0/P1/P2/P3 | [Nome] | [Data] | |
| A02 | [Descrição] | P0/P1/P2/P3 | [Nome] | [Data] | |

### 8.2 Riscos Aceitos

| ID | Risco | Justificativa | Aprovado por | Data |
|----|-------|---------------|--------------|------|
| RA01 | [Descrição] | [Por que aceitável] | [Nome] | [Data] |

---

## 9. Conclusão

### 9.1 Parecer

**Status Final**: [ ] Aprovado [ ] Aprovado com Ressalvas [ ] Reprovado

**Resumo**:
[Resumo da avaliação e principais pontos]

### 9.2 Condições para Aprovação (se com ressalvas)

- [ ] [Condição 1 - prazo]
- [ ] [Condição 2 - prazo]

### 9.3 Próximos Passos

1. [Ação 1]
2. [Ação 2]
3. [Ação 3]

---

## 10. Assinaturas

| Papel | Nome | Assinatura | Data |
|-------|------|------------|------|
| Security Lead | | | |
| DPO | | | |
| Tech Lead | | | |
| CTO | | | |

---

## Anexos

### A. Evidências Coletadas
[Lista de documentos, scans, relatórios]

### B. Referências
- OWASP Top 10: https://owasp.org/Top10/
- LGPD: Lei 13.709/2018
- ISO 27001
- NIST Cybersecurity Framework

### C. Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | [Data] | [Nome] | Avaliação inicial |
