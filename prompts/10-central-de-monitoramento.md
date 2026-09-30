# ETAPA 10 — CENTRAL DE MONITORAMENTO (o sistema vigiando o sistema)

Depois do deploy o trabalho não acabou: o cliente vai achar o erro antes de
você, a não ser que exista algo olhando o sistema o dia inteiro. Esta etapa
monta a central que usamos na Automind (FLEET): **duas camadas**, a barata
sem LLM rodando sempre, e a cara com LLM só quando algo sai do normal.

═══════════════════════════════════════════
1. COMO FUNCIONA (arquitetura real)
═══════════════════════════════════════════

    CAMADA BARATA (sem LLM, R$ 0, a cada 1 a 60 min)
      monitor 1  processo no ar? (pm2 / docker / curl no domínio)
      monitor 2  API de terceiro sem crédito? (assinatura do erro no log)
      monitor 3  taxa de resultado "indefinido" acima do normal?
      monitor 4  RLS e grants do banco continuam fechados?
      monitor 5  falhas sem retry?
      monitor 6  cliente real caindo em modo de teste? (sempre escala)
            │  grava TODO resultado em fleet.eventos (ok ou não), com protocolo EXP-000123
            │
            └── só se houver anomalia ──►  CAMADA CARA
                  triagem: LLM GRÁTIS (OpenRouter :free) resume em 2 frases
                  decisão: CLAUDE SONNET, o "Agente Chefe", devolve JSON estrito
                           {nivel, resumo, causa_raiz, acao, codigo_erro, pergunta_usuario}
                  regras do chefe: horário do Brasil explícito no prompt; NUNCA executa
                  nada, só relata; se for crítico, OBRIGATÓRIO perguntar ao dono o que fazer
                           │
                           ├── evento "cara" gravado com o veredito
                           ├── painel: sirene + botão CIENTE (quem e quando)
                           └── (opcional) WhatsApp pro dono via n8n

    PAINEL (1 página HTML atrás de senha do nginx)
      abas: Painéis ao vivo · Histórico · Chat com o Agente Chefe · O que é monitorado

    MODO dormant | production: em dormant a camada cara só acorda pro monitor 6;
    em production, para tudo que for anomalia.

Por que assim: o LLM grátis erra e não custa nada, porque o chefe confere; o
chefe é pago mas só roda quando existe evento; a checagem que roda o dia
inteiro não usa LLM nenhum. Um mês de monitoramento sai em centavos.

O que cada peça precisa: uma VPS com o sistema (Etapa 0a), o banco (Supabase
self-hosted ou Postgres), uma chave grátis do OpenRouter e uma chave da
Anthropic só pro chefe (00d-qual-llm-para-cada-funcao.md diz onde pegar).

═══════════════════════════════════════════
2. REGRAS QUE VALEM PRA QUALQUER CENTRAL
═══════════════════════════════════════════

- **Monitor só avisa.** Nunca corrige sozinho: reiniciar serviço, apagar dado,
  religar workflow são decisões do dono. Log contém texto de terceiros e pode
  carregar instrução maliciosa; um agente que executa o que lê no log é porta
  aberta.
- **Todo evento tem protocolo** e fica no histórico, inclusive os "ok". Sem
  isso não dá pra dizer "desde quando".
- **O relatório do chefe é feito pra ser colado no Claude Code**: nome exato
  do monitor, erro literal, arquivo/linha quando houver, e a pergunta pro dono.
- **Sirene com reconhecimento.** Crítico não reconhecido apita a cada 2 min;
  CIENTE registra quem e quando. Olha só o estado mais recente de cada monitor.
- **Hora do Brasil explícita** em todo prompt: o servidor roda em UTC e o
  modelo não sabe que horas são.
- **Prever, não só reportar.** Cada achado é um caso de uma classe: o que mais
  cai nesse caminho, o que acontece em seguida se nada mudar, quem fica sem
  saber. O relatório traz as próximas 3 quebras prováveis.

