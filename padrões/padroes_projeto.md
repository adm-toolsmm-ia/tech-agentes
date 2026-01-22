# Padrões do Projeto (Base Tech-Agentes)

## Hierarquia
1) **MUST (sempre)**: segurança, LGPD/PII, segredos, validação de inputs, não-destrutivo sem confirmação.
2) **Decisões do projeto**: `configs/` e `docs/` do projeto-alvo prevalecem.
3) **Fallback**: aplicar defaults por tipo/fase quando não houver decisão.
## Semver e mudanças
- Padrões/agents/templates são versionados (semver). Mudanças estruturais exigem ADR.
## Logging & Observabilidade
- 100% das execuções logadas com `run_id` e `tenant_id`.
- **Proibido** registrar estimativas não instrumentadas (tokens/latência/custo).
- `stage/prod`: exige instrumentação real habilitada (ou aprovação explícita do CTO).
## Gates (QA/Evals)
- Mudanças críticas (prompts/modelos/políticas) exigem rodar golden sets + rubricas.
- Evidências devem ser salvas em `evals/resultados/` antes de `stage/prod`.
