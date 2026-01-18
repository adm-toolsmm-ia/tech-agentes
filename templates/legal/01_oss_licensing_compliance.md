# Template: Compliance de Licenças OSS

> **Versão**: 1.0.0
> **Categoria**: Legal
> **Uso**: Garantir conformidade de licenças de dependências OSS

---

## Metadados

| Campo | Valor |
|-------|-------|
| **Projeto** | [Nome do projeto] |
| **Data** | [YYYY-MM-DD] |
| **Responsável** | [Nome] |

---

## 1. Objetivo

Definir o processo mínimo para identificar, registrar e aprovar o uso de dependências OSS,
evitando riscos legais e conflitos de licença.

---

## 2. Escopo

- Dependências diretas e transitivas do projeto
- Modelos e assets com licenças externas
- Ferramentas de build e runtime

---

## 3. Inventário de Licenças

Preencher o inventário de dependências:

| Dependência | Versão | Licença | Tipo | Uso | Status |
|------------|--------|---------|------|-----|--------|
| [lib-x] | [1.2.3] | [MIT/Apache/GPL] | direta/transitiva | runtime/build | aprovado/pendente |

---

## 4. Regras de Aprovação

### 4.1 Licenças Permitidas (padrão)
- MIT
- Apache-2.0
- BSD-2/3

### 4.2 Licenças Restritivas (exigem aprovação)
- GPL, AGPL, LGPL
- SSPL, Elastic License

---

## 5. Checklist de Conformidade

- [ ] Inventário completo das dependências
- [ ] Licenças identificadas e registradas
- [ ] Licenças restritivas revisadas pelo Jurídico/CTO
- [ ] Notas de atribuição registradas (se aplicável)
- [ ] Política de atualização definida

---

## 6. Exemplo de Preenchimento (curto)

| Dependência | Versão | Licença | Tipo | Uso | Status |
|------------|--------|---------|------|-----|--------|
| pydantic | 2.7.0 | MIT | direta | runtime | aprovado |

---

## Histórico

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0.0 | 2026-01-18 | CTO | Template inicial |
