---
name: automind-ai-startup
description: Use when starting any new system, app, SaaS, CRM or automation project; when adding a new module or feature to an existing project; when about to write a spec or start coding without one; before declaring a build finished; and before any production deploy. Also triggers on "projeto novo", "sistema novo", "spec", "vistoria", "auditoria", "segurança", "está pronto pra produção?", "validar", "deploy".
---

# Automind AI Startup — fluxo do zero ao deploy

## Princípio

Código só começa depois de spec sem lacunas, é construído uma fase por vez, e nada é declarado pronto sem validação funcional, vistoria e auditoria de segurança com relatório salvo em `work-log/`.

## Qual etapa aplicar

| Situação | Etapa | Referência |
|---|---|---|
| Ideia bruta, sem documento nenhum | Briefing estruturado (máx. 3 perguntas antes) | `references/01-briefing.md` |
| Briefing ou pedido pronto, antes de codar | Spec sem lacunas: rodar TODOS os checklists | `references/02-spec-sem-lacunas.md` |
| Spec fechada, projeto ainda sem estrutura | Workspace: `CLAUDE.md` ≤ 200 linhas + `context/for-agent/NN-*.md` por fase + `CHECKLIST.md` | `references/03-workspace-por-fases.md` |
| Construção | Uma fase por vez, na ordem: setup → banco → auth → backend → frontend → automações → deploy → segurança. Sugerir `/clear` entre fases | `references/03-workspace-por-fases.md` |
| Fase ou feature "terminada" | Validação funcional (tudo existe e funciona?) | `references/04-validacao-funcional.md` |
| Validação ok | Vistoria só leitura (padrão) ou com correção (se autorizado) | `references/05a-vistoria-so-leitura.md` / `references/05b-vistoria-com-correcao.md` |
| Antes de produção | Auditoria de segurança em fases | `references/06-seguranca.md` |
| Última checagem antes do deploy | Veredito final A–F com bloqueadores | `references/07-veredito-final.md` |

Abra a referência da etapa e siga o protocolo dela. Não resuma de memória.

## Feature nova em projeto existente

A mesma sequência, com o escopo reduzido à feature:
1. Rodar os checklists de `02` só nas entidades e telas da feature: CRUD completo, os 7 estados de UI (loading, vazio, erro, sucesso, sem permissão, offline, desabilitado), botões, feedback (toast/confirmação).
2. Construir por fase: banco → API → tela.
3. Validação funcional (`04`) só nas telas afetadas, clicando de verdade.
4. Mexeu em banco, auth, permissão ou webhook: rodar a fase correspondente de `06` antes do deploy.

## Regras que valem em todas as etapas

- Informação faltando: assumir o padrão mais comum pro tipo de sistema e **documentar como suposição**. Não inventar funcionalidade fora do contexto.
- Multi-tenant: testar com 2 usuários de tenants diferentes tentando ler/escrever dado cruzado. Isolamento tem que ser 100%.
- Supabase: RLS em todas as tabelas, `SERVICE_ROLE_KEY` só no servidor.
- n8n: webhook sempre autenticado.
- Segurança e vistoria só leitura: **não modificar nada sem confirmação**. Achado crítico: parar e avisar na hora.
- Relatórios em `work-log/` (validação, auditoria, auditoria-final), com status ✅/⚠️/❌ e severidade 🔴/🟠/🟡/🔵.
- Qualquer 🔴 aberto = veredito "NÃO PRONTO", sem exceção.

## Erros comuns

| Erro | Correção |
|---|---|
| Começar a codar direto do pedido | Passar pelo checklist de `02`, mesmo que em versão curta |
| Fazer todas as fases numa sessão só | Uma fase, validar, próxima |
| Declarar pronto porque o build passou | Build passar ≠ funcionar. Rodar `04` clicando nas telas |
| Tela só com o estado de sucesso | Todos os estados de UI especificados e implementados |
| Auditoria de segurança que "roda meia dúzia de comandos e declara seguro" | Arquivo por arquivo, cada achado com arquivo+linha, exploração e correção |
