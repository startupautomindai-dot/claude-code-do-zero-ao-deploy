# 📘 PASSO-A-PASSO-COMPLETO.md

**Como usar os arquivos da live — do zero ao deploy**

**Versão:** 1.0
**Última atualização:** Setembro/2026

---

## 📋 VISÃO GERAL

Este documento ensina você a usar os arquivos de prompt desta live para construir qualquer sistema, aplicativo ou SaaS do zero até o deploy.

O fluxo usa **3 ferramentas em sequência**:

DEEPSEEK → CLAUDE PROJECTS → CLAUDE CODE
(pensa)     (traduz)          (executa)

Você não precisa saber programar. Só precisa seguir a ordem dos arquivos e colar cada um no lugar certo.

---

## 🎯 O QUE VOCÊ VAI PRECISAR

### Arquivos (todos estão na pasta PROMPTS-LIVE/)

| Arquivo | Para que serve |
|---|---|
| 00a-INFRA-DO-ZERO.md | Pra quem não tem nada ainda: VPS (preços e specs), instalar Claude Code, Supabase self-hosted, n8n |
| 00-CONTEXTO-INFRAESTRUTURA.md | Descreve seu ambiente (GitHub, VPS, Supabase, n8n, Cloudflare, e-mail) |
| 00b-ACESSO-CLAUDE-CODE.md | Ensina a dar acesso de verdade a cada serviço (GitHub, VPS, Cloudflare, n8n, Supabase) e traz um prompt pra testar tudo |
| 01-PROMPT-DEEPSEEK.md | Instrução para o DeepSeek gerar o rascunho |
| 02-ARQUITETO-SENIOR-REFORMULADOR.md | Instrução para o Claude reformular o rascunho |
| 03-PROMPT-CLAUDE-IA.md | Instrução para o Claude gerar o workspace do Claude Code |
| 04-VALIDACAO-FUNCIONAL-PRE-VISTORIA.md | Testa se tudo funciona antes da auditoria |
| 05-VISTORIA-SEM-CORRIGIR.md | Audita a arquitetura sem alterar nada |
| 05-VISTORIA-COM-CORRECAO.md | Audita e corrige automaticamente |
| 06-PROMPT-SEGURANCA.md | Audita vulnerabilidades de segurança |
| 07-AUDITORIA-GERAL-FINAL.md | Dá o veredito final (pronto ou não para produção) |
| 08-PROMPT-MAIS-USADOS.md | Biblioteca de consulta (não faz parte do fluxo) |

### Credenciais que você precisa ter em mãos

- Token do GitHub
- Chave SSH da VPS
- URL do Supabase + ANON_KEY + SERVICE_ROLE_KEY
- URL do n8n + API key
- Token do Cloudflare
- Credenciais SMTP (e-mail)

### Ferramentas

- DeepSeek → chat.deepseek.com
- Claude Projects → claude.ai → Projects
- Claude Code → terminal no seu computador (no Windows: dentro do Ubuntu/WSL, versão atualizada, modelo Opus 5.5 — ver 00a-INFRA-DO-ZERO.md)
- Git → para versionar o código

### Tempo estimado

- Preparação: 10 min
- Fluxo completo: 90 min a 3h (depende do tamanho do projeto)

---

## 📁 ESTRUTURA DA SUA PASTA DE PROMPTS

Antes de começar, sua pasta PROMPTS-LIVE/ deve estar assim:

PROMPTS-LIVE/
├── 00a-INFRA-DO-ZERO.md
├── 00-CONTEXTO-INFRAESTRUTURA.md
├── 00b-ACESSO-CLAUDE-CODE.md
├── 01-PROMPT-DEEPSEEK.md
├── 02-ARQUITETO-SENIOR-REFORMULADOR.md
├── 03-PROMPT-CLAUDE-IA.md
├── 04-VALIDACAO-FUNCIONAL-PRE-VISTORIA.md
├── 05-VISTORIA-SEM-CORRIGIR.md
├── 05-VISTORIA-COM-CORRECAO.md
├── 06-PROMPT-SEGURANCA.md
├── 07-AUDITORIA-GERAL-FINAL.md
├── 08-PROMPT-MAIS-USADOS.md
└── GUIA-DE-USO.md

---

## 🚀 ETAPA 0 — PREPARAÇÃO (10 min)

