# Template: Pipeline CI/CD

> **Versão**: 1.0.0
> **Categoria**: DevOps
> **Uso**: Definir pipeline de integração e deploy contínuos

---

## Metadados do Pipeline

| Campo | Valor |
|-------|-------|
| **Projeto** | [Nome do Projeto] |
| **Repositório** | [URL do Repo] |
| **Plataforma CI/CD** | `GitHub Actions` / `GitLab CI` / `Azure DevOps` / `Jenkins` |
| **Última Atualização** | [YYYY-MM-DD] |
| **Responsável** | [Nome/Equipe] |

---

## 1. Visão Geral do Pipeline

### 1.1 Diagrama de Fluxo

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Commit  │───▶│   Build  │───▶│   Test   │───▶│  Deploy  │───▶│  Verify  │
│          │    │          │    │          │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │               │
     ▼               ▼               ▼               ▼               ▼
  trigger         lint           unit           staging         smoke
  validate        type-check     integration    production      health
  secrets         build          e2e            rollback        alerts
```

### 1.2 Ambientes

| Ambiente | Branch | Deploy | Aprovação |
|----------|--------|--------|-----------|
| **Dev** | `feature/*`, `fix/*` | Automático | Nenhuma |
| **Stage** | `develop`, `release/*` | Automático | Tech Lead |
| **Prod** | `main` | Manual | CTO + QA |

---

## 2. Stages do Pipeline

### 2.1 Stage: Validate

**Trigger**: Todo push/PR

```yaml
validate:
  runs-on: ubuntu-latest
  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Validate Branch Name
      run: |
        if [[ ! "${{ github.ref_name }}" =~ ^(main|develop|feature/|fix/|hotfix/|release/) ]]; then
          echo "Invalid branch name"
          exit 1
        fi

    - name: Check Secrets
      run: |
        # Verifica se não há secrets commitados
        if grep -rE "(api_key|password|secret|token)\s*=\s*['\"][^'\"]+['\"]" --include="*.py" --include="*.js" --include="*.ts" .; then
          echo "Potential secrets found!"
          exit 1
        fi

    - name: Validate Commit Messages
      run: |
        # Conventional commits
        git log --oneline -1 | grep -E "^[a-f0-9]+ (feat|fix|docs|style|refactor|test|chore|ci)(\(.+\))?: .+"
```

### 2.2 Stage: Build

**Trigger**: Após Validate passar

```yaml
build:
  needs: validate
  runs-on: ubuntu-latest
  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Install Dependencies
      run: |
        pip install -e .[dev]

    - name: Lint
      run: |
        ruff check .
        ruff format --check .

    - name: Type Check
      run: |
        mypy src/

    - name: Build Package
      run: |
        python -m build

    - name: Upload Artifact
      uses: actions/upload-artifact@v4
      with:
        name: dist
        path: dist/
```

### 2.3 Stage: Test

**Trigger**: Após Build passar

```yaml
test:
  needs: build
  runs-on: ubuntu-latest
  strategy:
    matrix:
      python-version: ['3.11', '3.12']

  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_PASSWORD: test
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5

  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Setup Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install Dependencies
      run: pip install -e .[dev]

    - name: Unit Tests
      run: |
        pytest tests/unit -v --cov=src --cov-report=xml

    - name: Integration Tests
      run: |
        pytest tests/integration -v
      env:
        DATABASE_URL: postgresql://postgres:test@localhost:5432/test

    - name: Upload Coverage
      uses: codecov/codecov-action@v4
      with:
        files: coverage.xml
```

### 2.4 Stage: Security

**Trigger**: PRs para `develop` ou `main`

```yaml
security:
  needs: test
  runs-on: ubuntu-latest
  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Dependency Audit
      run: |
        pip install pip-audit
        pip-audit

    - name: SAST Scan
      uses: github/codeql-action/analyze@v3
      with:
        languages: python

    - name: Container Scan
      if: hashFiles('Dockerfile') != ''
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.IMAGE_NAME }}
        severity: 'CRITICAL,HIGH'
```

### 2.5 Stage: Deploy Staging

**Trigger**: Push para `develop` ou `release/*`

```yaml
deploy-staging:
  needs: [test, security]
  if: github.ref == 'refs/heads/develop' || startsWith(github.ref, 'refs/heads/release/')
  runs-on: ubuntu-latest
  environment:
    name: staging
    url: https://staging.exemplo.com

  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Configure AWS
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_STAGING }}
        aws-region: us-east-1

    - name: Deploy to Staging
      run: |
        # Deploy via Terraform/Helm/etc
        cd infra/
        terraform init
        terraform apply -auto-approve -var="environment=staging"

    - name: Run Migrations
      run: |
        # Rodar migrations
        ./scripts/migrate.sh staging

    - name: Smoke Tests
      run: |
        # Testes básicos pós-deploy
        curl -f https://staging.exemplo.com/health || exit 1

    - name: Notify
      if: always()
      uses: slackapi/slack-github-action@v1
      with:
        channel-id: 'deploys'
        slack-message: "Deploy Staging: ${{ job.status }}"
```

### 2.6 Stage: Deploy Production

**Trigger**: Push para `main` (requer aprovação)

```yaml
deploy-production:
  needs: [test, security]
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  environment:
    name: production
    url: https://app.exemplo.com

  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Require Approvals
      run: |
        # Verificar aprovações necessárias
        echo "Deploy aprovado por: ${{ github.actor }}"

    - name: Configure AWS
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_PROD }}
        aws-region: us-east-1

    - name: Create Backup
      run: |
        # Backup antes do deploy
        ./scripts/backup.sh production

    - name: Deploy to Production
      run: |
        cd infra/
        terraform init
        terraform apply -auto-approve -var="environment=production"

    - name: Run Migrations
      run: |
        ./scripts/migrate.sh production

    - name: Smoke Tests
      run: |
        curl -f https://app.exemplo.com/health || exit 1

    - name: Monitor (5 min)
      run: |
        # Monitorar por 5 minutos
        ./scripts/monitor-deploy.sh 300

    - name: Rollback on Failure
      if: failure()
      run: |
        ./scripts/rollback.sh production

    - name: Notify
      if: always()
      uses: slackapi/slack-github-action@v1
      with:
        channel-id: 'deploys-prod'
        slack-message: "🚀 Deploy Production: ${{ job.status }}"
```

---

## 3. Configuração de Secrets

### 3.1 Secrets Necessários

| Secret | Ambiente | Descrição |
|--------|----------|-----------|
| `AWS_ROLE_STAGING` | Staging | Role ARN para deploy |
| `AWS_ROLE_PROD` | Production | Role ARN para deploy |
| `SLACK_WEBHOOK` | Todos | Notificações |
| `CODECOV_TOKEN` | CI | Upload de coverage |

### 3.2 Como Adicionar

```bash
# Via GitHub CLI
gh secret set AWS_ROLE_STAGING --env staging
gh secret set AWS_ROLE_PROD --env production
```

---

## 4. Environments e Aprovações

### 4.1 Configuração de Environment

```yaml
# .github/environments/production.yml (conceitual)
environment:
  name: production
  protection_rules:
    required_reviewers:
      - team: cto
      - team: qa-leads
    wait_timer: 5  # minutos
    deployment_branch_policy:
      protected_branches: true
```

### 4.2 Matriz de Aprovações

| Ambiente | Aprovadores | Wait Timer | Branches |
|----------|-------------|------------|----------|
| Dev | Nenhum | 0 | Qualquer |
| Staging | Tech Lead | 0 | develop, release/* |
| Production | CTO + QA | 5 min | main |

---

## 5. Rollback

### 5.1 Procedimento Automático

```yaml
rollback:
  runs-on: ubuntu-latest
  if: failure()
  steps:
    - name: Get Previous Version
      id: prev
      run: |
        PREV_VERSION=$(git describe --tags --abbrev=0 HEAD~1)
        echo "version=$PREV_VERSION" >> $GITHUB_OUTPUT

    - name: Rollback
      run: |
        ./scripts/deploy.sh ${{ steps.prev.outputs.version }}

    - name: Verify Rollback
      run: |
        curl -f https://app.exemplo.com/health

    - name: Alert
      run: |
        # Notificar sobre rollback
        echo "Rollback executado para ${{ steps.prev.outputs.version }}"
```

### 5.2 Rollback Manual

```bash
# Via CLI
./scripts/rollback.sh production v1.2.3

# Via GitHub Actions
gh workflow run rollback.yml -f version=v1.2.3 -f environment=production
```

---

## 6. Métricas e Monitoramento

### 6.1 Métricas do Pipeline

| Métrica | Target | Alerta |
|---------|--------|--------|
| Tempo total | < 15 min | > 20 min |
| Taxa de sucesso | > 95% | < 90% |
| Tempo de deploy | < 5 min | > 10 min |
| Coverage | > 80% | < 70% |

### 6.2 Dashboards

- **GitHub Actions**: Aba Actions do repositório
- **Grafana**: [URL do dashboard]
- **Datadog**: [URL do dashboard]

---

## 7. Manutenção

### 7.1 Atualizações Regulares

- [ ] **Semanal**: Revisar falhas de pipeline
- [ ] **Mensal**: Atualizar actions para versões recentes
- [ ] **Trimestral**: Revisar security scans e dependências

### 7.2 Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Build lento | Cache invalidado | Verificar cache keys |
| Testes flaky | Dependência de ordem | Isolar testes |
| Deploy falha | Permissões | Verificar roles |

---

## 8. Arquivo Completo de Referência

### GitHub Actions (`.github/workflows/ci-cd.yml`)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop, 'feature/**', 'fix/**', 'release/**']
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: '3.11'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate
        run: echo "Validation steps here"

  build:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      - run: pip install -e .[dev]
      - run: ruff check .
      - run: mypy src/

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -e .[dev]
      - run: pytest tests/ -v --cov=src

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: echo "Deploy to staging"

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: echo "Deploy to production"
```

---

## Checklist de Implementação

- [ ] Pipeline configurado na plataforma CI/CD
- [ ] Secrets configurados por ambiente
- [ ] Environments com aprovações configuradas
- [ ] Testes de rollback validados
- [ ] Notificações configuradas
- [ ] Documentação atualizada
- [ ] Time treinado no processo
