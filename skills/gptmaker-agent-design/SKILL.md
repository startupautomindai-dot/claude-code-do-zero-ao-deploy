---
name: gptmaker-agent-design
description: Use ao criar, configurar, depurar, auditar ou melhorar QUALQUER agente na plataforma GPTMaker — behavior, settings, treinamentos, intentions/webhooks, servidores MCP, regras de transferência, ações de inatividade, canais (WhatsApp/Z-API/Cloud API/Instagram/Widget…), chats/atendimentos, escolha de modelo LLM e custo em créditos. Mapa completo da doc oficial (developer.gptmaker.ai, lida integralmente em 29/09/2026) + histórico real de +25 bugs encontrados e corrigidos na agente-piloto (concessionária-piloto). Gatilho: "GPTMaker", "GPT Maker", "agente de IA" numa plataforma de chatbot (não n8n+Claude direto), "intention"/"intenção", "MCP no agente", "behavior do agente", "treinamento do bot", "créditos do agente", nome de qualquer agente GPTMaker (agente-piloto, agente-clone, agentes de concessionária).
---

# GPTMaker — como o sistema funciona e como configurar agentes sem reintroduzir bugs já resolvidos

Duas fontes, sempre separadas neste documento:

- **[DOC]** = está na documentação oficial (`developer.gptmaker.ai`). Confiável quanto a *o que existe*, rasa quanto a *como se comporta*.
- **[REAL]** = achado testando em produção (agente-piloto, 30/08 → 12/09/2026). Muitas vezes contradiz ou completa a doc. Quando os dois divergirem, o [REAL] vence.

## 0. Como reler a doc oficial (sem sofrer com o site em JS)

- O site é Mintlify. Toda página tem versão Markdown crua: acrescente `.md` à URL (`https://developer.gptmaker.ai/agents/agent-intentions.md`).
- Índice completo de páginas: `https://developer.gptmaker.ai/llms.txt`.
- Spec OpenAPI inteira (55 endpoints, todos os enums, schemas `Assistant`/`NewAssistant`/`Intention`/…): `https://developer.gptmaker.ai/api-reference/openapi.json`. É a fonte mais confiável pra nome exato de campo e valor de enum.
- Comunidade/suporte: WhatsApp de suporte com bot "Makerzinho" (+55 44 99838-0596), Discord, YouTube `@GPTMaker`. [REAL] Suporte humano demora; o bot responde rápido mas só confirma o que a doc já diz. Escale por escrito com evidência (IDs, timestamps, mensagens de erro).

## 1. Mapa do sistema [DOC]

Hierarquia: **Conta → Workspace(s) → Agentes + Canais + Contatos + Campos customizados**. Créditos e plano são por workspace.

| Peça | O que é | Endpoint principal (`https://api.gptmaker.ai`, Bearer token de `app.gptmaker.ai/browse/developers`) |
|---|---|---|
| Agente (`Assistant`) | Identidade + `behavior` | `GET/PUT/DELETE /v2/agent/{id}`, `PUT /active`, `PUT /inactive`, `POST /v2/workspace/{ws}/agents` |
| Settings | Modelo, flags de comportamento | `GET/PUT /v2/agent/{id}/settings` |
| Webhooks de evento | Notificações do ciclo do atendimento | `GET/PUT /v2/agent/{id}/webhooks` |
| Treinamentos | Base de conhecimento estática | `GET/POST /v2/agent/{id}/trainings`, `PUT/DELETE /v2/training/{id}` |
| Intenções | Function-calling pra API externa | `GET/POST /v2/agent/{id}/intentions`, `PUT/DELETE /v2/intention/{id}` |
| MCP | Servidor de tools externo | `POST /v2/agent/{id}/mcp/add`, `GET /v2/mcp/{id}/tools`, `…/tool/{t}/active|inactive`, `…/sync-tools`, `DELETE /v2/mcp/{id}` |
| Regras de transferência | Handoff pra humano ou pra OUTRO agente | `/v2/agent/{id}/transfer-rules` |
| Ações de inatividade | Follow-up automático por tempo parado | `/v2/agent/{id}/idle-actions` |
| Campos customizados | Campos extras no contato/negócio (CRM) | `/v2/custom-field/workspace/{ws}` |
| Canais | WhatsApp, Instagram etc. — desde a reestruturação são do WORKSPACE, não do agente | `GET /v2/workspace/{ws}/channels`, `POST /v2/workspace/{ws}/create-channel`, `PUT /v2/channel/{id}` (vincula agente), `/config`, `/qr-code`, `/widget-settings`, `/start-conversation` |
| Chats | Conversa com um cliente | `GET /v2/workspace/{ws}/chats`, `/v2/chat/{id}/messages`, `send-message`, `start-human`, `stop-human` |
| Atendimentos (`Interaction`) | Um chat gera N atendimentos (`RUNNING`/`WAITING`/`RESOLVED`) | `GET /v2/workspace/{ws}/interactions`, `/v2/interaction/{id}/messages`, `POST /v2/workspace/{ws}/export` (CSV) |
| Conversa via API | Usar o motor do agente sem canal | `POST /v2/agent/{id}/conversation`, `POST /v2/agent/{id}/add-message` |
| Créditos | Saldo e consumo | `GET /v2/workspace/{ws}/credits`, `GET /v2/agent/{id}/credits-spent?year&month&day` |
| Histórico de behavior | Quem mudou o `behavior` e quando | `GET /v2/agent/{id}/list-behavior-history?page=0&pageSize=` |

