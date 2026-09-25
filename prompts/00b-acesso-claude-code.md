# DAR ACESSO DE INFRAESTRUTURA AO CLAUDE CODE

Este arquivo é diferente do 00-CONTEXTO-INFRAESTRUTURA.md. Aquele descreve
O QUE existe. Este ensina COMO fazer o Claude Code (rodando no seu terminal)
realmente enxergar e mexer em cada serviço — GitHub, VPS, Cloudflare, n8n,
Supabase — sem você ter que copiar e colar comando por comando toda vez.

Regra de ouro: o Claude Code roda comandos no seu terminal. Qualquer coisa
que você mesmo consegue fazer pelo terminal (SSH, curl, gh, git), ele
também consegue — desde que a credencial exista no ambiente onde ele roda.
Nenhum segredo vai para o código nem para o Git. Sempre variável de
ambiente local ou `.env` fora do repositório.

═══════════════════════════════════════════
1. GITHUB
═══════════════════════════════════════════

Pra que serve: o Claude Code faz commit, push, cria branch por fase e
(se pedido) abre Pull Request.

Como configurar (uma vez só, no seu computador):

    Instale o GitHub CLI e rode:
    gh auth login

Siga o fluxo (escolhe GitHub.com, HTTPS, abre o navegador, autoriza).
Isso salva a sessão localmente — o Claude Code usa a mesma sessão do
terminal, não precisa de token separado nem de MCP pra isso funcionar.

Teste:

    gh auth status
    git remote -v

Se aparecer "Logged in" e o remote do projeto, está pronto.

═══════════════════════════════════════════
2. VPS (servidor Linux)
═══════════════════════════════════════════

Pra que serve: o Claude Code faz deploy, sobe container, edita nginx,
reinicia serviço — tudo via SSH, igual você faria na mão.

Como configurar:

    ssh-keygen -t ed25519 -C "seu-email"
    ssh-copy-id usuario@IP-DA-VPS

Se `ssh-copy-id` não estiver disponível, cole o conteúdo de
`~/.ssh/id_ed25519.pub` dentro de `~/.ssh/authorized_keys` no servidor,
manualmente.

Opcional (recomendado): salve um atalho em `~/.ssh/config`:

    Host minha-vps
        HostName IP-DA-VPS
        User usuario
        IdentityFile ~/.ssh/id_ed25519

Assim o Claude Code (e você) usa só `ssh minha-vps` em vez do IP inteiro.

Teste:

    ssh minha-vps "echo conectado"

═══════════════════════════════════════════
3. CLOUDFLARE
═══════════════════════════════════════════

Pra que serve: criar/editar registro DNS do subdomínio, configurar Pages,
gerenciar regras de borda.

Como configurar:

1. dash.cloudflare.com → ícone de perfil → API Tokens → Create Token
2. Use o template "Edit zone DNS" (ou customizado com o escopo mínimo
   necessário: Zone → DNS → Edit, Zone → Zone → Read), restrito à zona
   (domínio) do projeto.
3. Guarde o token gerado como variável de ambiente local, nunca no código:

    export CF_API_TOKEN="cole-o-token-aqui"

(coloque essa linha no seu `~/.zshrc`/`~/.bashrc`, ou num `.env` local que
não vai pro Git, e carregue antes de abrir o Claude Code)

Com isso, o Claude Code chama a API da Cloudflare via `curl` usando essa
variável — não precisa de MCP para o básico de DNS. Se você já tem o MCP
server da Cloudflare configurado, ele também funciona e é mais direto
(comandos nativos em vez de montar curl na mão).

Teste:

    curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
      https://api.cloudflare.com/client/v4/user/tokens/verify

Deve responder `"success":true`.

═══════════════════════════════════════════
4. N8N
═══════════════════════════════════════════

Pré-requisito importante: a instância do n8n precisa JÁ EXISTIR e estar
rodando (self-hosted via Docker, ou n8n Cloud). A API key sozinha não cria
a instância — ela só dá acesso a uma instância que já está no ar.