### Passo 0.0 — Não tem VPS, Supabase ou n8n ainda?

Se você não tem nada disso rodando, comece pelo 00a-INFRA-DO-ZERO.md —
ele ensina a contratar a VPS (com faixa de preço), instalar o Claude Code,
subir Supabase self-hosted e subir o n8n. Só depois disso volte pra cá.

### Passo 0.1 — Abra o 00-CONTEXTO-INFRAESTRUTURA.md

Leia o arquivo e marque o que você já tem:

- [ ] GitHub ✅
- [ ] VPS ✅
- [ ] Supabase self-hosted ✅
- [ ] n8n self-hosted ✅
- [ ] Cloudflare ✅
- [ ] E-mail ✅
- [ ] MCP servers configurados ✅

### Passo 0.2 — Tenha as credenciais à mão

Separe em um bloco de notas os tokens e chaves listados acima. Você vai precisar deles durante o fluxo.

### Passo 0.3 — Escolha o projeto

Decida o que vai construir. Exemplos:

- Sistema de agendamento
- CRM simples
- Dashboard de vendas
- Plataforma de cursos
- App de finanças pessoais

### Passo 0.4 — Dê acesso de verdade ao Claude Code

Ter a credencial anotada não é a mesma coisa que o Claude Code conseguir usá-la. Abra o 00b-ACESSO-CLAUDE-CODE.md e siga a configuração de cada serviço que seu projeto vai precisar (GitHub, VPS, Cloudflare, n8n, Supabase). No final desse arquivo tem um prompt pronto pra colar no Claude Code e testar tudo de uma vez, antes de seguir pra Etapa 1.

---

## 🧠 ETAPA 1 — IDEAÇÃO NO DEEPSEEK (10 min)

**Objetivo:** gerar o rascunho do projeto.

### Passo 1.1 — Abra o DeepSeek

Acesse chat.deepseek.com e crie um novo chat.

### Passo 1.2 — Cole o arquivo 01-PROMPT-DEEPSEEK.md

Abra o arquivo, copie TODO o conteúdo e cole no chat. Envie.

O DeepSeek vai responder algo como: "Entendido. Descreva seu projeto."

### Passo 1.3 — Anexe o 00-CONTEXTO-INFRAESTRUTURA.md

Clique no clipe 📎 e anexe o arquivo.

### Passo 1.4 — Descreva o projeto

No mesmo campo de mensagem, escreva algo assim:

Com base no contexto de infraestrutura anexo, gere o rascunho do
projeto seguindo o formato padrão.

PROJETO: Sistema de agendamento para clínicas

Descrição:
Quero construir um sistema que permita pacientes agendarem
consultas online e clínicas gerenciarem horários pelo painel.
É multi-tenant. Preciso de autenticação, notificações por email
e integração com Google Calendar.

Funcionalidades do MVP:
- Cadastro de clínicas
- Cadastro de profissionais
- Agenda com horários disponíveis
- Agendamento online
- Painel administrativo
- Notificações por email

Envie.

### Passo 1.5 — Responda às perguntas

O DeepSeek vai fazer até 3 perguntas para esclarecer. Responda.

### Passo 1.6 — Salve o briefing

O DeepSeek gera um briefing estruturado em Markdown. Copie tudo e salve como:

BRIEFING-DEEPSEEK.md

✅ Etapa 1 concluída.

---

## 🏗️ ETAPA 2 — REFORMULAÇÃO NO CLAUDE PROJECTS (10 min)

**Objetivo:** transformar o rascunho em uma especificação completa, sem lacunas.

### Passo 2.1 — Crie um novo Project

Acesse claude.ai → Projects → New Project.
Nome sugerido: Arquiteto de Sistemas.

### Passo 2.2 — Cole as Custom Instructions

Abra o 02-ARQUITETO-SENIOR-REFORMULADOR.md, copie TODO o conteúdo e cole em Custom Instructions do Project.

### Passo 2.3 — Anexe os arquivos de conhecimento

Em Project Knowledge, clique em "Add content" e anexe:

- 00-CONTEXTO-INFRAESTRUTURA.md
- BRIEFING-DEEPSEEK.md

### Passo 2.4 — Peça a reformulação

No chat do Project, envie:

Gere a especificação reformulada completa para este projeto,
seguindo o formato do prompt e preenchendo TODAS as lacunas
(menus, botões, CRUDs, configurações, estados de UI).

