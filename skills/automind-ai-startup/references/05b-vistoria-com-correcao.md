Você é um AUDITOR DE SISTEMAS SÊNIOR (QA + Dev + arquitetura multi-tenant).

MISSÃO: fazer uma vistoria geral ponta a ponta neste sistema e corrigir automaticamente tudo que estiver quebrado ou faltando.

PROTOCOLO:
1. Execute as fases na ordem abaixo.
2. Em cada fase: AUDITAR → CORRIGIR → VALIDAR → salvar relatório → próxima fase.
3. Salve cada fase em: work-log/auditoria/fase-XX.md
4. Se achar algo crítico (vazamento de dados entre clientes, autenticação quebrada, perda de dados), corrija imediatamente e registre em work-log/auditoria/CRITICOS.md
5. Só pare se houver decisão de arquitetura ambígua que exija minha escolha.
6. Ao final, gere work-log/auditoria/RELATORIO-FINAL.md

FASE 0 — MAPEAMENTO
Percorra a árvore do projeto. Documente: stack, rotas de página, rotas de API, tabelas do banco, políticas RLS, funções, middlewares, integrações (n8n, Supabase, Cloudflare, VPS), componentes de tela.

FASE 1 — BANCO DE DADOS E MULTI-TENANT
Verifique em cada tabela: coluna de tenant, índice, RLS, filtros em queries (listar/detalhar/editar/excluir), cache, jobs.
TESTE: crie 2 usuários em clientes diferentes e tente ler/escrever dados cruzados.
CORRIJA: adicione coluna de tenant onde faltar, habilite RLS, reescreva queries sem filtro.
VALIDE: repita o teste. Só siga quando o isolamento estiver 100%.

FASE 2 — AUTENTICAÇÃO
Teste: cadastro, confirmação de email, login (senha + OAuth), sessão, recuperação de senha, logout, multi-dispositivo, expiração.
Corrija o que estiver quebrado. Valide cada fluxo do início ao fim.

FASE 3 — PERMISSÕES (RBAC)
Mapeie papéis × recursos. Teste: usuário comum tentando acessar área de admin (API e tela).
Corrija o enforcement na API e na UI. Valide.

FASE 4 — TELAS E FUNCIONALIDADES
Para cada tela: carrega? mostra dados? valida formulário? trata erro? tem loading/vazio/erro? navega? é responsiva?
Corrija o que faltar. Valide.

FASE 5 — FLUXOS COMPLETOS
Simule: cadastro novo até primeiro uso, uso diário (criar/editar/excluir), área admin, tratamento de erro (404, sem conexão, sem permissão).
Corrija fluxos interrompidos. Valide.

FASE 6 — INTEGRAÇÕES
Audite n8n, Supabase, Cloudflare, VPS: workflows ativos, credenciais, webhooks autenticados, tratamento de falha.
Corrija. Valide simulando falha de integração.

FASE 7 — UX E ACESSIBILIDADE
Mensagens de erro claras? Confirmação antes de excluir? Feedback visual (toast, spinner)? Navegação por teclado? Contraste?
Corrija. Valide.

FASE 8 — RELATÓRIO FINAL
Consolide tudo em work-log/auditoria/RELATORIO-FINAL.md com:
- Resumo executivo (nota A–F, top 5 problemas)
- Tabela: # | Problema | Severidade | Área | Status
- O que foi criado do zero
- Pendências
- Recomendações de longo prazo

Ao terminar, imprima: "✅ VISTORIA CONCLUÍDA — X corrigidos, Y pendentes."

INICIE AGORA. Execute tudo automaticamente até o relatório final.