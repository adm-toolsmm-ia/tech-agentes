# ADR-001: Feature-Based Architecture para Frontend

> **Status**: Aprovado
> **Data**: 2026-01-18
> **Autor**: Agente Eng. Software / Arquiteto IA & DevOps
> **Aprovador**: CTO

---

## Contexto

O protótipo atual (`src/`) foi gerado pelo Lovable com estrutura técnica (por tipo de arquivo):

```
src/
├── components/
│   ├── dashboard/
│   ├── layout/
│   ├── solicitacoes/
│   └── ui/
├── contexts/
├── data/
├── hooks/
├── integrations/
├── lib/
└── pages/
```

Essa estrutura funciona para protótipos, mas apresenta problemas para projetos maiores:
- Difícil localizar código relacionado a uma feature
- Componentes, hooks e tipos espalhados em pastas diferentes
- Acoplamento implícito entre features

---

## Decisão

Adotar **Feature-Based Architecture** (também conhecida como Feature Slices ou Vertical Slices), organizando o código por domínio de negócio ao invés de tipo técnico.

### Nova Estrutura Proposta

```
src/
├── app/                          # Configuração global da aplicação
│   ├── App.tsx
│   ├── main.tsx
│   ├── routes.tsx                # Definição centralizada de rotas
│   └── providers.tsx             # Providers globais (Query, Auth, Theme)
│
├── features/                     # Módulos por domínio de negócio
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types.ts
│   │   └── index.ts              # Barrel export
│   │
│   ├── dashboard/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── index.ts
│   │
│   ├── solicitacoes/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types.ts
│   │   └── index.ts
│   │
│   ├── documentacoes/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── index.ts
│   │
│   ├── tarefas/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── index.ts
│   │
│   ├── logs/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── index.ts
│   │
│   └── admin/
│       ├── apis/
│       ├── automacoes/
│       ├── tabelas-auxiliares/
│       └── index.ts
│
├── shared/                       # Código compartilhado entre features
│   ├── components/
│   │   ├── ui/                   # Shadcn/ui components (mantido)
│   │   └── layout/               # Header, Sidebar, MainLayout
│   ├── hooks/
│   │   ├── use-toast.ts
│   │   └── use-mobile.tsx
│   ├── lib/
│   │   └── utils.ts
│   ├── types/
│   │   └── common.ts
│   └── services/
│       └── supabase/
│           ├── client.ts
│           └── types.ts
│
├── assets/                       # Arquivos estáticos
│   └── styles/
│       ├── index.css
│       └── App.css
│
└── test/                         # Configuração de testes
    └── setup.ts
```

---

## Justificativa

### Prós

1. **Coesão**: Todo código de uma feature fica junto (componentes, hooks, types, services)
2. **Manutenibilidade**: Fácil entender e modificar uma feature isoladamente
3. **Escalabilidade**: Novas features são adicionadas sem afetar estrutura existente
4. **Testabilidade**: Testes podem ser colocados junto da feature (`__tests__/`)
5. **Onboarding**: Novos desenvolvedores entendem o domínio mais facilmente
6. **Lazy Loading**: Features podem ser carregadas sob demanda facilmente

### Contras

1. **Migração inicial**: Requer mover arquivos e atualizar imports
2. **Código compartilhado**: Precisa de disciplina para não duplicar código
3. **Curva de aprendizado**: Equipe precisa entender a nova estrutura

### Mitigações

- Migração incremental por feature
- Linter rules para validar imports entre features
- Documentação clara da estrutura

---

## Regras de Organização

### 1. Features são isoladas

```typescript
// ✅ Correto: Feature importa de shared
import { Button } from '@/shared/components/ui/button';
import { supabase } from '@/shared/services/supabase/client';

// ❌ Incorreto: Feature importa de outra feature diretamente
import { TicketCard } from '@/features/solicitacoes/components/TicketCard';
```

### 2. Comunicação entre features via shared ou eventos

```typescript
// Se features precisam compartilhar dados, usar:
// - React Query cache (já compartilhado globalmente)
// - Context em shared/
// - Event bus (se necessário)
```

### 3. Barrel exports obrigatórios

```typescript
// features/solicitacoes/index.ts
export * from './components';
export * from './hooks';
export * from './types';
export { SolicitacoesPage } from './pages/SolicitacoesPage';
```

### 4. Tipos colocados junto da feature

```typescript
// features/solicitacoes/types.ts
export interface Solicitacao {
  id: string;
  titulo: string;
  // ...
}
```

---

## Plano de Migração

### Fase 1: Estrutura Base
1. Criar pastas `app/`, `features/`, `shared/`
2. Mover configuração global para `app/`
3. Mover `components/ui/` para `shared/components/ui/`
4. Mover `components/layout/` para `shared/components/layout/`

### Fase 2: Migrar Features (uma por vez)
1. `auth/` - Contexto e página de login
2. `dashboard/` - Páginas e componentes de dashboard
3. `solicitacoes/` - Kanban, lista, detalhes
4. `documentacoes/` - CRUD de docs
5. `tarefas/` e `logs/` - Sync e logs
6. `admin/` - APIs, automações, tabelas

### Fase 3: Limpeza
1. Remover pastas antigas vazias
2. Atualizar imports
3. Configurar path aliases no tsconfig

---

## Path Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/app/*": ["./src/app/*"],
      "@/features/*": ["./src/features/*"],
      "@/shared/*": ["./src/shared/*"]
    }
  }
}
```

---

## Consequências

### Positivas
- Código mais organizado e fácil de navegar
- Facilita code splitting e lazy loading
- Prepara para possível migração para monorepo no futuro

### Negativas
- Trabalho inicial de migração (~2-4 horas)
- Alguns imports quebrados durante migração

### Riscos
- **Baixo**: Possíveis bugs de import durante migração → Mitigado por testes e lint

---

## Decisões Relacionadas

- ADR-002 (futuro): Padrão de hooks com React Query
- ADR-003 (futuro): Estratégia de testes por feature

---

## Referências

- [Feature-Sliced Design](https://feature-sliced.design/)
- [Bulletproof React](https://github.com/alan2207/bulletproof-react)
- [React Project Structure Best Practices](https://www.robinwieruch.de/react-folder-structure/)

---

*ADR criado pelo Agente Eng. Software / Arquiteto em 2026-01-18*