### Passo 2.5 — Salve a especificação

O Claude vai gerar uma especificação completa. Copie tudo e salve como:

ESPECIFICACAO-REFORMULADA.md

✅ Etapa 2 concluída.

---

## 📁 ETAPA 3 — WORKSPACE DO CLAUDE CODE (10 min)

**Objetivo:** gerar a pasta que o Claude Code vai ler.

### Passo 3.1 — Crie um novo Project (ou use o mesmo)

Nome sugerido: Tradutor de Workspace.

### Passo 3.2 — Cole as Custom Instructions

Abra o 03-PROMPT-CLAUDE-IA.md, copie TODO o conteúdo e cole em Custom Instructions.

### Passo 3.3 — Anexe os arquivos

Em Project Knowledge, anexe:

- 00-CONTEXTO-INFRAESTRUTURA.md
- ESPECIFICACAO-REFORMULADA.md

### Passo 3.4 — Peça o workspace

No chat, envie:

Gere o workspace completo do Claude Code para este projeto.
Inclua CLAUDE.md, context/for-agent/, context/reference/,
.claude/commands/, .mcp.json e CHECKLIST.md.

### Passo 3.5 — Crie a pasta do projeto no seu computador

No disco, crie esta estrutura:

meu-projeto/
├── CLAUDE.md
├── CHECKLIST.md
├── .mcp.json
├── context/
│   ├── for-agent/
│   └── reference/
├── .claude/
│   ├── commands/
│   └── agents/
├── work-log/
└── planning/

### Passo 3.6 — Salve cada arquivo no lugar certo

O Claude vai gerar os arquivos um por um. Para cada bloco:

1. Copie o conteúdo
2. Salve no caminho indicado pelo CHECKLIST.md gerado

Salve também uma cópia do 00-CONTEXTO-INFRAESTRUTURA.md em:

meu-projeto/context/reference/00-contexto-infraestrutura.md

### Passo 3.7 — (Opcional, recomendado) Desenhe o frontend antes de construir

Antes de mandar o Claude Code construir, vale ver o visual primeiro.

Abra um chat novo em claude.ai (fora do Project, não precisa ser no mesmo). Descreva a tela principal do sistema — cores, estilo, referências de site que você gosta — e peça pro Claude gerar um Artifact (HTML ou React) com o layout. Ajuste ali mesmo no chat até aprovar o visual.

Quando for para a Etapa 4, cole o código do Artifact aprovado junto com o pedido de construção:

Use este Artifact como padrão visual e construa o frontend a
partir dele (mesma paleta, tipografia e layout):

[cole aqui o código do Artifact]

Isso evita que o Claude Code invente um visual genérico — ele constrói em cima do design que você já aprovou.

✅ Etapa 3 concluída.

---

## ⚙️ ETAPA 4 — CONSTRUÇÃO NO CLAUDE CODE (25 min+)

**Objetivo:** construir o sistema fase por fase.

### Passo 4.1 — Abra o terminal

No Windows: abra o Ubuntu (Windows Terminal → aba Ubuntu). Não use
PowerShell/CMD — pelo Ubuntu você consegue arrastar prints pra dentro do
Claude Code, e os comandos são os mesmos da VPS.

cd caminho/para/meu-projeto

### Passo 4.2 — Atualize e inicie o Claude Code

claude update
claude

Dentro dele, rode /model e confirme que está no Opus 5.5 (fica salvo
como padrão depois da primeira escolha). Se não aparecer na lista, a
versão está velha — rode claude update de novo.

### Passo 4.3 — Confirme que ele leu o workspace

Envie:

Leia o CLAUDE.md e o CHECKLIST.md e me diga qual é a ordem
das fases e o que devo fazer primeiro.

### Passo 4.4 — Construa fase por fase

Para CADA fase, envie um comando. Exemplo:

Execute a FASE 0 (setup) conforme descrito em
context/for-agent/01-setup.md

Depois:

Execute a FASE 1 (banco de dados) conforme
context/for-agent/02-database.md

Continue até a última fase (deploy).

💡 Dica de ouro: entre cada fase, rode /clear para limpar o contexto. Isso economiza MUITOS tokens.

✅ Etapa 4 concluída.

---

## ✅ ETAPA 5 — VALIDAÇÃO FUNCIONAL (8 min)

**Objetivo:** testar se tudo existe e funciona.

