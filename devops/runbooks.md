# Runbooks Operacionais - Tech-Agentes

> **Versão**: 1.0.0
> **Última atualização**: 2026-01-18
> **Responsável**: DevOps / CTO

---

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Instalação e Setup](#2-instalação-e-setup)
3. [Operações de Rotina](#3-operações-de-rotina)
4. [Troubleshooting](#4-troubleshooting)
5. [Releases e Deploy](#5-releases-e-deploy)
6. [Gestão de Ambientes](#6-gestão-de-ambientes)
7. [Contatos e Escalação](#7-contatos-e-escalação)

---

## 1. Visão Geral

### 1.1 O que é o Tech-Agentes

O tech-agentes é um framework padrão para projetos multiagentes com AI/LLM. Inclui:

- **CLI**: Ferramenta de linha de comando para scaffold, validação e sync
- **Schemas**: Definições Pydantic para configs e workflows
- **Templates**: Documentação e prompts padronizados
- **Agentes**: Definições de agentes base

### 1.2 Componentes do Sistema

```
tech-agentes/
├── src/tech_agents/     # Código fonte do CLI
├── agents/              # Definições de agentes
├── configs/             # Configurações de projeto
├── templates/           # Templates de documentação
├── prompts/             # Templates de prompts
├── workflows/           # Planos e backlog
├── evals/               # Golden sets e rubricas
└── devops/              # Pipelines e runbooks
```

### 1.3 Ambientes

| Ambiente | Uso | Branch | PyPI |
|----------|-----|--------|------|
| Dev | Desenvolvimento local | feature/*, fix/* | N/A |
| Stage | Testes de integração | develop, release/* | TestPyPI |
| Prod | Produção | main + tags | PyPI |

---

## 2. Instalação e Setup

### 2.1 Requisitos

- Python 3.11+
- pip ou uv
- Git

### 2.2 Instalação para Desenvolvimento

```bash
# Clonar repositório
git clone https://github.com/solucoessistemas/tech-agentes.git
cd tech-agentes

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou: .venv\Scripts\activate  # Windows

# Instalar em modo editable com deps de dev
pip install -e .[dev]

# Verificar instalação
tech-agents --help
tech-agents scan .
```

### 2.3 Instalação de Produção

```bash
# Via PyPI (quando publicado)
pip install tech-agentes

# Via GitHub
pip install git+https://github.com/solucoessistemas/tech-agentes.git

# Versão específica
pip install tech-agentes==0.1.0
```

### 2.4 Configuração de Editor (VS Code)

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "ruff.enable": true
}
```

---

## 3. Operações de Rotina

### 3.1 Executar Linting

```bash
# Verificar problemas
ruff check .

# Corrigir automaticamente
ruff check --fix .

# Verificar formatação
ruff format --check .

# Formatar
ruff format .
```

### 3.2 Executar Testes

```bash
# Todos os testes
pytest tests/ -v

# Com coverage
pytest tests/ -v --cov=src/tech_agents --cov-report=html

# Testes específicos
pytest tests/test_cli.py -v
pytest tests/ -k "test_scan" -v
```

### 3.3 Verificar Type Hints

```bash
mypy src/ --ignore-missing-imports
```

### 3.4 Build do Pacote

```bash
# Instalar build
pip install build

# Build
python -m build

# Verificar
ls dist/
# tech_agentes-0.1.0-py3-none-any.whl
# tech_agentes-0.1.0.tar.gz

# Testar instalação
pip install dist/*.whl
tech-agents --help
```

### 3.5 Validar Repo Alvo

```bash
# Escanear estrutura
tech-agents scan /path/to/repo

# Validar configs e schemas
tech-agents validate /path/to/repo

# Exportar artefatos
tech-agents export /path/to/repo --out /path/to/output
```

---

## 4. Troubleshooting

### 4.1 CLI não encontrado após instalação

**Sintoma**: `tech-agents: command not found`

**Diagnóstico**:
```bash
# Verificar se está instalado
pip show tech-agentes

# Verificar scripts
pip show -f tech-agentes | grep bin

# Verificar PATH
echo $PATH
which tech-agents
```

**Solução**:
```bash
# Reinstalar
pip uninstall tech-agentes
pip install -e .

# Ou adicionar ao PATH
export PATH="$HOME/.local/bin:$PATH"
```

### 4.2 Erro de validação de schema

**Sintoma**: `ValidationError: ... is not a valid ...`

**Diagnóstico**:
```bash
# Verificar conteúdo do arquivo
cat configs/projeto.json | python -m json.tool

# Validar manualmente
python -c "
from tech_agents.schemas.configs import ProjectConfig
import json
data = json.load(open('configs/projeto.json'))
ProjectConfig.model_validate(data)
"
```

**Solução**:
1. Verificar se JSON é válido
2. Comparar com schema esperado
3. Corrigir campos inválidos

### 4.3 Testes falhando localmente mas passando no CI

**Diagnóstico**:
```bash
# Verificar versão do Python
python --version

# Limpar cache
rm -rf .pytest_cache __pycache__ .mypy_cache

# Reinstalar deps
pip install -e .[dev] --force-reinstall
```

**Solução**:
1. Garantir mesma versão de Python
2. Limpar caches
3. Atualizar dependências

### 4.4 Import errors no desenvolvimento

**Sintoma**: `ModuleNotFoundError: No module named 'tech_agents'`

**Solução**:
```bash
# Reinstalar em modo editable
pip install -e .

# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

---

## 5. Releases e Deploy

### 5.1 Processo de Release

```
1. Criar branch release/X.Y.Z a partir de develop
2. Atualizar versão em pyproject.toml
3. Atualizar CHANGELOG.md
4. Criar PR para main
5. Após aprovação e merge, criar tag vX.Y.Z
6. Pipeline publica automaticamente no PyPI
```

### 5.2 Criar Release Manualmente

```bash
# 1. Atualizar versão
# Editar pyproject.toml: version = "X.Y.Z"

# 2. Commit
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z"

# 3. Criar tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z

# 4. Pipeline roda automaticamente
```

### 5.3 Publicar no PyPI (Manual)

```bash
# Apenas se pipeline falhar ou for necessário manual

# 1. Build
python -m build

# 2. Upload para TestPyPI primeiro
pip install twine
twine upload --repository testpypi dist/*

# 3. Testar instalação do TestPyPI
pip install --index-url https://test.pypi.org/simple/ tech-agentes

# 4. Se OK, upload para PyPI
twine upload dist/*
```

### 5.4 Rollback de Release

```bash
# 1. Yankar versão problemática no PyPI (via web UI)

# 2. Criar hotfix
git checkout -b hotfix/X.Y.Z-fix main
# ... fazer correções ...

# 3. Bump patch version
# Editar pyproject.toml: version = "X.Y.Z+1"

# 4. PR + merge + tag
git push origin hotfix/X.Y.Z-fix
# Criar PR, aprovar, mergear
git checkout main && git pull
git tag -a vX.Y.Z+1 -m "Hotfix release"
git push origin vX.Y.Z+1
```

---

## 6. Gestão de Ambientes

### 6.1 Criar Novo Ambiente de Teste

```bash
# Criar venv isolado
python -m venv /tmp/test-env
source /tmp/test-env/bin/activate

# Instalar versão específica
pip install tech-agentes==X.Y.Z

# Ou do branch
pip install git+https://github.com/solucoessistemas/tech-agentes.git@develop
```

### 6.2 Atualizar Dependências

```bash
# Ver outdated
pip list --outdated

# Atualizar deps de dev
pip install -U ruff mypy pytest

# Atualizar tudo
pip install -e .[dev] --upgrade

# Regenerar lock file (se usar)
pip freeze > requirements-lock.txt
```

### 6.3 Limpar Ambiente

```bash
# Limpar caches
rm -rf .pytest_cache .mypy_cache .ruff_cache __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Limpar builds
rm -rf dist/ build/ *.egg-info

# Reset completo
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

---

## 7. Contatos e Escalação

### 7.1 Matriz de Responsabilidades

| Área | Responsável | Contato |
|------|-------------|---------|
| CLI / Core | Dev Team | [canal] |
| Templates / Docs | Doc Team | [canal] |
| DevOps / Pipeline | DevOps | [canal] |
| Segurança | Security | [canal] |
| Decisões técnicas | CTO | [canal] |

### 7.2 Escalação

| Severidade | Tempo | Quem Contatar |
|------------|-------|---------------|
| P1 - Bloqueante | Imediato | CTO + DevOps |
| P2 - Crítico | < 4h | Tech Lead |
| P3 - Importante | < 24h | Time responsável |
| P4 - Nice-to-have | Backlog | Time responsável |

### 7.3 Canais de Comunicação

- **Issues**: GitHub Issues para bugs e features
- **Discussões**: GitHub Discussions para dúvidas
- **Urgente**: [Canal Slack/Teams]
- **Releases**: [Canal de anúncios]

---

## Checklist de Onboarding

Para novos membros do time:

- [ ] Clonar repositório
- [ ] Setup de ambiente local
- [ ] Rodar testes localmente
- [ ] Entender estrutura de diretórios
- [ ] Ler documentação de agentes
- [ ] Fazer PR de teste (fix typo ou similar)
- [ ] Acessos a CI/CD configurados
- [ ] Adicionado aos canais de comunicação

---

## Histórico de Revisões

| Data | Versão | Autor | Mudanças |
|------|--------|-------|----------|
| 2026-01-18 | 1.0.0 | CTO | Versão inicial |