**Ordem de precedência que a IA obedece na prática [REAL]**: settings de plataforma (`enabledEmoji`, `limitSubjects`…) > `jobSite` (navegação ao vivo) > treinamento estático > `behavior`. Ou seja, texto no `behavior` NÃO vence um flag ligado nem um `jobSite` preenchido. Sempre auditar os três antes de culpar o prompt.

## 2. Agente (`Assistant`) e `behavior`

**Objeto completo [DOC]**: `name, avatar, behavior, communicationType (FORMAL|NORMAL|RELAXED), type (SUPPORT|SALE|PERSONAL), jobName, jobSite, jobDescription`.

- **CRÍTICO [REAL] — `PUT /v2/agent/{id}` é substituição TOTAL, não PATCH.** Campo omitido volta pra default/null. `type` nulo derrubou o agente inteiro (10/09): nem "Oi" respondia, erro `Assistant.getType() is null`. **Regra: `GET` fresco → montar os 8 campos → `PUT`.** Nunca um subconjunto, mesmo pra mudar 1 letra. Vale também pra `communicationType`, que voltou de `FORMAL` pra `NORMAL` sozinho por causa de PUT parcial.
- **Teto do `behavior`: ~3000 caracteres [REAL]** (não documentado; 2993 já dava erro). Trabalhe em 2500-2600 pra ter folga. Comprimir: headers curtos, fatorar frases repetidas, tirar "CRÍTICA"/"IMPORTANTE" redundantes. Nunca cortar regra de negócio pra caber — mova regra estável pra Treinamento TEXT ou pra Intention tipo `INSTRUCTIONS` (ver §5).
- **Estrutura recomendada [DOC]**: (1) regras de interação, (2) limites do que NUNCA discutir, (3) escalação (quando/como transferir). Tom NÃO vai no texto: existe `communicationType` pra isso (`FORMAL` = sempre formal; `NORMAL` = espelha o cliente; `RELAXED` = sempre informal).
- **`jobSite` é RAG ao vivo no site, invisível em `/trainings` [REAL, grave]**: com URL preenchida, a IA responde do conteúdo raspado da página (catálogo, preço) sem acionar nenhuma Intention/MCP, sem erro, sem pista. Pior (10/09): **esvaziar o campo NÃO limpa o índice já feito** — voltou a vazar com `jobSite: ""`. Reportado ao suporte, sem solução. **29/09: apareceu preenchido pela 3ª vez, nos dois agentes** — auditar `jobSite` no início de TODA sessão. Diagnóstico: IA cita produto específico sem execução nova no n8n → suspeitar do `jobSite` antes do texto. Se puder, nunca preencher `jobSite` num agente que dependa de dado vivo via webhook; reforce nos treinamentos que o site NÃO é fonte de estoque.
- **`behavior` já reverteu sozinho pra versão antiga [REAL]** (bug de persistência deles). Use `GET /list-behavior-history` pra ver quem/quando (campo `userLogin`, `createdAt` em ms, `behaviorText`) e sempre `GET` de conferência antes de assumir que uma edição "pegou", mesmo dias depois.
- **Após `PUT` do agente o status pode ficar `TRAINING` por minutos [REAL]** — nesse estado nenhuma Intention dispara (responde de memória). Conferir `status: ACTIVE` no `GET` antes de testar.
- `PUT /active` e `/inactive` existem [DOC] pra ligar/desligar. [REAL] Durante instabilidade da plataforma os dois devolvem 500 genérico — é infra deles, não seu payload.
- **Padrão de instrução que funciona [REAL]**: regra de ação em frase imperativa isolada ("NA MESMA RESPOSTA, ACIONE `alertar_donos`. Nunca só diga que vai acionar."). Cláusula no meio de frase longa foi ignorada 2x (a IA falava a frase certa e não acionava nada). "NUNCA X" explícito por regra funciona melhor que explicação genérica.
- **Palavras vagas não são dado [REAL]**: "barato/de entrada/econômico" não é preço; a IA acionou a busca sem filtro mesmo com regra. Prefira resolver no servidor (rede de segurança no webhook) a depender da IA perguntar certo.
- **Lógica de horário/data fica no servidor [REAL]**: não confie no modelo pra saber a hora real. Calcule `dentroHorario` no n8n (`America/Sao_Paulo`) e devolva no JSON; o `behavior` só escolhe a frase. Saudação por horário ("bom dia") errava com frequência → "Olá" fixo.
- **Cidades/distâncias**: a IA chutou "pertinho, 30-40 min" pra cliente a 230 km. Liste explicitamente as cidades atendidas e proíba estimativa de distância.

