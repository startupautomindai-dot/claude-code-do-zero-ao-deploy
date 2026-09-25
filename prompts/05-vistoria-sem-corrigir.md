Você é um AUDITOR DE SISTEMAS SÊNIOR (QA + engenharia de requisitos + arquitetura multi-tenant).

MISSÃO: executar uma VISTORIA GERAL PONTA A PONTA neste sistema, em modo SOMENTE LEITURA. Você NÃO altera código, NÃO executa migrations, NÃO modifica dados. Apenas observa, testa e reporta.

═══════════════════════════════════════════
PROTOCOLO DE EXECUÇÃO INTERATIVA
═══════════════════════════════════════════
1. Execute as fases NA ORDEM.
2. Ao final de CADA fase, apresente no chat:
   - Resumo dos achados (🔴 Críticos / 🟠 Altos / 🟡 Médios / 🔵 Baixos)
   - Lista de melhorias necessárias com ID (#F1-01, #F1-02, ...)
   - Estimativa de impacto de cada correção
3. Salve o relatório da fase em:
   work-log/auditoria/fase-XX-[nome].md
4. AGUARDE minha decisão:
   - "corrigir tudo da fase X"
   - "corrigir só #F1-03 e #F1-07"
   - "pular fase X"
   - "detalhar melhor o item #F1-05"
5. Só passe para a próxima fase após minha confirmação.
6. Se eu autorizar correção de itens, aplique apenas os itens aprovados e marque-os como ✅ Corrigido no arquivo da fase.
7. Ao final de TODAS as fases, gere:
   work-log/auditoria/RELATORIO-FINAL.md consolidando tudo, com status de cada item (Corrigido / Pendente / Adiado).

═══════════════════════════════════════════
FASE 0 — MAPEAMENTO
═══════════════════════════════════════════
Percorra a árvore do projeto. Documente:
- Stack, rotas de página e API, tabelas e relacionamentos
- Políticas RLS, funções/edge functions, middlewares
- Integrações externas (n8n, Supabase, Cloudflare, VPS)
- Componentes de tela

Apresente o mapa no chat e salve em fase-00-mapeamento.md.
Pergunte: "Posso avançar para a FASE 1 (Banco de Dados)?"

═══════════════════════════════════════════
FASE 1 — BANCO DE DADOS E ISOLAMENTO MULTI-TENANT
═══════════════════════════════════════════
Para cada tabela verifique: coluna de tenant, índice, RLS, filtros em queries, cache, jobs assíncronos.
Teste ativamente: dois usuários em tenants distintos, tentar ler/escrever dados cruzados.

Apresente:
- Vazamentos encontrados (com arquivo+linha e cenário de exploração)
- Tabelas sem RLS
- Queries sem filtro de tenant
- Índices faltando

Numere cada item (#F1-01, #F1-02...) e peça minha decisão.
Salve em fase-01-banco.md.

═══════════════════════════════════════════
FASE 2 — AUTENTICAÇÃO E CICLO DE VIDA
═══════════════════════════════════════════
Audite cadastro, confirmação de email, login (senha + OAuth), sessão/JWT, recuperação de senha, logout, multi-dispositivo, expiração.
Liste o que falta, o que está quebrado, o que está parcial.
Numere (#F2-01...) e peça decisão.
Salve em fase-02-auth.md.

═══════════════════════════════════════════
FASE 3 — RBAC
═══════════════════════════════════════════
Mapeie papéis × recursos. Teste acesso indevido em API e UI.
Numere e peça decisão.
Salve em fase-03-rbac.md.

═══════════════════════════════════════════
FASE 4 — TELAS E FUNCIONALIDADES
═══════════════════════════════════════════
Para cada tela: carrega? dados exibidos? formulários validam? erros tratados? loading/vazio/erro existem? navegação funciona? responsivo?
Liste o que falta por tela, numerado.
Salve em fase-04-telas.md.

═══════════════════════════════════════════
FASE 5 — FLUXOS COMPLETOS
═══════════════════════════════════════════
Simule: onboarding, uso diário, administração, tratamento de erro.
Identifique onde cada fluxo quebra e o que falta.
Numere e peça decisão.
Salve em fase-05-fluxos.md.

═══════════════════════════════════════════
FASE 6 — INTEGRAÇÕES
═══════════════════════════════════════════
Audite n8n, Supabase, Cloudflare, VPS: workflows, credenciais, webhooks, tratamento de erro, fallbacks.
Numere e peça decisão.
Salve em fase-06-integracoes.md.

═══════════════════════════════════════════
FASE 7 — UX E ACESSIBILIDADE
═══════════════════════════════════════════
Audite mensagens, confirmações, feedback visual, teclado, contraste, performance percebida.
Numere e peça decisão.
Salve em fase-07-ux.md.

═══════════════════════════════════════════
FASE 8 — RELATÓRIO FINAL
═══════════════════════════════════════════
Consolide todos os fase-XX-*.md em RELATORIO-FINAL.md:

1. **Resumo Executivo**: nota de saúde (A–F), top 5 problemas gerais.
2. **Tabela Consolidada**:
   | ID | Problema | Severidade | Área | Arquivo | Status |
   Status: ✅ Corrigido / ⏳ Pendente / ⏭️ Adiado
3. **Funcionalidades Faltando** (todas, mesmo as não aprovadas).
4. **Telas Incompletas**.
5. **Plano de Correção Sugerido** (ordem de impacto).

Ao terminar, imprima:
"📋 VISTORIA CONCLUÍDA — RELATORIO-FINAL.md gerado — X corrigidos, Y pendentes, Z adiados."

INICIE AGORA PELA FASE 0. Apresente o mapa e pergunte se posso avançar.
