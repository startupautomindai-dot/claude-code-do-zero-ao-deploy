# INFRA DO ZERO — VPS, CLAUDE CODE, SUPABASE E N8N

Este arquivo é pra quem ainda não tem NADA disso — nem VPS, nem Claude
Code instalado, nem Supabase, nem n8n. Se você já tem tudo isso rodando,
pula direto pro 00-CONTEXTO-INFRAESTRUTURA.md.

═══════════════════════════════════════════
1. VPS — O QUE É E QUANTO CUSTA
═══════════════════════════════════════════

VPS é um servidor Linux só seu, ligado 24h, com um IP público. É onde
ficam Supabase, n8n e os sites/apps que você for colocar no ar. Acesso é
por SSH — terminal, sem interface gráfica.

Provedores comuns e faixa de preço (varia com câmbio e promoção, sempre
confirme o valor atual no site):

- Contabo — geralmente o mais barato, planos a partir de uns 5-6 EUR/mês
  já com boa quantidade de RAM.
- Hetzner — ótimo custo-benefício, também na faixa de 5-15 EUR/mês.
- Hostinger VPS — cobra em real, planos a partir de ~R$30-50/mês.
- DigitalOcean / Vultr / Linode — cobrança em dólar, droplets a partir de
  uns 5-6 USD/mês nos planos básicos.

Specs mínimas pra rodar Supabase self-hosted + n8n + alguns projetos ao
mesmo tempo: 2 vCPU / 4 GB RAM / 60-80 GB de disco (SSD). Supabase
self-hosted sozinho já sobe uns 8 containers (Postgres, Auth, Realtime,
Storage, Studio, Kong...), então RAM é o que mais aperta. Pra produção de
verdade, com clientes reais e vários projetos, 8 GB de RAM é bem mais
confortável — é o que a Automind roda hoje.

Sistema operacional: Ubuntu 22.04 LTS. É o mais documentado e o que todo
tutorial de Docker/Supabase/n8n assume.

### Passo a passo pra deixar a VPS pronta

1. Contrate a VPS, anote o IP e a senha (ou chave) que o provedor te der.
2. Acesse: `ssh root@IP-DA-VPS`
3. Atualize o sistema:

    apt update && apt upgrade -y

4. Instale Docker e Docker Compose (pré-requisito de tudo abaixo):

    curl -fsSL https://get.docker.com | sh

O Docker Compose v2 já vem junto (comando `docker compose`, sem hífen).

5. (Recomendado) configure firewall básico:

    ufw allow OpenSSH
    ufw allow 80
    ufw allow 443
    ufw enable

═══════════════════════════════════════════
2. CLAUDE CODE — COMO INSTALAR
═══════════════════════════════════════════

O Claude Code roda no SEU computador (Mac, Windows ou Linux), não na
VPS — ele executa comandos localmente, e usa SSH quando precisa mexer no
servidor.

### No Windows: use pelo Ubuntu (WSL), não pelo PowerShell/CMD

Dá pra instalar o Claude Code direto no Windows, mas na prática o jeito
que funciona melhor é rodar ele DENTRO do Ubuntu (WSL — o Linux que roda
dentro do Windows). Motivos:

- Arrastar imagem/print pra dentro do terminal funciona: o Claude Code
  recebe o arquivo e enxerga a imagem.
- Os comandos que ele roda (ssh, git, curl, docker) são os mesmos da VPS,
  que também é Ubuntu. Nada de adaptar comando pra PowerShell.
- Uma instalação só pra manter atualizada. Instalação duplicada (uma no
  Windows e outra no Ubuntu) é armadilha: a do Windows fica esquecida,
  desatualizada, e é aí que começa a cair ou a não mostrar modelo novo.

Instalar o Ubuntu no Windows (PowerShell como administrador, uma vez só):

    wsl --install -d Ubuntu

Reinicie o PC, abra o app "Ubuntu" (ou o Windows Terminal → aba Ubuntu),
crie usuário e senha. Daqui pra frente, TUDO abaixo é dentro do Ubuntu.

### Instalação (Ubuntu, Mac ou Linux)

Pré-requisito: Node.js 18 ou mais recente instalado.

    npm install -g @anthropic-ai/claude-code

Primeira execução (dentro da pasta do seu projeto):

    claude

Na primeira vez ele pede login — conta Claude.ai (Pro/Max) ou uma API key
do console.anthropic.com. Depois de logado uma vez, fica salvo.

### Manter atualizado (é o que libera modelo novo)

Modelo novo só aparece em versão nova do Claude Code. Antes de qualquer
sessão importante:

    claude --version
    claude update

