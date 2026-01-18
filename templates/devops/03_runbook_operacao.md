# Template: Runbook de Operações

> **Versão**: 1.0.0
> **Categoria**: DevOps / Operações
> **Uso**: Documentar procedimentos operacionais padronizados

---

## Metadados do Runbook

| Campo | Valor |
|-------|-------|
| **Sistema/Serviço** | [Nome do Sistema] |
| **Criticidade** | `Alta` / `Média` / `Baixa` |
| **SLA** | [X% uptime, Yms latência] |
| **Última Revisão** | [YYYY-MM-DD] |
| **Responsável** | [Nome/Equipe] |
| **Contato de Emergência** | [Email/Telefone] |

---

## 1. Visão Geral do Sistema

### 1.1 Descrição
[Breve descrição do sistema e sua função de negócio]

### 1.2 Arquitetura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  Load       │────▶│  App        │
│             │     │  Balancer   │     │  Servers    │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                    ┌─────────────┐     ┌─────┴─────┐
                    │   Cache     │◀────│  Database │
                    │   (Redis)   │     │  (Postgres)│
                    └─────────────┘     └───────────┘
```

### 1.3 Componentes Principais

| Componente | Tecnologia | Localização | Health Check |
|------------|------------|-------------|--------------|
| API | Python/FastAPI | EKS cluster | `/health` |
| Database | PostgreSQL 15 | RDS | Port 5432 |
| Cache | Redis 7 | ElastiCache | Port 6379 |
| Queue | RabbitMQ | EC2 | Port 5672 |

### 1.4 Dependências Externas

| Serviço | SLA | Fallback |
|---------|-----|----------|
| AWS | 99.99% | Multi-AZ |
| Stripe | 99.9% | Queue + retry |
| SendGrid | 99.9% | Fallback SMTP |

---

## 2. Acessos e Ferramentas

### 2.1 Acessos Necessários

| Sistema | Como Obter | Nível Necessário |
|---------|------------|------------------|
| AWS Console | SSO via Okta | DevOps role |
| Kubernetes | `kubectl` config | namespace-admin |
| Database | Bastion host | read-only (ops) |
| Logs | Datadog | viewer |
| Alerts | PagerDuty | responder |

### 2.2 Ferramentas

```bash
# Configurar kubectl
aws eks update-kubeconfig --name production-cluster --region us-east-1

# Conectar ao bastion
ssh -i ~/.ssh/bastion.pem ec2-user@bastion.exemplo.com

# Acessar database (via bastion)
psql -h db.exemplo.internal -U readonly -d production
```

---

## 3. Monitoramento

### 3.1 Dashboards

| Dashboard | URL | Descrição |
|-----------|-----|-----------|
| Overview | [Grafana URL] | Métricas gerais |
| API | [Grafana URL] | Latência, throughput |
| Database | [Grafana URL] | Queries, conexões |
| Infra | [Grafana URL] | CPU, memória, disco |

### 3.2 Métricas Críticas

| Métrica | Normal | Warning | Critical |
|---------|--------|---------|----------|
| API Latency P95 | < 200ms | 200-500ms | > 500ms |
| Error Rate | < 1% | 1-5% | > 5% |
| CPU Usage | < 70% | 70-85% | > 85% |
| Memory Usage | < 80% | 80-90% | > 90% |
| DB Connections | < 80% | 80-90% | > 90% |
| Disk Usage | < 70% | 70-85% | > 85% |

### 3.3 Alertas Configurados

| Alerta | Severidade | Ação |
|--------|------------|------|
| `HighErrorRate` | P1 | Investigar imediatamente |
| `HighLatency` | P2 | Verificar em 15 min |
| `DiskSpaceLow` | P2 | Expandir/limpar em 1h |
| `CertExpiring` | P3 | Renovar em 7 dias |

---

## 4. Procedimentos de Rotina

### 4.1 Health Check Diário

```bash
#!/bin/bash
# health-check.sh

echo "=== Health Check $(date) ==="

# 1. Verificar pods
kubectl get pods -n production
if [ $(kubectl get pods -n production | grep -v Running | wc -l) -gt 1 ]; then
    echo "⚠️ Pods com problema!"
fi

# 2. Verificar endpoints
curl -s https://api.exemplo.com/health | jq .

# 3. Verificar métricas recentes
echo "Latência P95 (última hora):"
curl -s "https://metrics.exemplo.com/api/v1/query?query=http_latency_p95[1h]" | jq .

# 4. Verificar logs de erro
echo "Erros na última hora:"
kubectl logs -n production -l app=api --since=1h | grep -c ERROR
```

### 4.2 Backup Verificação (Semanal)

```bash
#!/bin/bash
# verify-backups.sh

