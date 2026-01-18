# tech-agentes

Base padrão de **multiagentes** (Cursor + AI) para iniciar e acompanhar projetos da equipe.

## O que é
Este repositório é a **fonte da verdade** para:
- Estrutura padrão de projeto (docs, agents, prompts, workflows, configs, templates).
- Regras operacionais (segurança, governança do CTO, semver, observabilidade real).
- CLI Python para **instalar/sincronizar** essa base em qualquer repositório-alvo.

## Como rodar (dev)
1) Crie/ative um ambiente Python 3.11+.
2) Instale em modo editable:

```bash
pip install -e .[dev]
```

3) Veja comandos do CLI:

```bash
tech-agents --help
```

## Comandos principais (MVP)
- `tech-agents scan <repo>`
- `tech-agents init <repo> --project-name <name> --tenant-id <tenant> --env dev`
- `tech-agents install-rules <repo>`
- `tech-agents validate <repo>`
- `tech-agents export <repo>`
- `tech-agents eval <repo> --outputs-json <file>`