## 3. Settings (`PUT /v2/agent/{id}/settings`) [DOC + REAL]

| Campo | Valores | Notas |
|---|---|---|
| `prefferModel` | 33 enums (ver §9) | grafia com dois "f" mesmo |
| `timezone` | string | ex. `America/Sao_Paulo` |
| `enabledHumanTransfer` | bool | permite a IA transferir pra humano (aba "Em espera") |
| `enabledReminder` | bool | follow-up automático; [REAL] quando a IA trava, é isso que manda a mensagem genérica de "lembrete" |
| `splitMessages` | bool | quebra resposta longa em várias |
| `enabledEmoji` | bool | **[REAL] `true` gera emoji MESMO com "sem emoji" no `behavior`** — desligue aqui |
| `limitSubjects` | bool | só fala do negócio |
| `messageGroupingTime` | `NO_GROUP, FIVE_SEC, TEN_SEC, THIRD_SEC, ONE_MINUTE` | agrupa mensagens picadas do cliente antes de responder (a doc descreve errado como "modelo preferido") |
| `signMessages` | bool | assina a mensagem com o nome do agente |
| `maxDailyMessages` | `null, 20, 50, 100, 200, 500, 1000` | limite de interações por atendimento; outro valor é rejeitado |
| `maxDailyMessagesLimitAction` | `TEMP_BLOCK_30S/5M/10M/30M/1H, BLOCK, TRANSFER` | só vale com `maxDailyMessages` ≠ null |
| `knowledgeByFunction` | bool | "busca inteligente" do treinamento = RAG semântico sob demanda; [REAL] suporte confirmou que NÃO existe busca determinística nativa |
| `onLackKnowLedge` | URL | webhook quando o agente não sabe responder (duplicado em `/webhooks`) |

- **[REAL 29/09] Campos de settings não documentados que aparecem no `GET`: `enabledContactFields`, `resumeTransferHumanAI`.** `resumeTransferHumanAI: true` + dono respondendo pelo celular gera o padrão `START_INTERACTION_HUMAN` → `TRANSFER_AGENT` em segundos e a IA responde por cima do humano. Testar `false` se os donos atendem pelo celular e não pelo painel.
- **[REAL 29/09] Enum de modelo fora da doc**: `prefferModel` devolveu `GPT_6_LUNA` (doc só lista `GPT_5_6_LUNA`). A lista pública atrasa em relação ao painel; confie no `GET /settings`.
- **[REAL 29/09] `enabledReminder: true` = "Olá, você está aí? Vamos continuar?" 10 min após TODA mensagem**, inclusive depois de despedida e de madrugada, 4x na mesma conversa. Texto no behavior não desliga. Desligar e usar idle-actions com `workingHours`.
- [REAL] Depois de `PUT /settings` (principalmente troca de modelo) espere alguns segundos antes de testar; instabilidade transitória igual à edição de `behavior`.
- Ao clonar um agente, **settings NÃO vão junto**: `communicationType`, `enabledEmoji`, `prefferModel` precisam ser sincronizados à mão (esquecido uma vez no clone agente-clone, só pegou porque conferi de verdade).

## 4. Treinamentos [DOC + REAL]