### Passo 5.1 — Ainda no Claude Code, cole o 04-VALIDACAO-FUNCIONAL-PRE-VISTORIA.md

Abra o arquivo, copie TODO o conteúdo e cole no chat do Claude Code.

### Passo 5.2 — Aguarde o relatório

O Claude Code vai testar tudo e salvar em:

work-log/validacao/RELATORIO-VALIDACAO.md

### Passo 5.3 — Leia o resultado

- ✅ Presente e funcional
- ⚠️ Presente mas com problema
- ❌ Ausente

### Passo 5.4 — Corrija o que falta

Envie:

Corrija os itens ❌ e ⚠️ do RELATORIO-VALIDACAO.md.

✅ Etapa 5 concluída.

---

## 🔍 ETAPA 6 — VISTORIA ARQUITETURAL (10 min)

**Objetivo:** auditar banco, auth, RBAC, fluxos, UX.

### Passo 6.1 — Escolha o modo

**Modo A — Diagnóstico primeiro (recomendado):**
Cole o conteúdo de 05-VISTORIA-SEM-CORRIGIR.md.

**Modo B — Auditar e corrigir direto:**
Cole o conteúdo de 05-VISTORIA-COM-CORRECAO.md.

### Passo 6.2 — Aguarde o relatório

Salvo em:

work-log/auditoria/RELATORIO-FINAL.md

### Passo 6.3 — Se escolheu o Modo A, decida o que corrigir

Leia o relatório e envie:

Corrija os itens #F1-03, #F1-07, #F2-01 do RELATORIO-FINAL.md.

✅ Etapa 6 concluída.

---

## 🔒 ETAPA 7 — AUDITORIA DE SEGURANÇA (8 min)

**Objetivo:** auditar vulnerabilidades e hardening.

### Passo 7.1 — Ainda no Claude Code, cole o 06-PROMPT-SEGURANCA.md

### Passo 7.2 — Aguarde o relatório

Salvo em:

work-log/security-audit-AAAA-MM-DD.md

### Passo 7.3 — Corrija o que for crítico

Envie:

Corrija todos os itens 🔴 Crítico e 🟠 Alto do relatório de segurança.

✅ Etapa 7 concluída.

---

## 🏁 ETAPA 8 — VEREDITO FINAL (4 min)

**Objetivo:** receber a nota final do sistema (A–F).

### Passo 8.1 — Cole o 07-AUDITORIA-GERAL-FINAL.md

### Passo 8.2 — Aguarde o veredito

Salvo em:

work-log/auditoria-final/VEREDITO-FINAL.md

### Passo 8.3 — Leia a nota

| Nota | Significado |
|---|---|
| A | Pronto para produção ✅ |
| B | Pronto com ressalvas ⚠️ |
| C | Corrigir antes de subir 🛑 |
| D/F | Não subir — corrigir tudo 🔴 |

### Passo 8.4 — Se houver bloqueadores

Envie:

Corrija todos os BLOQUEADORES listados em VEREDITO-FINAL.md.

✅ Etapa 8 concluída.

---

## 🚀 ETAPA 9 — DEPLOY (opcional na live)

**Objetivo:** colocar em produção.

### Passo 9.1 — Commit final

git add .
git commit -m "feat: sistema completo validado e auditado"
git push origin main

### Passo 9.2 — Deploy do frontend

Faça o deploy do frontend no Cloudflare Pages seguindo
context/for-agent/07-deploy.md

### Passo 9.3 — Deploy do backend (se aplicável)

Depende da stack: VPS via SSH, Supabase edge functions ou Cloudflare Workers.

### Passo 9.4 — Configure o domínio

Duas situações possíveis, dependendo do que você já tem:

**A) Você já tem um domínio na Cloudflare e só quer um subdomínio novo pro projeto**
(caso mais comum — reaproveitar um domínio que já existe)

1. No painel da Cloudflare, abra o domínio → DNS → Add record.
2. Tipo A (aponta pro IP da VPS) ou CNAME (aponta pra outro serviço, ex: Cloudflare Pages).
3. Nome: o subdomínio escolhido (ex: meuprojeto).
4. Proxy status: ativado (nuvem laranja) se quiser o Cloudflare na frente.
5. Salve — geralmente propaga na hora.

**B) Você não tem nenhum domínio ainda**

