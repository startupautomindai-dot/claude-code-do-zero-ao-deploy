# CONTEXTO DE INFRAESTRUTURA — LEIA ANTES DE INICIAR QUALQUER PROJETO

Este documento descreve o ambiente técnico já disponível para o Claude Code.
Deve ser lido ANTES de gerar qualquer rascunho, especificação ou código.
Toda decisão técnica deve respeitar o que já existe aqui. NÃO invente
infraestrutura que não está nesta lista sem justificar.

═══════════════════════════════════════════
1. O QUE O CLAUDE CODE JÁ TEM ACESSO
═══════════════════════════════════════════

O Claude Code já está conectado aos serviços abaixo. Não é necessário
configurar do zero, criar conta nova ou instalar nada nesses serviços.

### 1.1 GITHUB
- Acesso: ✅ Configurado
- O que pode fazer: criar repositórios, commit, push, pull, branches, PRs
- Uso esperado: versionamento do código, histórico de alterações, deploy via CI/CD
- Observação: sempre criar branch por fase (`feat/fase-01-banco`), nunca commitar direto na main

### 1.2 VPS (Servidor Linux)
- Acesso: ✅ Configurado
- O que pode fazer: SSH, instalar pacotes, rodar serviços, configurar firewall
- Uso esperado: hospedar serviços self-hosted (Supabase, n8n), rodar containers Docker
- Observação: todas as ações devem ser documentadas em `work-log/vps/`

### 1.3 SUPABASE (Cloud ou Self-Hosted)
- Acesso: ✅ Configurado
- Modo: [ ] Cloud  [ ] Self-Hosted (marcar qual)
- O que pode fazer: criar tabelas, RLS, edge functions, buckets, gerenciar auth
- Uso esperado: banco de dados, autenticação, storage, realtime
- Observação: RLS habilitado em TODAS as tabelas, sem exceção. SERVICE_ROLE_KEY só server-side.

### 1.4 N8N (Self-Hosted)
- Acesso: ✅ Configurado
- Versão mínima: 2.14.1 (para suportar Instance-level MCP)
- O que pode fazer: criar workflows, configurar webhooks, integrar APIs
- Uso esperado: automações, integrações entre sistemas, jobs agendados
- Observação: webhooks sempre autenticados, nunca expor URL pública sem token

### 1.5 CLOUDFLARE
- Acesso: ✅ Configurado
- O que pode fazer: DNS, SSL, WAF, Pages, Workers, R2
- Uso esperado: domínio, deploy de frontend estático, proteção de borda
- Observação: WAF ativo, tokens de API com escopo mínimo

### 1.6 E-MAIL
- Acesso: ✅ Configurado
- O que pode fazer: enviar e-mails transacionais (boas-vindas, reset de senha, confirmações)
- Uso esperado: fluxos de autenticação, notificações, alertas
- Observação: nunca expor credenciais SMTP no frontend

### 1.7 MCP SERVERS JÁ CONFIGURADOS
O Claude Code já possui os seguintes MCP servers ativos:
- [ ] Supabase (leitura de schema, migrations, auth)
- [ ] n8n (criação de workflows via linguagem natural)
- [ ] Cloudflare (deploy, DNS, variáveis)
- [ ] GitHub (repositórios, PRs)
- [ ] Outros: _______________________

═══════════════════════════════════════════
2. O QUE VOCÊ (USUÁRIO) PRECISA TER EM MÃOS
═══════════════════════════════════════════

Antes de iniciar qualquer projeto, tenha estas informações prontas:

### 2.1 Credenciais e Acessos
- [ ] Token de API do GitHub (com escopo de repo)
- [ ] Chave SSH ou senha da VPS
- [ ] URL do Supabase + ANON_KEY + SERVICE_ROLE_KEY
- [ ] URL do n8n + API key (se aplicável)
- [ ] Token de API do Cloudflare (com escopo de DNS + Pages)
- [ ] Credenciais SMTP (host, porta, usuário, senha)

### 2.2 Informações do Projeto
- [ ] Nome do projeto
- [ ] Domínio desejado (ex: meusistema.com.br)
- [ ] Descrição em 1 parágrafo do que o sistema faz
- [ ] Público-alvo
- [ ] Funcionalidades obrigatórias do MVP (lista)
- [ ] Funcionalidades desejadas para o futuro (lista)

### 2.3 Decisões que precisam ser tomadas ANTES de começar
- [ ] É multi-tenant (vários clientes) ou single-tenant (um cliente)?
- [ ] Tem área administrativa? Quem acessa?
- [ ] Precisa de integração com sistemas externos?
- [ ] Precisa de automações (n8n)? Quais?
- [ ] Precisa de pagamentos? Qual gateway?
- [ ] Vai ter app mobile ou só web?

═══════════════════════════════════════════
3. REGRAS DE OURO (VÁLIDAS PARA TODOS OS PROJETOS)
═══════════════════════════════════════════

1. NUNCA commitar segredos (`.env`, tokens, chaves). Sempre no `.gitignore`.
2. SEMPRE habilitar RLS no Supabase, mesmo em tabelas "pequenas".
3. SEMPRE autenticar webhooks do n8n. Nunca expor URL sem token.
4. SEMPRE separar dados por tenant (coluna `tenant_id` + índice + RLS).
5. SEMPRE tratar estados de UI: loading, vazio, erro, sucesso.
6. SEMPRE confirmar antes de ações destrutivas (excluir, desativar).
7. SEMPRE documentar decisões em `work-log/` para auditoria futura.
8. NUNCA rodar migrations direto em produção. Sempre branch primeiro.
9. SEMPRE usar HTTPS. Cloudflare fornece SSL gratuito — usar.
10. SEMPRE fazer backup do Supabase antes de migrations grandes.

═══════════════════════════════════════════
4. COMO USAR ESTE ARQUIVO
═══════════════════════════════════════════

Este arquivo deve ser enviado JUNTO com o rascunho do projeto para o
DeepSeek e para o Claude Projects. Ele garante que:

- O rascunho não invente infraestrutura que você não tem
- As decisões técnicas respeitem o que já está configurado
- O Claude Code não perca tempo perguntando o que já sabe
- Nenhuma credencial precise ser repetida a cada etapa

Fluxo recomendado:
1. Ler este arquivo
2. Preencher as seções 1.7, 2.1, 2.2 e 2.3
3. Anexar este arquivo ao prompt do DeepSeek
4. Anexar este arquivo + rascunho do DeepSeek ao Claude Projects
5. Anexar este arquivo ao workspace do Claude Code (em `context/reference/infra.md`)

═══════════════════════════════════════════
5. DICAS INICIAIS ANTES DE ENVIAR PARA O DEEPSEEK
═══════════════════════════════════════════

- Descreva o projeto em linguagem natural, sem se preocupar com termos técnicos
- Diga o que o sistema FAZ, não como ele deve ser construído
- Liste as funcionalidades que você quer, mesmo as que pareçam óbvias
- Mencione se é para uso próprio ou para vender para clientes
- Diga se já tem domínio registrado
- Diga se já tem identidade visual (logo, cores) ou se precisa criar
- Anexe este arquivo de contexto junto com a descrição

O DeepSeek vai usar este contexto para gerar um rascunho que respeita
sua infraestrutura real, sem sugerir ferramentas que você não usa.

═══════════════════════════════════════════
FIM DO ARQUIVO
═══════════════════════════════════════════