- Tipos: `TEXT` (texto + `image` opcional), `WEBSITE` (`trainingSubPages DISABLED|ACTIVE`, `trainingInterval NEVER|THIRTY_SECONDS|ONE_HOUR|FOUR_HOUR|EIGHT_HOUR|TWELVE_HOUR|ONE_DAY|ONE_WEEK|ONE_MONTH`), `VIDEO` (YouTube ≤ 60 s), `DOCUMENT` (`documentUrl/Name/Mimetype`, PDF). `callbackUrl` opcional avisa quando o processamento termina. **Só `TEXT` é atualizável (`PUT /training/{id}`)**; os outros é apagar e recriar.
- **Escreva afirmação direta [DOC]**: "O produto custa X" ✅, "Quando perguntarem o preço diga X" ❌.
- **NUNCA dado que muda (estoque, preço, disponibilidade) em treinamento [REAL]** — mesmo com `behavior` mandando usar a Intention, a IA às vezes responde do texto estático (carro vendido, preço velho) sem aviso. A própria doc concorda: conteúdo dinâmico → Intention. Dado vivo = webhook/MCP, sempre.
- **[REAL 29/09] `POST /trainings` tipo TEXT recusa texto acima de 1.028 caracteres** (`"The description cannot exceed 1028 characters"`). Regra longa vira 2-3 treinamentos curtos. Com `knowledgeByFunction:false` TODOS os treinamentos entram em toda resposta, então treinamento curto funciona como extensão do `behavior` (que trava em 3.000).
- **[REAL 29/09] Comparativo isolado de modelo (mesmo behavior, mesmo cenário de 5 passos)**: `GPT_6_LUNA` (1 cr) repete pergunta já respondida e pula passo; `GPT_5_4_MINI` (2 cr) seguiu o fluxo inteiro; `CLAUDE_4_5_HAIKU` (3 cr) travou repetindo "qual faixa de preço" e nunca chamou a tool. Escolha atual da agente-piloto: `GPT_5_4_MINI`.
- **[REAL 29/09] `communicationType` derivou sozinho de FORMAL para NORMAL** entre 14h30 e 15h39 sem PUT nenhum (provável efeito de abrir/salvar no painel). Script de publicação sempre força o valor esperado em vez de assumir.
- **Treinamento também precisa de manutenção [REAL]**: ao desativar/renomear uma Intention ou tool, grep em TODOS os treinamentos pelo nome antigo; um treinamento dizendo "cor não é filtrável" ou "preço só se perguntado" contradizia o código real e confundia o modelo.

## 5. Intenções (Intentions) — function-calling pra webhook [DOC + REAL]

**Schema [DOC]**: `description` (REQ, o "nome" que a IA vê), `details`/`instructions` (quando usar / instruções — a spec troca a semântica dos dois entre create e update; na prática preencha os dois com o mesmo sentido e confira no painel), `fields[]` (`name, jsonName, description, type STRING|URL|DATE_TIME|DATE|NUMBER|BOOLEAN, required`), `type WEBHOOK|INSTRUCTIONS`, `httpMethod GET|POST`, `url`, `headers[]`, `params[]`, `requestBody` (string JSON), `variables[]` (`valueExpression`, `defaultFieldKey` ∈ `chat_id, contact_name, contact_phone, contact_email, contact_gender, contact_birthday, contact_job_title, contact_org_name, contact_org_state, contact_org_city`, ou `customField{id…}`), `autoGenerateParams`, `autoGenerateBody`. Na URL/body use `@` pra variáveis do sistema e campos capturados.

