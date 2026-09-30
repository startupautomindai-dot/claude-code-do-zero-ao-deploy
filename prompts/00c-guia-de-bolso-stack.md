# GUIA DE BOLSO — QUE FERRAMENTA E QUE LINGUAGEM USAR EM CADA PROJETO

Leia antes da Etapa 1. É com este guia que você e a IA decidem a stack do
projeto no briefing (o prompt 01 já usa estes critérios). Quem está começando
não precisa decorar: precisa entender para que serve cada coisa e conseguir
conferir se a escolha da IA faz sentido.

═══════════════════════════════════════════
1. FRONTEND — O QUE O NAVEGADOR ENTENDE (A BASE)
═══════════════════════════════════════════

| Linguagem  | Serve para                                                        | Analogia                       |
|------------|-------------------------------------------------------------------|--------------------------------|
| HTML       | Estrutura: títulos, botões, tabelas, formulários                   | A planta da casa               |
| CSS        | Aparência: cores, espaçamento, tamanho, layout, animação           | A pintura e a decoração        |
| JavaScript | Comportamento: o que acontece quando o usuário clica, digita, rola | A eletricidade e o encanamento |

Regra de ouro: tudo o mais no frontend é jeito de escrever essas três.

═══════════════════════════════════════════
2. FRONTEND — AS FERRAMENTAS (NÃO SÃO LINGUAGENS)
═══════════════════════════════════════════

| Ferramenta  | Para que serve                                                     | Por que existe                              |
|-------------|--------------------------------------------------------------------|---------------------------------------------|
| TypeScript  | JavaScript com tipos; avisa o erro antes de rodar                  | Evita bug bobo em projeto grande            |
| React       | Divide a tela em componentes reutilizáveis                         | Não repetir código: botão, card, modal      |
| Vite        | Build: junta e comprime tudo num pacote                            | Site rápido no navegador                    |
| Tailwind    | CSS por classes prontas direto no HTML                             | Escrever menos CSS, padronizar o visual     |
| Next.js     | React com servidor embutido; monta parte da página no servidor     | SEO melhor, carregamento mais rápido        |
| PWA         | Site instalável como app, funciona offline                         | Usuário não precisa baixar na loja          |

═══════════════════════════════════════════
3. FRONTEND — QUAL ABORDAGEM ESCOLHER
═══════════════════════════════════════════

| Situação                                   | Escolha                     | Motivo                          |
|--------------------------------------------|-----------------------------|---------------------------------|
| Painel pequeno, site institucional, landing| HTML + CSS + JS puro        | Simples, rápido, sem build      |
| App que vai crescer, várias telas          | React + TypeScript + Vite   | Componentes, tipagem, escala    |
| Site que precisa de SEO forte              | Next.js                     | Renderiza no servidor           |
| App que precisa funcionar offline / campo  | PWA (em cima de qualquer um)| Instalável, cache local         |

═══════════════════════════════════════════
4. BACKEND — PARA QUE SERVE CADA OPÇÃO
═══════════════════════════════════════════

| Tecnologia        | Para que serve                                                          | Quando usar                                   |
|-------------------|-------------------------------------------------------------------------|-----------------------------------------------|
| Node.js           | Rodar JavaScript no servidor: receber pedidos, aplicar regras, falar com o banco | APIs tradicionais, gateways, integrações rápidas |
| Python + FastAPI  | A mesma coisa em Python; forte em dados, IA e automação                 | Agentes, processamento pesado, scraping, polling |
| n8n               | Orquestração visual: fluxos em blocos, sem escrever código              | Integrar vários sistemas, automações, webhooks |
| Supabase direto   | O frontend fala direto com o banco via PostgREST, com RLS               | App simples, sem backend próprio               |

═══════════════════════════════════════════
5. BACKEND — COMO ESCOLHER
═══════════════════════════════════════════

| Se o problema é…                                   | Escolha…          | Porque…                                        |
|----------------------------------------------------|-------------------|------------------------------------------------|
| API padrão, CRUD, gateway                          | Node.js           | Rápido, mesma linguagem do front               |
| IA, agentes, processamento, scraping               | Python + FastAPI  | Ecossistema forte de dados e IA                |
| Integrar 5 sistemas sem escrever código            | n8n               | Visual, rápido de montar, fácil de manter      |
| App pequeno, sem backend próprio                   | Supabase direto   | PostgREST já dá a API pronta                   |

Pode misturar: o mais comum nos projetos da Automind é frontend + Supabase
direto para o CRUD, e n8n para automações e integrações (WhatsApp, e-mail,
agendamento). Backend próprio (Node ou Python) só quando há regra de negócio
pesada ou IA.

═══════════════════════════════════════════
6. COMO TUDO SE CONECTA (VISÃO DE CIMA)
═══════════════════════════════════════════

    [ NAVEGADOR ]                     [ SERVIDOR ]                    [ BANCO ]
    HTML + CSS + JS      ──HTTP/JSON──►  Node.js / Python    ──SQL──►   PostgreSQL
    React / Next / PWA   ◄────JSON────   n8n / Supabase                 + RLS
           │
           └──── fetch (API REST) ────►  Backend  ────►  Responde JSON

    Sistema externo (WhatsApp, iFood, gateway de pagamento)
           │
           └──── webhook ────►  Meu backend / n8n

- API REST = o front pergunta, o back responde (HTTP/JSON).
- Webhook = um sistema externo avisa o meu backend.

═══════════════════════════════════════════
7. PARA FIXAR
═══════════════════════════════════════════

Frontend: HTML = estrutura · CSS = aparência · JS = comportamento.
React, Vite, Tailwind e Next são ferramentas, não linguagens. PWA = site que vira app.

Backend: Node = JavaScript no servidor (APIs, gateways) · Python/FastAPI = IA, agentes,
dados · n8n = orquestração visual, sem código · Supabase direto = frontend falando com o banco.

Frase final: "HTML estrutura, CSS veste, JavaScript dá vida. React organiza, TypeScript
protege, Vite empacota, Next renderiza no servidor. No backend, Node para API, Python para
IA, n8n para orquestrar. E tudo se fala por HTTP/JSON; webhook é quando o mundo externo avisa."

═══════════════════════════════════════════
COMO USAR NA ETAPA 1
═══════════════════════════════════════════

Anexe este arquivo junto com o 00-contexto-infraestrutura.md no chat da Etapa 1.
O prompt 01 manda a IA escolher a stack por estes critérios, dizer o porquê de
cada escolha e, se duas opções empatarem, perguntar a você antes de fechar o
briefing. Na Etapa 2 o Arquiteto confere a escolha e só troca com justificativa.