# 1. Listar backups recentes
aws rds describe-db-snapshots --db-instance-identifier production-db \
    --query 'DBSnapshots[?SnapshotCreateTime>=`2024-01-01`].{ID:DBSnapshotIdentifier,Time:SnapshotCreateTime}'

# 2. Verificar backup mais recente
LATEST=$(aws rds describe-db-snapshots --db-instance-identifier production-db \
    --query 'sort_by(DBSnapshots, &SnapshotCreateTime)[-1].DBSnapshotIdentifier' --output text)

echo "Backup mais recente: $LATEST"

# 3. Testar restore (em ambiente de teste)
# aws rds restore-db-instance-from-db-snapshot ...
```

### 4.3 Rotação de Logs (Automático)

Configurado via logrotate:
```
/var/log/app/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 app app
    postrotate
        systemctl reload app
    endscript
}
```

---

## 5. Procedimentos de Incidentes

### 5.1 Triagem Inicial

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CONFIRMAR INCIDENTE                                          │
│    - Alerta é real ou falso positivo?                           │
│    - Qual é o impacto? (usuários afetados, funcionalidade)      │
│    - Desde quando?                                               │
├─────────────────────────────────────────────────────────────────┤
│ 2. CLASSIFICAR SEVERIDADE                                        │
│    P1: Serviço indisponível, >50% usuários afetados             │
│    P2: Funcionalidade degradada, <50% usuários afetados         │
│    P3: Impacto menor, workaround disponível                     │
│    P4: Cosmético, sem impacto funcional                         │
├─────────────────────────────────────────────────────────────────┤
│ 3. COMUNICAR                                                     │
│    P1: Escalar imediatamente para CTO + status page             │
│    P2: Notificar Tech Lead + atualizar status interno           │
│    P3/P4: Registrar ticket para resolução normal                │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Incidente: Alta Latência

**Sintomas**: Latência P95 > 500ms, timeout em requests

**Diagnóstico**:
```bash
# 1. Verificar métricas de infra
kubectl top pods -n production

# 2. Verificar queries lentas
psql -c "SELECT * FROM pg_stat_activity WHERE state = 'active' AND query_start < now() - interval '5 seconds';"

# 3. Verificar cache hit rate
redis-cli INFO stats | grep keyspace

# 4. Verificar logs
kubectl logs -n production -l app=api --tail=100 | grep -E "(slow|timeout|error)"
```

**Ações**:
| Causa | Ação |
|-------|------|
| CPU alta em pods | Scale horizontal: `kubectl scale deployment api --replicas=10` |
| Queries lentas | Identificar e otimizar ou kill: `SELECT pg_terminate_backend(pid)` |
| Cache miss | Verificar Redis, warm cache se necessário |
| Dependência externa | Ativar circuit breaker, verificar status do serviço |

**Rollback se necessário**:
```bash
# Reverter último deploy
kubectl rollout undo deployment/api -n production

# Verificar status
kubectl rollout status deployment/api -n production
```

### 5.3 Incidente: Erro 5xx em Massa

**Sintomas**: Error rate > 5%, múltiplos 500s

**Diagnóstico**:
```bash
# 1. Verificar logs de erro
kubectl logs -n production -l app=api --since=10m | grep -E "ERROR|Exception" | head -50

# 2. Verificar eventos recentes
kubectl get events -n production --sort-by='.lastTimestamp' | tail -20

# 3. Verificar último deploy
kubectl rollout history deployment/api -n production
```

**Ações**:
| Causa | Ação |
|-------|------|
| Bug em novo deploy | Rollback imediato |
| Database down | Verificar RDS, failover se necessário |
| Dependency failure | Verificar circuit breaker, fallback |
| Memory leak | Restart pods: `kubectl rollout restart deployment/api` |

### 5.4 Incidente: Database Indisponível

**Sintomas**: Connection refused, timeout em queries

**Diagnóstico**:
```bash
# 1. Verificar status RDS
aws rds describe-db-instances --db-instance-identifier production-db \
    --query 'DBInstances[0].{Status:DBInstanceStatus,Endpoint:Endpoint}'

# 2. Testar conectividade
nc -zv db.exemplo.internal 5432

# 3. Verificar logs RDS
aws rds describe-events --source-identifier production-db --source-type db-instance
```

**Ações**:
| Causa | Ação |
|-------|------|
| Instance down | Aguardar auto-recovery ou manual reboot |
| Network issue | Verificar security groups e NACLs |
| Storage full | Aumentar storage, limpar dados antigos |
| Too many connections | Kill connections idle, aumentar limit |

---

## 6. Procedimentos de Deploy

### 6.1 Deploy Padrão

```bash
#!/bin/bash
# deploy.sh <version> <environment>