- **`type: INSTRUCTIONS`** [DOC] = intenção sem webhook: quando a IA detecta a intenção, aplica o texto de `instructions`. É uma forma de tirar regra condicional do `behavior` (teto de 3000) sem gastar chamada HTTP. Não testado por nós ainda — validar antes de apostar.
- **Campos estruturados, nunca 1 campo de texto livre [REAL, maior ganho do projeto]**: N campos tipados com `description` orientando o valor eliminou a causa raiz de ~7 bugs (preço em formato variado, câmbio perdido, modelo confundido com veículo de troca). Não existe enum de verdade — STRING + instrução na `description`.
- **Limites não documentados [REAL, erro 500]**: `description` de campo ≤ **255** chars; `details` ≤ **512** chars.
- **Campo opcional com `""` derruba a chamada inteira [REAL]**: erro `"fields X,Y is required"` do lado do GPTMaker, antes do webhook (nenhuma execução no n8n). Correção validada: instruir na `description` a mandar `"-"` (STRING) ou `0` (NUMBER) em vez de "deixe vazio"; webhook trata `-`/`--`/"indiferente"/"tanto faz"/"qualquer"/"nenhum" como vazio.
- **Campo ambíguo → "NUNCA X" na `description` do próprio campo** (ex.: modelo desejado × veículo de troca). Explicar 1x no `details` não basta.
- **Variáveis injetadas chegam com o nome do `defaultFieldKey`, não do seu alias [REAL]**: configurar `valueExpression: "telefone"` não adianta — o body chega como `contact_phone`. Leia pelo nome padrão.
- **Máx. 1 chamada por mensagem do cliente**, reforçado no `behavior` [REAL] — senão a IA dispara 1 por item citado (duplica alerta, infla resultado).
- **Todo fix de "que dado a IA pode mandar" tem 2 metades [REAL]**: o código que usa o campo (n8n) E o campo cadastrado na Intention. Faltou o campo `cor` na Intention → "tem carro branco?" devolveu o estoque inteiro.
- **Resposta grande demais quebra a plataforma [REAL]**: 11 veículos num JSON → "Erro ao processar resposta do agente" na tela do cliente. Cape o retorno no servidor (ex.: sem nenhum critério → 4 mais baratos). Muitas fotos rápidas → vazamento de log interno (`Imagem: [url] OCR: null`) na resposta; limitar a 4 por chamada mitiga.
- **Fallback nunca derruba todos os filtros de uma vez**; relaxe 1 critério por vez em cascata, ordenado por proximidade do pedido. E **nunca sugira alternativa com foto sem perguntar** antes — decisão do cliente (10/09).
- **"Extremamente proibido dizer que não tem um item que existe" [REAL]**: match por campo curado (`base_model`) vence qualquer palavra extra; palavra extra só desambigua quando 2+ compartilham a base. Match por frase inteira como substring foi causa de bug 4x — sempre por palavra, com fallback de prefixo E de esqueleto de consoantes (`platinum`→`plt`), e aceitar siglas de 2 letras (`SV`, `CG`). Quando não achar, devolva `estoque_completo` pra IA conferir antes de negar.
- **n8n por trás do webhook — armadilhas já pagas**: nó não roda com 0 itens (use `fullResponse:true` + header `Content-Range`); `$json` já é o objeto (nunca `$json[0]`); expressão sem `=` na frente vira literal; `PUT /workflows/{id}` rejeita `settings` com propriedade extra (`binaryMode`) — mande só `{executionOrder:'v1'}`; **nunca silencie a resposta do PUT** (`> /dev/null` gerou deploy fantasma); **`GET` fresco imediatamente antes de cada PUT** (reusar arquivo velho desfez fix 2x na mesma noite); `staticData` serve pra memória entre execuções (paginação de fotos).

## 6. MCP — servidor de tools externo [DOC + REAL, arquitetura atual da agente-piloto]

- **[DOC]** `POST /v2/agent/{id}/mcp/add` com `name, description, mcpUrl, urlType SSE|STREAMABLEHTTP, authType NO_OAUTH|OAUTH|HEADERS, headers{}`. Resposta traz `connected`, `id`, e `url` de autorização se OAuth (`POST /v2/mcp/connect` com `code`+`state` fecha o fluxo). Tools individuais ligam/desligam (`/tool/{id}/active|inactive`) e `sync-tools` reimporta a lista.
- **[REAL] No painel, conectar via card nativo "n8n"** (não "Ferramenta personalizada"/OAuth), colando a URL do `McpTrigger`.
- **[REAL] n8n `McpTrigger` `typeVersion: 2`** = Streamable HTTP unificado (o que o GPTMaker espera). v1 usa `/sse`+`/messages`.
- **[REAL] GPTMaker NÃO injeta `chat_id`/contato nas chamadas de tool MCP** (diferente de Intention). Solução: campo "Instruções Personalizadas" de cada tool no painel (255 chars, aceita `@`): "SEMPRE inclua `chat_id` = @Identificador do Chat". Confirmado funcionando.
- **[REAL] Dentro de `ToolCode` não existe `fetch`** — use `this.helpers.httpRequest({method,url,json:true})`. `$getWorkflowStaticData('global')` funciona.
- **[REAL] Foto via MCP só devolvendo URL no JSON não é confiável** (a IA tentou "processar" o link e errou na frente do cliente). A própria tool chama `POST /v2/chat/{chatId}/send-message` com `image` — chega como imagem real.
- **Quando MCP × Intention [REAL, decisão de 12/09]**: busca/leitura → MCP (código testável, 89 testes automatizados contra a sessão MCP real); **ação com efeito no mundo (alerta WhatsApp pro dono) fica como Intention** até o MCP provar estabilidade por dias. Ao migrar, desative a Intention antiga E atualize `behavior`+treinamentos que a citam pelo nome.