1. Registre um domínio (ex: .com.br no Registro.br, ou .com em qualquer registrador).
2. Crie o site na Cloudflare (Add a site) e copie os 2 nameservers que ela dá.
3. Cole esses nameservers no painel do registrador onde o domínio foi comprado.
4. Espere propagar (Cloudflare avisa por e-mail quando ativa — minutos a poucas horas).
5. Com o domínio ativo na Cloudflare, siga o caminho A acima pra criar o registro.

### Passo 9.5 — Ative o n8n (se aplicável)

Configure os workflows do n8n descritos em
context/for-agent/06-automations.md

### Passo 9.6 — Teste em produção

Acesse o domínio e faça um teste completo do fluxo principal.

✅ Etapa 9 concluída. Sistema em produção.

---

## 📊 RESUMO VISUAL

ETAPA 0 → PREPARAÇÃO (pasta + credenciais)
ETAPA 1 → DEEPSEEK (01-PROMPT-DEEPSEEK) → BRIEFING-DEEPSEEK.md
ETAPA 2 → CLAUDE PROJECTS (02-ARQUITETO-SENIOR) → ESPECIFICACAO-REFORMULADA.md
ETAPA 3 → CLAUDE PROJECTS (03-PROMPT-CLAUDE-IA) → Pasta do projeto
ETAPA 4 → CLAUDE CODE (construção fase por fase)
ETAPA 5 → CLAUDE CODE (04-VALIDACAO-FUNCIONAL)
ETAPA 6 → CLAUDE CODE (05-VISTORIA-*)
ETAPA 7 → CLAUDE CODE (06-PROMPT-SEGURANCA)
ETAPA 8 → CLAUDE CODE (07-AUDITORIA-GERAL-FINAL)
ETAPA 9 → DEPLOY (Cloudflare + VPS + n8n + DNS)

---

## ⏱️ TEMPO ESTIMADO POR ETAPA

| Etapa | Tempo | Onde |
|---|---|---|
| 0. Preparação | 10 min | Fora da live |
| 1. DeepSeek | 10 min | Live |
| 2. Arquiteto | 10 min | Live |
| 3. Workspace | 10 min | Live |
| 4. Construção | 25 min+ | Live |
| 5. Validação | 8 min | Live |
| 6. Vistoria | 10 min | Live |
| 7. Segurança | 8 min | Live |
| 8. Veredito | 4 min | Live |
| 9. Deploy | 10 min | Opcional |
| TOTAL | ~105 min | |

---

## 💡 DICAS PARA A LIVE

1. Teste o fluxo inteiro 2–3 vezes antes de ir ao vivo.
2. Escolha um projeto pequeno para construir ao vivo (ex: lista de tarefas multi-tenant).
3. Tenha trechos pré-gravados das partes arriscadas (deploy, n8n).
4. Use /clear entre fases no Claude Code para economizar tokens.
5. Mostre os relatórios salvos em work-log/ — impressiona o público.
6. Salve prints dos momentos-chave para usar como fallback.
7. Deixe o chat aberto para perguntas durante a live.

---

## 📦 O QUE VOCÊ RECEBE NO FINAL

- ✅ 10 arquivos de prompt em .md
- ✅ O 00-CONTEXTO-INFRAESTRUTURA.md preenchido
- ✅ Este passo a passo completo
- ✅ O projeto-exemplo construído ao vivo
- ✅ Acesso ao repositório GitHub com tudo versionado

---

## 🔄 CHECKLIST DE VERIFICAÇÃO

Antes de considerar o projeto pronto, confirme:

- [ ] Briefing gerado pelo DeepSeek (BRIEFING-DEEPSEEK.md)
- [ ] Especificação reformulada (ESPECIFICACAO-REFORMULADA.md)
- [ ] Workspace do Claude Code criado (CLAUDE.md + pastas)
- [ ] Sistema construído por fases
- [ ] Validação funcional concluída (todos ✅)
- [ ] Vistoria arquitetural concluída (sem 🔴 crítico)
- [ ] Auditoria de segurança concluída (sem 🔴 crítico)
- [ ] Veredito final: nota A ou B
- [ ] Deploy realizado
- [ ] Teste em produção funcionando
- [ ] Tudo commitado no GitHub

---

**FIM DO DOCUMENTO**

Se tiver dúvidas, volte ao arquivo de prompt correspondente ou pergunte no chat da live.
