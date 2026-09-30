# QUAL LLM USAR PARA CADA FUNÇÃO — GUIA DE BOLSO

Regra geral: **modelo grátis ou barato onde errar não custa nada (rascunho,
triagem, classificação de texto curto); modelo forte onde a saída vira decisão,
código ou dinheiro.** E nunca troque modelo e prompt na mesma rodada: isole a
variável, senão você não sabe o que corrigiu o problema.

═══════════════════════════════════════════
1. NO FLUXO DA LIVE (do prompt ao deploy)
═══════════════════════════════════════════

| Função                                   | Modelo                          | Por quê                                              | Custo     |
|------------------------------------------|---------------------------------|------------------------------------------------------|-----------|
| Ideação e briefing (Etapa 1)             | DeepSeek (chat.deepseek.com)    | Barato, bom em perguntar; o erro aqui custa nada     | ~grátis   |
| Spec sem lacunas (Etapa 2)               | Claude Opus, no Claude Projects | Checklist longo, precisa de raciocínio e memória     | plano     |
| Workspace do Claude Code (Etapa 3)       | Claude Opus, no Claude Projects | Gera 12 arquivos coerentes entre si                  | plano     |
| Construção fase a fase (Etapa 4)         | Claude Code com Opus 5.5        | Código de verdade; use `/model` pra confirmar        | plano     |
| Tarefa repetitiva no código (renomear, gerar 20 testes iguais) | Claude Code com Sonnet | Mais rápido e mais barato, mesma qualidade nisso | plano |
| Validação, vistoria, segurança (5 a 8)   | Claude Code com Opus 5.5        | Auditoria exige achar o que não está óbvio           | plano     |

═══════════════════════════════════════════
2. NO SISTEMA QUE VOCÊ CONSTRUIU (produção)
═══════════════════════════════════════════

| Função no sistema                                  | Modelo                                         | Por quê                                                                 | Custo real                |
|----------------------------------------------------|------------------------------------------------|-------------------------------------------------------------------------|---------------------------|
| Checagem de saúde (processo no ar, API respondendo, RLS ligado, taxa de erro) | **Nenhum LLM.** Script com curl, pm2, SQL | Regra fixa não precisa de modelo; roda a cada minuto de graça | R$ 0 |
| Triagem de um evento anômalo (resumir em 2 frases o que aconteceu) | Modelo grátis via OpenRouter (`:free`, ex. Nemotron) | Texto curto, sem decisão; se errar, o chefe corrige | R$ 0 |
| Decisão de severidade + relatório de incidente (o "agente chefe") | Claude Sonnet, JSON estrito | Precisa citar monitor, erro literal e ação; é o que o humano vai copiar no Claude Code | centavos por evento |
| Agente de vendas no WhatsApp numa plataforma (GPTMaker e similares) | Modelo pequeno (2 créditos, ex. GPT 5.4 Mini) **+ regras no servidor** | Modelo grande custa 5 a 7x por mensagem; o pequeno funciona se portões, frases prontas e memória ficarem no servidor | 2 créditos/msg |
| Leitura de nota fiscal, cupom ou print, com confirmação do usuário | Claude Sonnet (visão) | Precisa ler número e valor certo; confirmação do usuário cobre o resto | ~R$ 0,03 por imagem |
| Resumo semanal automático por WhatsApp                | Claude Sonnet                                  | Texto curto sobre dados que já vieram do banco                          | centavos por envio        |
| Assistente conversacional com regras de negócio (agendamento, atendimento) | Claude Sonnet ou Opus via n8n | Segue regra longa e chama ferramenta com confiança | centavos por conversa |

═══════════════════════════════════════════
3. O QUE APRENDEMOS TESTANDO (vale mais que a tabela)
═══════════════════════════════════════════

- **Modelo pequeno segue a frase, não a intenção.** Com 2 créditos, "gostou do
  carro?" vira pergunta repetida e "a equipe entra em contato" sai sem acionar
  nada. Solução não é prompt maior: é portão no servidor (o webhook recusa sem
  dado), frase pronta devolvida pela ferramenta, memória por conversa fora do
  modelo e um vigia que confere se a promessa virou ação.
- **Janela de contexto é limite real.** Plano básico de plataforma de chatbot
  mostra só as últimas 20 mensagens ao modelo; cada foto conta como uma. Ou
  paga o dobro, ou guarda o estado no servidor.
- **Haiku e modelos "mini" falharam em tool calling com muitas regras**; um
  modelo pequeno ficou mudo numa plataforma por incompatibilidade. Teste 1
  cenário fixo com cada modelo antes de escolher.
- **Grátis tem lugar**: triagem, rascunho, classificar texto. Não tem lugar
  onde a resposta vira decisão do dono, cobrança, ou ação em produção.
- **Sem chave em código, nunca.** Chave do OpenRouter, Anthropic e OpenAI vão
  em variável de ambiente ou `.env` fora do git. Chave vazada no GitHub já
  custou uma tarde de rotação.

═══════════════════════════════════════════
4. ONDE PEGAR
═══════════════════════════════════════════

- OpenRouter (modelos grátis): openrouter.ai → chave → filtre modelos com `:free`.
  Limite de uso por dia; serve pra triagem e rascunho.
- Claude API: console.anthropic.com → chave; use Sonnet pro chefe, Opus só se
  o raciocínio pesar.
- DeepSeek: chat.deepseek.com (chat) ou platform.deepseek.com (API).

═══════════════════════════════════════════
5. ROTEADOR DE LLM (opcional, pra quem quer baratear o Claude Code)
═══════════════════════════════════════════

Existe um jeito de o Claude Code usar modelos diferentes por tipo de tarefa
sem você trocar nada na mão: um **roteador** self-hosted, compatível com a API
da Anthropic, que fica entre o Claude Code e os modelos. Ele detecta a fase do
pedido (planejar, executar, revisar, utilidade) e manda cada uma pro modelo
que você configurou, inclusive modelos grátis ou mais baratos.

Repositório público (feito por um amigo da Automind):
https://github.com/lSaGaT/router-llm  (Next.js/Bun, tem Dockerfile e docker-compose)

Como usamos:
1. Clonar o repo e subir o servidor (`bun run dev` local, ou Docker na VPS).
   Ele escuta numa porta (ex.: 3003) e tem uma UI pra cadastrar chaves e rotas.
2. No `~/.claude/settings.json` apontar o Claude Code pro roteador:
   `ANTHROPIC_BASE_URL` = `http://127.0.0.1:3003/api` e `ANTHROPIC_AUTH_TOKEN`
   com o token do roteador. Pronto: rode `claude` normalmente, o roteamento é
   transparente.
3. Configurar por fase: modelo forte pra planejar e revisar, modelo barato pra
   executar tarefa mecânica, modelo grátis pra utilidades.

O que aprendemos usando: o Claude do roteador executa bem código de produto
(rotas, modelos, regra de negócio), mas em 3 tarefas diferentes **pulou ou
deixou pela metade arquivo de teste sem avisar**, e o relatório dizia
"criado". Regra: depois de qualquer tarefa dele, confira os arquivos no disco
antes de aceitar. Vale pra qualquer modelo mais barato: economiza dinheiro,
não economiza conferência.