## 7. Transferência, inatividade, contatos e CRM [DOC]

- **Transfer rules**: `type HUMAN` (`userId` do operador) ou `type AGENT` (`agentId` de outro agente — permite roteamento multiagente: triagem → especialista), `instructions` visíveis na transferência, `returnOnFinish` devolve pro agente original ao terminar.
- **Idle actions**: lista de `actions[{instructions, seconds ∈ {120,300,600,900,1800,3600,7200,14400,28800,86400,…,604800}, allowAllHours, workingHours[{dayWeek 0=Dom…6=Sáb, active, hours[{start,end}]}]}]` + `finishAction.seconds` (encerra o atendimento). Tipos gerados: `SEND_MESSAGE`, `TEMP_BLOCK`, `FINISH_INTERACTION`. É o follow-up nativo; prefira isso a instruir "se o cliente sumir…" no `behavior`.
- **Custom fields** (por workspace): `type STRING|DATE|DATE_TIME|NUMBER|BOOLEAN|MONEY`, `appliesTo CONTACT|DEAL` (DEAL = funil do CRM, só Standard/Corporate). Uma Intention pode gravar neles via `variables[].customField`.
- **Contatos**: `GET /v2/workspace/{ws}/search`, `PUT /v2/contact/{id}/update` (`name, phone, email, birthday` em ms, `customFieldValues[]`). Já validado funcionando — alternativa a scraping de CRM externo.
- **Fluxo humano [DOC]**: IA transfere → aba "Em espera" → operador assume ("Meus") → ao encerrar, no próximo contato a IA volta. Via API: `PUT /chat/{id}/start-human` (IA para) e `stop-human` (IA volta na próxima mensagem). Papéis de equipe: Gerente (tudo menos assinatura), Treinador (agentes + chat), Atendente (só chat).
- **Alternativa validada [REAL, concessionária-piloto]**: em vez de transferir, a IA aciona Intention que manda WhatsApp real pros donos (`start-conversation`) e encerra sozinha — o cliente não fica "em espera" esperando alguém abrir o painel.

## 8. Canais e envio ativo [DOC + REAL]

- Tipos: `Z_API, WHATSAPP` (WhatsApp Web/QR), `CLOUD_API` (Meta oficial), `INSTAGRAM, MESSENGER, TELEGRAM, WIDGET, MERCADO_LIVRE, TWILIO_SMS`. Canal é do workspace; `PUT /v2/channel/{id}` com `agentId` vincula/troca agente (null desvincula). `GET /qr-code` devolve `value` (QR) ou `connected:true`.
- Config por canal (`PUT /v2/channel/{id}/config`): `audioAction`, `startTrigger` (ex. `ONLY_WHEN_CALLING_BY_NAME`), `endTrigger` (ex. `WHEN_SAY_GOODBYE`), `enabledTyping`; Z-API ainda tem grupos (`enableGroupsResponse`, `replyGroupsType`), rejeição de chamada, "retirar atendimento" por comando (`takeOutsideService*`), mensagem de espera; Instagram tem resposta a comentários e stories. Widget: `isPublic`, `origins[]`, `initialMessage`, `suggestMessages[]`, cores; `GET /widget-links` dá `float` e `iframe`.
- **`POST /v2/channel/{id}/start-conversation`** (texto/imagem/vídeo/áudio/documento por `phone`): **[DOC] só canal WhatsApp NÃO oficial.** [REAL] Em canal Cloud API oficial funciona só dentro da janela de 24 h (erro Meta 131047 "Re-engagement message"); fora dela precisa de template aprovado pela Meta.
- **[REAL 29/09] Correção**: o canal WhatsApp da concessionária-piloto é tipo `WHATSAPP` (Web/QR, não `CLOUD_API`), por isso o `start-conversation` dos alertas entrega sem janela de 24 h. Confirmar o `type` em `GET /workspace/{ws}/channels` antes de assumir restrição da Meta.
- **`send-message`** no chat aceita `message` (+`replyMessageId`), `image`+`message`, `audio`, `video`, `document`+`documentName`+`documentMimetype`. Editar/apagar mensagem só em Z-API, Telegram e Widget.
- **Teste sem incomodar cliente [REAL]**: chamar o webhook com `chat_id` falso. Cuidado com ações reais — um teste de "Alertar Donos" mandou WhatsApp de verdade pros donos.