VERSION=$1
ENV=$2

echo "=== Deploying $VERSION to $ENV ==="

# 1. Pre-checks
./scripts/pre-deploy-check.sh $ENV || exit 1

# 2. Backup atual
kubectl get deployment api -n $ENV -o yaml > /tmp/api-backup.yaml

# 3. Deploy
kubectl set image deployment/api api=registry.exemplo.com/api:$VERSION -n $ENV

# 4. Aguardar rollout
kubectl rollout status deployment/api -n $ENV --timeout=300s

# 5. Smoke tests
./scripts/smoke-tests.sh $ENV

# 6. Monitorar por 5 minutos
./scripts/monitor.sh $ENV 300

echo "=== Deploy Complete ==="
```

### 6.2 Rollback

```bash
#!/bin/bash
# rollback.sh <environment> [revision]

ENV=$1
REVISION=${2:-1}  # Default: voltar 1 revisão

echo "=== Rolling back $ENV to revision -$REVISION ==="

# 1. Executar rollback
kubectl rollout undo deployment/api -n $ENV --to-revision=$REVISION

# 2. Aguardar
kubectl rollout status deployment/api -n $ENV

# 3. Verificar
curl -f https://$ENV.exemplo.com/health

echo "=== Rollback Complete ==="
```

### 6.3 Hotfix em Produção

```
⚠️ PROCEDIMENTO DE EMERGÊNCIA - REQUER APROVAÇÃO CTO

1. Criar branch hotfix/[issue-id]
2. Implementar fix com teste mínimo
3. PR com label "hotfix" + aprovação CTO
4. Deploy direto para produção (bypass staging)
5. Monitoramento intensivo por 1 hora
6. Backport para develop
7. Post-mortem em 24 horas
```

---

## 7. Manutenção Programada

### 7.1 Checklist Pré-Manutenção

- [ ] Comunicado enviado com 48h de antecedência
- [ ] Janela de manutenção aprovada
- [ ] Backup verificado
- [ ] Rollback plan documentado
- [ ] Equipe de plantão confirmada

### 7.2 Procedimento de Manutenção

```bash
#!/bin/bash
# maintenance.sh start|stop

ACTION=$1

case $ACTION in
    start)
        # 1. Ativar página de manutenção
        kubectl apply -f maintenance-page.yaml

        # 2. Drain connections
        kubectl scale deployment api --replicas=0

        # 3. Confirmar
        echo "Manutenção iniciada às $(date)"
        ;;

    stop)
        # 1. Restaurar serviço
        kubectl scale deployment api --replicas=5

        # 2. Remover página de manutenção
        kubectl delete -f maintenance-page.yaml

        # 3. Verificar health
        sleep 30
        curl -f https://api.exemplo.com/health

        echo "Manutenção finalizada às $(date)"
        ;;
esac
```

---

## 8. Contatos e Escalação

### 8.1 Matriz de Escalação

| Nível | Tempo | Quem Contatar |
|-------|-------|---------------|
| L1 | 0-15 min | On-call engineer |
| L2 | 15-30 min | Tech Lead |
| L3 | 30-60 min | CTO |
| L4 | > 60 min | CEO + Comunicação |

### 8.2 Contatos

| Papel | Nome | Contato | Horário |
|-------|------|---------|---------|
| On-call | Rotativo | PagerDuty | 24/7 |
| Tech Lead | [Nome] | [Telefone] | Comercial |
| CTO | [Nome] | [Telefone] | Emergências |
| DBA | [Nome] | [Telefone] | Comercial |
| Infra | [Nome] | [Telefone] | Comercial |

---

## 9. Histórico e Lições Aprendidas

### 9.1 Incidentes Passados

| Data | Incidente | Causa | Resolução | Post-mortem |
|------|-----------|-------|-----------|-------------|
| 2024-01-15 | Outage 2h | Deploy com bug | Rollback | [Link] |
| 2024-02-20 | Latência alta | Query N+1 | Otimização | [Link] |

### 9.2 Melhorias Implementadas

- [2024-01] Adicionado circuit breaker para dependências
- [2024-02] Melhorado alertas de latência
- [2024-03] Automatizado backup verification

---

## Checklist de Validação do Runbook

- [ ] Todos os comandos testados e funcionais
- [ ] Acessos documentados e verificados
- [ ] Contatos atualizados
- [ ] Procedimentos revisados pela equipe
- [ ] Treinamento realizado com on-call
- [ ] Próxima revisão agendada