Como configurar:

1. Dentro do n8n: Settings → n8n API → Create an API key.
2. Guarde a URL da instância e a key como variável de ambiente local:

    export N8N_URL="https://seu-n8n.dominio.com"
    export N8N_API_KEY="cole-a-key-aqui"

Com isso o Claude Code cria/edita workflow via `curl` na API REST do n8n
(GET/PUT em `/api/v1/workflows`). Se tiver o MCP server do n8n configurado,
ele consegue criar workflow descrevendo em linguagem natural, sem montar
o JSON manualmente.

Teste:

    curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_URL/api/v1/workflows" | head -c 200

Deve devolver uma lista (mesmo que vazia) em JSON, não erro 401.

═══════════════════════════════════════════
5. SUPABASE
═══════════════════════════════════════════

Como configurar: pegue na dashboard do projeto (ou no painel self-hosted)

    export SUPABASE_URL="https://seu-projeto.supabase.co"
    export SUPABASE_ANON_KEY="chave-publica-aqui"
    export SUPABASE_SERVICE_ROLE_KEY="chave-privada-aqui"

A ANON_KEY pode ir pro frontend. A SERVICE_ROLE_KEY NUNCA — fica só na
variável de ambiente local/backend, nunca em código versionado.

Teste:

    curl -s "$SUPABASE_URL/rest/v1/" -H "apikey: $SUPABASE_ANON_KEY"

═══════════════════════════════════════════
6. E-MAIL / SMTP
═══════════════════════════════════════════

Guarde host, porta, usuário e senha como variáveis de ambiente
(`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`). Só é usado
server-side (edge function / backend), nunca no frontend.

═══════════════════════════════════════════
7. ONDE GUARDAR TUDO ISSO NA PRÁTICA
═══════════════════════════════════════════

- Nunca dentro do código do projeto nem commitado no Git.
- Um `.env` local (na pasta do projeto, listado no `.gitignore`) ou
  exportado no `~/.zshrc`/`~/.bashrc` do seu computador.
- O Claude Code herda as variáveis de ambiente do terminal onde ele foi
  aberto — se a variável existe no shell, ele já enxerga, sem configuração
  extra.
- Se usar MCP servers (Cloudflare, n8n, Supabase, GitHub), as credenciais
  ficam no `.mcp.json` do projeto — esse arquivo também nunca vai pro Git.

═══════════════════════════════════════════
8. PROMPT PRONTO — TESTE TUDO DE UMA VEZ
═══════════════════════════════════════════

Depois de configurar o que precisar, abra o Claude Code na pasta do
projeto e cole:

    Preciso que você confirme o acesso a cada serviço abaixo antes de
    começarmos. Teste um por um, na ordem, e me diga o resultado de cada
    (✅ funcionou / ❌ erro, qual / ⚠️ não configurei ainda):

    1. GitHub — rode: gh auth status && git remote -v
    2. VPS — rode: ssh minha-vps "echo conectado"
       (troque "minha-vps" pelo host configurado em ~/.ssh/config)
    3. Cloudflare — rode: curl -s -H "Authorization: Bearer $CF_API_TOKEN"
       https://api.cloudflare.com/client/v4/user/tokens/verify
    4. n8n — rode: curl -s -H "X-N8N-API-KEY: $N8N_API_KEY"
       "$N8N_URL/api/v1/workflows" | head -c 200
    5. Supabase — rode: curl -s "$SUPABASE_URL/rest/v1/"
       -H "apikey: $SUPABASE_ANON_KEY"

    No final, me dê um resumo: o que está pronto e o que eu preciso
    configurar antes de seguirmos para a Etapa 1.

Só avance para a Etapa 1 (DeepSeek) depois que todos os serviços que o
seu projeto vai usar estiverem ✅.

═══════════════════════════════════════════
FIM DO ARQUIVO
═══════════════════════════════════════════