### Usar o Opus 5.5 (modelo mais recente)

Dentro do Claude Code, digite:

    /model

e escolha Opus 5.5. A escolha fica salva como padrão pras próximas
sessões. Pra abrir já direto nele:

    claude --model claude-opus-5-5

Se o Opus 5.5 não aparecer na lista do /model: primeiro rode
`claude update` e abra de novo. Se mesmo atualizado não aparecer, confira
o plano da sua conta.

### Mandar print/imagem pro Claude Code

No Windows Terminal com a aba Ubuntu aberta, arraste o arquivo da imagem
pra dentro do terminal (o caminho do arquivo aparece no prompt) e escreva
sua pergunta junto. Ele abre a imagem e analisa — serve pra mostrar tela
com erro, layout que você quer copiar, print de conversa de cliente.

═══════════════════════════════════════════
3. SUPABASE SELF-HOSTED — COMO INSTALAR
═══════════════════════════════════════════

Instalação nova (na VPS, via SSH):

    git clone --depth 1 https://github.com/supabase/supabase
    cd supabase/docker
    cp .env.example .env

Abra o `.env` e gere os segredos pedidos (JWT secret, senha do Postgres,
ANON_KEY e SERVICE_ROLE_KEY) — o próprio repositório do Supabase tem um
guia de self-hosting com o passo de gerar essas chaves via JWT. Não suba
com os valores de exemplo do `.env.example`.

Depois:

    docker compose up -d

Isso sobe todos os serviços (Postgres, Auth, Storage, Realtime, Studio,
Kong como gateway da API). Por padrão, o Studio (painel) fica na porta
3000 e a API (Kong) na porta 8000 — pra ter um domínio bonito com HTTPS
em vez de `IP:porta`, configure nginx como proxy reverso na frente e
aponte um subdomínio pra ele (ver Etapa 9 do PASSO-A-PASSO-COMPLETO.md
pra DNS).

### Se a ideia é MIGRAR de Supabase Cloud pra self-hosted

Não é 1-click. O caminho:

1. No projeto Cloud, exporte o banco: `pg_dump` (a própria dashboard do
   Supabase Cloud tem a connection string pronta pra isso).
2. Suba o Supabase self-hosted (passos acima) primeiro, do zero.
3. Restaure o dump no Postgres self-hosted: `psql` ou `pg_restore`,
   apontando pra connection string do self-hosted.
4. Reconfigure Auth (provedores de login) e Storage (buckets) manualmente
   no painel self-hosted — essa parte não migra junto com o dump do banco.
5. Troque a `SUPABASE_URL`/`ANON_KEY`/`SERVICE_ROLE_KEY` no projeto pras
   novas, do self-hosted, e teste tudo de novo antes de desligar o Cloud.

═══════════════════════════════════════════
4. N8N — COMO INSTALAR
═══════════════════════════════════════════

Mais simples que o Supabase — um único container.

Teste rápido (não é o setup de produção):

    docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n

Pra produção de verdade (domínio próprio, HTTPS, acessível de fora),
suba via `docker-compose.yml` com essas variáveis de ambiente:

    N8N_HOST=seu-subdominio.seudominio.com.br
    N8N_PROTOCOL=https
    WEBHOOK_URL=https://seu-subdominio.seudominio.com.br/
    GENERIC_TIMEZONE=America/Sao_Paulo

E, como no Supabase, nginx como proxy reverso na frente + DNS apontado
pro subdomínio (Etapa 9 do PASSO-A-PASSO-COMPLETO.md).

Depois que estiver no ar:

1. Acesse o domínio, crie o usuário owner (primeiro acesso).
2. Vá em Settings → n8n API → Create an API key.
3. Essa API key é a que o 00b-ACESSO-CLAUDE-CODE.md usa pra dar acesso ao
   Claude Code.

═══════════════════════════════════════════
5. ORDEM RECOMENDADA PRA QUEM COMEÇA DO ZERO
═══════════════════════════════════════════

1. Contratar a VPS e instalar Docker (seção 1).
2. Instalar o Claude Code no seu computador (seção 2).
3. Subir Supabase self-hosted na VPS (seção 3).
4. Subir n8n na VPS (seção 4).
5. Seguir pro 00-CONTEXTO-INFRAESTRUTURA.md e 00b-ACESSO-CLAUDE-CODE.md
   pra dar ao Claude Code o acesso de verdade a tudo isso.
6. Só então começar a Etapa 1 (DeepSeek) do PASSO-A-PASSO-COMPLETO.md.

═══════════════════════════════════════════
FIM DO ARQUIVO
═══════════════════════════════════════════
