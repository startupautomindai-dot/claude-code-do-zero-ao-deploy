Prompts mais usados por profissionais de cybersecurity (para usar com Claude Code)
Com base nas bibliotecas de prompts especializadas, aqui estão os prompts que auditores de segurança mais utilizam:

Cenário	Prompt	Fonte
Auditoria de PC/Servidor	"Você é um engenheiro de cybersecurity elite. Pense como um atacante patrocinado por Estado-nação. Faça uma auditoria full-spectrum desta máquina."	Journal du Net
Auditoria de código-fonte	"Você é um auditor de código especializado em cybersegurança aplicativa. Analise estaticamente cada variável, função, import e configuração. Busque OWASP Top 10, CWE Top 25 e falhas lógicas."	Journal du Net
Verificação de MCP Server	"Estou prestes a instalar um MCP server que fala com Stripe. Me guie pelo que verificar antes de conceder acesso de escrita."	Claude Security Skills
Prompt Injection Defense	"Estou construindo um agente de suporte que lê e-mails e pode responder. Como prevenir ataques de injeção?"	Claude Security Skills
Auditoria de RAG	"Nosso chatbot RAG indexa toda a wiki da empresa. Usuários estão vendo conteúdo de documentos que não têm acesso. Corrija o design."	Claude Security Skills
OWASP LLM Top 10	"Quero implementar o OWASP LLM Top 10 no nosso app. Por onde começo?"	Claude Security Skills
Auditoria de Dockerfile	"Revise este Dockerfile: running como root, :latest, curl | sh, segredos embutidos."	NovaCode37
Como instalar as skills de segurança no Claude Code
Para ter acesso a essas capacidades, clone o repositório (não existe pacote
npm oficial com esse nome — não rode `npm install -g claude-security-skills`,
qualquer um pode registrar esse nome):

bash
# No terminal, fora do Claude Code
git clone https://github.com/NovaCode37/claude-security-skills.git

Antes de instalar qualquer skill de terceiro, leia o conteúdo: uma skill é
instrução que o Claude Code vai seguir com o seu acesso.
Depois, dentro do Claude Code, basta pedir em linguagem natural:

text
> audite meu projeto para segredos expostos
> verifique os headers HTTP do meu site
> inspecione este JWT
> red-team meu agente LLM para prompt injection
O Claude Code identifica automaticamente a skill adequada e a executa.

Checklist final de segurança (para incluir no CLAUDE.md do projeto)
□ CLAUDE.md inclui a seção de segurança com os comandos /security-review e skills instaladas
□ context/for-agent/08-security.md gerado pelo agente do Claude Projects com o passo a passo da FASE 7
□ .claude/commands/security-audit.md criado como slash command reutilizável
□ Segredos (.env, tokens, chaves) NUNCA commitados — verificar .gitignore
□ Supabase: RLS habilitado em todas as tabelas, SERVICE_ROLE_KEY só server-side
□ n8n: ADMIN_TOKEN forte, webhooks autenticados, SSL ativo
□ Cloudflare: WAF ativo, tokens com escopo mínimo
□ VPS: firewall configurado, SSH com chave, portas desnecessárias fechadas
□ /security-review executado e todos os achados críticos/altos corrigidos
□ Relatório de auditoria salvo em work-log/security-audit-YYYY-MM-DD.md
