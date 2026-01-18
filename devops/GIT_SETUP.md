# Setup Git - Tech-Agentes

> **Guia rápido** para configurar Git e sincronizar com GitHub

---

## Setup Inicial (Primeira vez)

### 1. Inicializar Repositório

```bash
git init
```

### 2. Configurar Remote

```bash
git remote add origin https://github.com/adm-toolsmm-ia/tech-agentes.git
```

### 3. Configurar Branch Padrão

```bash
git branch -M main
```

### 4. Configurar Template de Commit

```bash
git config commit.template .gitmessage
```

---

## Formato de Commit (Conventional Commits)

```
<tipo>(<escopo>): <assunto>

Tipos válidos:
  feat:     Nova funcionalidade
  fix:      Correção de bug
  docs:     Mudanças em documentação
  style:    Formatação
  refactor: Refatoração
  test:     Testes
  chore:    Manutenção
  perf:     Performance
  ci:       CI/CD
  build:    Build system

Escopos: configs, agents, templates, schemas, cli, docs, workflows, devops

Exemplos:
  feat(agents): adicionar agente specialist healthcare
  fix(schemas): corrigir validação de tenant_id vazio
  docs(versionamento): atualizar política de tags
  chore(deps): atualizar pydantic para v2.9
```

---

## Comandos de Uso Diário

### Adicionar e Commitar

```bash
# Ver status
git status

# Adicionar arquivos
git add <arquivo>        # Arquivo específico
git add .                # Todos os arquivos modificados

# Commit (abre editor com template)
git commit

# Ou commit direto
git commit -m "feat(agents): adicionar specialist healthcare"
```

### Sincronizar com GitHub

```bash
# Atualizar do remoto
git fetch origin
git pull origin main

# Enviar para remoto
git push origin main

# Primeira vez (configurar upstream)
git push -u origin main
```

### Primeiro Push

```bash
git add .
git commit -m "chore: configuração inicial do projeto tech-agentes"
git push -u origin main
```

---

## Verificar Configuração

```bash
# Ver remote configurado
git remote -v

# Ver branch atual
git branch

# Ver template configurado
git config commit.template
```

---

## Troubleshooting

### Remote não configurado
```bash
git remote add origin https://github.com/adm-toolsmm-ia/tech-agentes.git
```

### Atualizar remote existente
```bash
git remote set-url origin https://github.com/adm-toolsmm-ia/tech-agentes.git
```

### Ver configurações Git do repositório
```bash
git config --list --local
```