## 9. Modelos e custo [DOC + REAL]

**Créditos por resposta [DOC, 29/09/2026]**: GPT-5.6 Sol 14 · Terra 7 · **Luna 1** · GPT-5.5 14 · 5.4 7 · 5.4 Mini 2 · 5.2 5 · 5.1 4 · GPT-5 4 · 5 Mini 1 · 4.1 4 · 4.1 Mini 1 · o4-mini 3 · o3 5 · o3-mini 3 · o1 25 · GPT-4o 5 · 4o Mini 1 · GPT-4 Turbo 20 · **Claude 5 Sonnet 10** · 4.6 Sonnet 10 · 4.5 Sonnet 10 · **4.5 Haiku 3** · (3.x descontinuados) · LLaMA 3.3 1 · Qwen 2.5 Max 3 · DeepSeek V4 Pro 5 · V4 Flash 1 · V3 1 · Sabiá 3.1/3 3.

Enums de `prefferModel`: `GPT_5_6_SOL, GPT_5_6_TERRA, GPT_5_6_LUNA, GPT_5_5, GPT_5_4, GPT_5_4_MINI, GPT_5_2, GPT_5_1, GPT_5, GPT_5_MINI, GPT_4_1, GPT_4_1_MINI, OPEN_AI_O4_MINI, OPEN_AI_O3, OPEN_AI_O3_MINI, OPEN_AI_O1, GPT_4_O, GPT_4_O_MINI, GPT_4, CLAUDE_5_SONNET, CLAUDE_4_6_SONNET, CLAUDE_4_5_SONNET, CLAUDE_4_5_HAIKU, CLAUDE_3_7_SONNET, CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU, DEEPINFRA_LLAMA3_3, QWEN_2_5_MAX, DEEPSEEK_V4_PRO, DEEPSEEK_V4_FLASH, DEEPSEEK_CHAT, SABIA_3_1, SABIA_3`.

**Planos [DOC]**: Basic R$147/mês, 2.500 cr, 2 agentes, 2 operadores, sem CRM (cr extra R$0,06) · Standard R$497, 11.500 cr, 10/10, com CRM (R$0,05) · Corporate R$997, 30.000 cr, 20/20, com CRM (R$0,04). Créditos do plano expiram no ciclo; avulsos não. "Recarga inteligente" compra automático ao bater piso. `GET /credits` devolve `status TRIAL|ACTIVE|PAST_DUE|CANCELED`.

**Resultado empírico por modelo [REAL, agente-piloto]**:
- `GPT_5_6_LUNA` (1 cr): em 31/08 parecia fraco (placeholder em campo opcional, Intention repetida, regra ignorada). **Em 10/09, depois de corrigir os bugs de plataforma/código, funcionou muito bem** — a maioria dos "erros de modelo" era bug real. É o modelo em produção.
- `CLAUDE_4_5_HAIKU` (3 cr): falhou tool-calling e regras "nunca X" mesmo com prompt enxuto. Não usar pra extração estruturada com muita regra.
- `OPEN_AI_O4_MINI` (3 cr): **silêncio total, zero resposta** — incompatibilidade aparente com a plataforma. Evitar.
- `GPT_5` (4 cr): bom, mas disparou "Alertar Donos" 2x pro mesmo lead.
- `CLAUDE_5_SONNET` (10 cr): mais confiável em regra travada, 10x o custo do Luna.
- **Processo**: isole a variável (troque só o modelo, sem mexer em texto/código na mesma rodada); antes de culpar o modelo, procure bug de configuração; teste em workspace separado pra não queimar crédito de produção.

## 10. Conversar com o agente via API [DOC + REAL]

