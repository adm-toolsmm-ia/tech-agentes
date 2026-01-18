# Infraestrutura

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18

---

## Visão Geral

Este diretório contém configurações de infraestrutura como código (IaC) para o projeto tech-agentes.

**Nota**: O tech-agentes é primariamente uma biblioteca/CLI Python, portanto a infraestrutura é mínima. Este diretório é principalmente para:

1. **Documentação de padrões** de IaC para projetos que usam tech-agentes
2. **Referências** para setups específicos quando necessário
3. **Templates** de infraestrutura reutilizáveis

---

## Estrutura Planejada

```
infra/
├── README.md           # Este arquivo
├── terraform/          # Módulos Terraform (quando necessário)
│   ├── modules/
│   └── environments/
├── kubernetes/         # Manifests K8s (quando necessário)
│   ├── base/
│   └── overlays/
└── docker/             # Dockerfiles (quando necessário)
```

---

## Padrões de IaC

### Terraform

Quando usar Terraform para projetos tech-agentes:

```hcl
# Estrutura de módulo padrão
module "example" {
  source = "./modules/example"

  # Sempre incluir tags padrão
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = "tech-team"
  }
}

# Variáveis obrigatórias
variable "project_name" {
  type        = string
  description = "Nome do projeto"
}

variable "environment" {
  type        = string
  description = "Ambiente (dev/stage/prod)"
  validation {
    condition     = contains(["dev", "stage", "prod"], var.environment)
    error_message = "Environment deve ser dev, stage ou prod."
  }
}
```

### Kubernetes

Quando usar Kubernetes:

```yaml
# Labels padrão
metadata:
  labels:
    app.kubernetes.io/name: {{ .Chart.Name }}
    app.kubernetes.io/instance: {{ .Release.Name }}
    app.kubernetes.io/version: {{ .Chart.AppVersion }}
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    tech-agentes.io/project: {{ .Values.project }}
    tech-agentes.io/environment: {{ .Values.environment }}
```

### Docker

Quando criar Dockerfiles:

```dockerfile
# Base image padrão
FROM python:3.11-slim

# Labels padrão
LABEL maintainer="tech-team"
LABEL org.opencontainers.image.source="https://github.com/solucoessistemas/tech-agentes"

# Security: non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# ... restante do Dockerfile
```

---

## Referências

- [Template CI/CD](../templates/devops/01_ci_cd_pipeline.md)
- [Template Runbook](../templates/devops/03_runbook_operacao.md)
- [Políticas de Segurança](../../docs/seguranca/politicas.md)

---

## Quando Adicionar Infraestrutura

Adicione configurações neste diretório quando:

1. **Deploy automatizado**: Pipeline precisa provisionar recursos
2. **Ambientes de teste**: Infra para testes de integração
3. **Serviços auxiliares**: Databases, caches para desenvolvimento
4. **Containers**: Dockerização do CLI ou serviços relacionados

Não adicione:

- Configurações de projetos-alvo (cada projeto tem seu próprio infra/)
- Secrets ou credenciais (usar secret managers)
- Dados de produção ou backups
