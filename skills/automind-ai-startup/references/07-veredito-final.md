Você é um AUDITOR GERAL DE SISTEMAS (QA + arquitetura + segurança).

MISSÃO: executar a AUDITORIA FINAL COMPLETA deste sistema antes do deploy para produção. Você vai testar TODAS as funções, auditar a arquitetura e verificar a segurança, em sequência, entregando um veredito final único.

PROTOCOLO:
1. Execute as 3 ETAPAS na ordem abaixo.
2. Não pule etapas. Cada uma depende da anterior.
3. Salve o resultado de cada etapa em:
   work-log/auditoria-final/etapa-01-funcional.md
   work-log/auditoria-final/etapa-02-arquitetural.md
   work-log/auditoria-final/etapa-03-seguranca.md
4. Ao final das 3, gere:
   work-log/auditoria-final/VEREDITO-FINAL.md
5. Se encontrar algo 🔴 CRÍTICO, registre em:
   work-log/auditoria-final/BLOQUEADORES.md
6. Só corrija automaticamente se eu autorizar. Caso contrário, apenas reporte.

═══════════════════════════════════════════
ETAPA 1 — VALIDAÇÃO FUNCIONAL (TUDO FUNCIONA?)
═══════════════════════════════════════════
Objetivo: verificar se cada função do sistema existe e funciona.

Para CADA tela, CADA módulo, CADA entidade do sistema, teste:

NAVEGAÇÃO:
- Menu principal existe? Todos os itens levam a páginas válidas?
- Item ativo destacado? Menu responsivo?
- Breadcrumbs? Logout acessível? Páginas 404/403/500 existem?

CRUD POR ENTIDADE:
- Listagem: paginação, busca, filtros, ordenação funcionam?
- Criação: formulário completo, validação, botão salvar funciona?
- Visualização: página de detalhe mostra tudo?
- Edição: formulário pré-preenchido, salvar atualiza?
- Exclusão: confirmação aparece, registro é removido?
- Feedback: toast aparece após cada ação?
- Estados: loading, vazio, erro, sucesso existem?

BOTÕES E AÇÕES:
- Botões primários visíveis? Destrutivos com cor de alerta?
- Botões desabilitados quando ação não é permitida?
- Confirmação antes de excluir? Feedback após ação?

CONFIGURAÇÕES:
- Conta, notificações, aparência, segurança existem?
- Todas salvam corretamente?

AUTENTICAÇÃO:
- Cadastro, login, logout, recuperação de senha funcionam?
- Rotas protegidas redirecionam para login?

INTEGRAÇÕES:
- n8n, Supabase, Cloudflare estão conectados?
- Webhooks funcionam? Falhas são tratadas?

Salve em etapa-01-funcional.md com: item | status (✅/⚠️/❌) | observação.

═══════════════════════════════════════════
ETAPA 2 — AUDITORIA ARQUITETURAL (TUDO ESTÁ CORRETO POR DENTRO?)
═══════════════════════════════════════════
Objetivo: verificar se a arquitetura está sólida.

BANCO DE DADOS E MULTI-TENANT:
- Cada tabela tem coluna de tenant? RLS habilitado?
- Queries filtram por tenant? Cache inclui tenant?
- TESTE: 2 usuários em tenants diferentes — vazamento de dados?
- Jobs assíncronos carregam contexto do tenant?

AUTENTICAÇÃO PROFUNDA:
- JWT contém tenant_id? Sessão expira corretamente?
- Multi-dispositivo funciona? Logout invalida sessão?

RBAC:
- Papéis × recursos mapeados?
- Enforcement na API e na UI?
- TESTE: usuário comum tenta acessar admin?

FLUXOS COMPLETOS:
- Onboarding, uso diário, admin, tratamento de erro
- Cada jornada roda do início ao fim?

UX E ACESSIBILIDADE:
- Mensagens claras? Navegação por teclado? Contraste adequado?

Salve em etapa-02-arquitetural.md com severidade (🔴/🟠/🟡/🔵).

═══════════════════════════════════════════
ETAPA 3 — AUDITORIA DE SEGURANÇA (TUDO ESTÁ PROTEGIDO?)
═══════════════════════════════════════════
Objetivo: verificar se o sistema está blindado.

CÓDIGO (OWASP Top 10 + CWE Top 25):
- Injeção (SQL, NoSQL, comando)?
- Broken access control?
- Segredos hardcoded?
- XSS, SSRF, deserialização?
- Criptografia fraca?

DEPENDÊNCIAS:
- CVEs conhecidos? Versões desatualizadas?
- Dockerfiles inseguros?

INFRAESTRUTURA SELF-HOSTED:
- Supabase: RLS em todas as tabelas? SERVICE_ROLE_KEY protegida?
- n8n: admin token forte? webhooks autenticados? SSL?
- Cloudflare: WAF ativo? tokens com escopo mínimo?
- VPS: firewall ativo? SSH com chave? portas fechadas?

LLM/AGENTES (se aplicável):
- Prompt injection? Data leakage? Excessive agency?

Salve em etapa-03-seguranca.md com severidade.

═══════════════════════════════════════════
VEREDITO FINAL
═══════════════════════════════════════════
Consolide as 3 etapas em VEREDITO-FINAL.md:

1. **Nota geral**: A (pronto para produção) / B (pronto com ressalvas) / C (precisa de correções) / D (não pronto) / F (crítico)

2. **Resumo por etapa**:
   - Funcional: X% funcional, Y itens faltando
   - Arquitetural: Z problemas (🔴/🟠/🟡/🔵)
   - Segurança: W vulnerabilidades (🔴/🟠/🟡/🔵)

3. **BLOQUEADORES** (impedem deploy):
   Liste tudo que é 🔴 Crítico. Se houver algum, o veredito é automaticamente "NÃO PRONTO".

4. **Tabela consolidada de problemas**:
   | # | Problema | Etapa | Severidade | Área | Correção |

5. **Recomendação final**:
   - [ ] Pode ir para produção?
   - [ ] Precisa corrigir X antes?
   - [ ] Precisa refazer Y?

6. **Próximos passos** (o que corrigir primeiro, em ordem de impacto).

Ao terminar, imprima:
"🏁 AUDITORIA FINAL CONCLUÍDA — Nota: X — Bloqueadores: Y — Relatório: VEREDITO-FINAL.md"

INICIE AGORA PELA ETAPA 1. Execute as 3 etapas em sequência e entregue o veredito final.