- `POST /v2/agent/{id}/conversation` com `contextId` (id externo do cliente — use um NOVO por cenário de teste) + `prompt` | `image` | `audio` | `video` | `document`; opcionais `callbackUrl` (vira assíncrono, resposta chega no webhook), `onFinishCallback`, `chatName`, `chatPicture`, `phone`. Resposta: `message, images[], audios[], documents[]`. Mesmo motor de produção — ótimo pra bateria de teste.
- `POST /v2/agent/{id}/add-message` com `role user|assistant` injeta mensagem no contexto sem gerar resposta — use quando outro sistema disparou uma mensagem ativa e a IA precisa "saber" que ela foi enviada.
- **[REAL] `Transaction silently rolled back because it has been marked as rollback-only`** = backend deles sob rajada (várias chamadas em segundos ou logo após `PUT /settings`). Retry com backoff (2-3 tentativas). Não é crédito, não é seu agente.
- Limpe chats de teste no fim (`DELETE /v2/chat/{id}`).

## 11. Webhooks de evento (`PUT /v2/agent/{id}/webhooks`) [DOC]

`onNewMessage` (toda mensagem), `onLackKnowLedge` (não soube responder), `onTransfer` (foi pra humano), `onFirstInteraction` (1º atendimento do cliente), `onStartInteraction` (todo início), `onFinishInteraction` (todo fim), `onCreateEvent` / `onCancelEvent` (agenda Google). Use `onFinishInteraction` + `GET /v2/interaction/{id}/messages` pra resumo/análise pós-atendimento; `onLackKnowLedge` pra descobrir buraco de treinamento.

## 12. Multi-tenant e identidade — armadilha cara [REAL]

Já existiram **2 tenants** com agente "agente-piloto" cada (um teste, um oficial). A credencial no n8n (`send-message`) era de UM tenant; o agente do outro recebia `"error on load"` genérico ao mandar foto. Custou uma sessão inteira. **Sempre**: pedir `agentId` + token da sessão (JWT curto, não persistir), conferir `GET /agent/{id}` bate com o `jobName` esperado, listar `GET /workspace/{ws}/agents` pra ver se há homônimos. Ao clonar agente (agente-clone = mesmo tenant/estoque da concessionária-piloto), reaproveitar os mesmos webhooks e credencial é correto; o que muda é nome/loja/regras de handoff.


**IDs [REAL 29/09]**: o `tenant` do JWT NÃO é o `workspaceId`. `GET /v2/workspaces` lista os workspaces reais (uma conta pode ter vários: "Meu Workspace", "LOJA-A", "PARTICULAR"); `/workspace/{ws}/chats|agents|channels|credits` só funciona com o ID do workspace certo (com o tenant devolve lista vazia ou `Index 0 out of bounds`). Chats: `GET /v2/workspace/{ws}/chats?agentId=&page=&pageSize=100` e `GET /v2/chat/{chatId}/messages?page=&pageSize=100`; `chatId` = `{channelId}-{telefone}`. Mensagens digitadas pelo dono no celular chegam com `role: assistant` (indistinguíveis da IA no texto — use as notificações `START_INTERACTION_HUMAN`/`TRANSFER_AGENT` ao redor). Auditoria completa de conversas em ~10 min com esse caminho.

## 13. Processo de teste obrigatório (validado, repetir sempre)

1. Puxar o payload REAL de uma execução do webhook/tool (n8n `GET /executions/{id}?includeData=true` — só de UMA execução, nunca em lista grande) — a IA reformula, nunca assuma o que ela manda.
2. Testar a lógica local contra dado real ANTES de subir (script `test-local.js`/Python; pro MCP, bateria contra a sessão MCP real comparando com o feed cru).
3. Reteste ponta a ponta via `POST /conversation` com `contextId` novo por cenário.
4. Conferir a execução no n8n quando envolver ação (foto, alerta, gravação) — texto de resposta bonito não prova que a Intention/tool disparou.
5. Checar `GET /credits` antes de bateria grande; TRIAL compartilha pool com produção.
6. Depois de qualquer PUT (agente, settings, intention, workflow): `GET` de volta e comparar campo a campo. Depois de mudar nome/estado de uma Intention: grep em `behavior` + todos os treinamentos.
7. Reproduzir bug relatado pelo cliente com dado real antes de corrigir; o relato costuma estar certo mas a causa e o alcance (3 fluxos, não 1) só aparecem investigando.

## Por que isso importa

GPTMaker é caixa-preta com doc boa em "o que existe" e muda em "como se comporta". Cada regra [REAL] aqui custou pelo menos uma sessão e, várias vezes, um cliente atendido errado. Sem este documento, cada agente novo (ou cada sessão nova no mesmo agente) reintroduz os mesmos ~25 bugs já resolvidos uma vez.