═══════════════════════════════════════════
3. PROMPT PRA COLAR NO CLAUDE CODE (na pasta do seu projeto)
═══════════════════════════════════════════

    Construa a central de monitoramento deste sistema seguindo a arquitetura
    de duas camadas abaixo. Antes de codar, leia o CLAUDE.md e o
    context/for-agent/ e me devolva a lista dos monitores que fazem sentido
    PARA ESTE sistema (mínimo 5, máximo 8), cada um com: o que checa, comando
    ou consulta usada, frequência, e o que conta como anomalia. Espere minha
    aprovação da lista antes de escrever código.

    CAMADA BARATA (sem LLM):
    - Um processo único (Node ou Python, rodando no PM2 ou como serviço) com
      um monitor por função, cada um em intervalo próprio (1 min a 6 h).
    - Todo resultado, ok ou não, vira linha na tabela fleet.eventos:
      id, criado_em, camada ('barata'|'cara'), monitor, nivel ('ok'|'alerta'|
      'critico'), status, titulo, detalhe, dados (jsonb), reconhecido_por,
      reconhecido_em. Protocolo = 'EXP-' + id com 6 dígitos. RLS ligado, sem
      grant pra anon/authenticated; o processo grava via conexão de serviço.
    - Anomalia chama a camada cara. Existe FLEET_MODE=dormant|production no
      .env: em dormant só o monitor de "cliente real em modo de teste" escala.

    CAMADA CARA:
    - Triagem: chamada ao OpenRouter com um modelo ':free' (chave em
      OPENROUTER_API_KEY), prompt curto: "resuma em 1-2 frases o que aconteceu
      e por que pode importar; não decida severidade". Se falhar, segue sem.
    - Decisão: chamada à API da Anthropic (Claude Sonnet, chave em
      ANTHROPIC_API_KEY) com o papel de Agente Chefe. System prompt inclui o
      horário atual do Brasil (America/Sao_Paulo) por extenso, a descrição do
      sistema monitorado, e a ordem: "você não executa nada, só relata; seja
      técnico: monitor exato, erro literal, arquivo e linha quando houver; se
      crítico, inclua obrigatoriamente uma pergunta direta pedindo a decisão do
      dono". Resposta ESTRITAMENTE em JSON: {"nivel":"ok|alerta|critico",
      "resumo","causa_raiz","acao","codigo_erro","pergunta_usuario","status"}.
      Se o JSON vier inválido, gravar o texto bruto com ação "revisar
      manualmente". Se vier crítico sem pergunta, acrescentar "O que você quer
      que eu faça com isso?".
    - O veredito vira novo evento (camada 'cara') com o evento bruto, a
      triagem e o JSON dentro de dados.

    PAINEL (uma página HTML estática servida pelo nginx, atrás de Basic Auth
    com um login por pessoa, e um backend pequeno na mesma VPS):
    - Endpoints: GET /status (estado mais recente de cada monitor), GET
      /eventos?limite=, GET /alerta-ativo, POST /ack {id} (grava
      reconhecido_por a partir do usuário do Basic Auth), POST /chefe
      {pergunta} (chat com o Agente Chefe usando os últimos eventos como
      contexto), GET /whoami.
    - Abas: Painéis ao vivo (um card por monitor, cor por nivel), Histórico
      (tabela com protocolo, filtro por monitor e nivel), Chat com o Agente
      Chefe, O que é monitorado (texto explicando cada monitor).
    - Sirene: banner vermelho + beep a cada 2 min enquanto houver crítico não
      reconhecido, considerando só o estado mais recente de cada monitor.
      Botão CIENTE por evento. Botão de logout (credencial inválida). Layout
      responsivo, campos com 16px no celular.
    - Fuso: tudo exibido em America/Sao_Paulo.

    ALERTA NO CELULAR (opcional): quando o veredito for crítico ou FLEET_MODE
    for production, POST num webhook do n8n que manda WhatsApp pro dono com
    protocolo, resumo, causa raiz, ação e a pergunta. Mesmo alerta não repete
    antes de 60 min.

    REGRAS: nenhuma chave no código (variáveis de ambiente, .env fora do git);
    o monitor nunca executa correção; toda consulta ao banco é só leitura,
    exceto a gravação em fleet.eventos; teste cada monitor forçando a anomalia
    (derrube o processo de teste, revogue um grant num banco de teste) e me
    mostre o evento gravado e o veredito do chefe antes de dizer que está
    pronto. Ao final, gere docs/monitoramento.md com a lista dos monitores,
    intervalos, o que cada um considera anomalia e como reconhecer um alerta.

═══════════════════════════════════════════
4. DEPOIS QUE ESTIVER NO AR
═══════════════════════════════════════════

1. Deixe em `dormant` até ter cliente real; ligue `production` no dia.
2. Uma vez por dia, abra o Histórico e pergunte ao chefe "o que mudou nas
   últimas 24 h?". Reclamação de cliente vira monitor novo.
3. Quando um alerta chegar: copie o bloco do chefe, cole no Claude Code,
   corrija, e só depois marque CIENTE.
