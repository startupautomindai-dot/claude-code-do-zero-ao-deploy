# TRAVOU? PEDE AJUDA AO CLAUDE (vale em qualquer etapa)

No começo vai travar. Terminal que não abre, comando que dá erro, arquivo que
você não sabe onde salvar, resposta da IA que não fez sentido. Nada disso é
motivo pra parar: o próprio Claude, no chat (claude.ai), destrava se você
perguntar do jeito certo.

═══════════════════════════════════════════
1. MONTE UM AJUDANTE QUE CONHECE O ROTEIRO (5 minutos, uma vez só)
═══════════════════════════════════════════

1. claude.ai → Projects → New Project. Nome: "Ajudante da live".
2. Em Instruções do projeto, cole:

    Você ajuda uma pessoa que está começando com o Claude Code a seguir o
    roteiro "do prompt ao deploy" (arquivos anexos). Ela não é programadora.
    Regras: responda em português simples; uma coisa de cada vez; sempre diga
    em qual etapa e em qual arquivo do roteiro ela está; quando houver um
    comando, mostre o comando completo e diga em qual terminal rodar (Ubuntu,
    VPS ou dentro do Claude Code); quando houver erro, explique a causa em 1
    frase antes da solução; nunca peça senha, token ou chave, e avise se ela
    colar um por engano. Se a dúvida for sobre o que construir (regra de
    negócio), pergunte antes de sugerir.

3. Em Conhecimento do projeto, anexe: PASSO-A-PASSO-COMPLETO.md,
   00a-infra-do-zero.md, 00b-acesso-claude-code.md, 00c-guia-de-bolso-stack.md,
   00d-qual-llm-para-cada-funcao.md.

Pronto. Toda dúvida vai nesse Project; ele sabe o roteiro inteiro.

═══════════════════════════════════════════
2. COMO PERGUNTAR (copie e complete)
═══════════════════════════════════════════

Erro em comando ou terminal:

    Estou na Etapa [número], passo [x.y]. Rodei este comando no [Ubuntu/VPS/
    Claude Code]:
    [comando]
    Apareceu isto:
    [cole o erro inteiro]
    O que aconteceu e qual é o próximo passo? Uma coisa de cada vez.

Não sei onde salvar ou o que fazer com um arquivo:

    Estou na Etapa [número]. O Claude gerou este bloco:
    [cole as 3 primeiras linhas]
    Onde salvo, com que nome, e o que faço depois?

A IA respondeu algo estranho (no DeepSeek, no Project ou no Claude Code):

    Na Etapa [número] eu mandei:
    [sua mensagem]
    e recebi:
    [resposta]
    Isso está certo pro roteiro? Se não, o que eu mando de volta?

Não entendi um termo:

    O que é [termo] no contexto da Etapa [número]? Explique com um exemplo do
    meu projeto: [1 frase sobre o projeto].

Perdi o fio:

    Terminei a Etapa [número] e não sei o que vem depois. Me diga só o próximo
    passo e o arquivo que eu abro.

═══════════════════════════════════════════
3. REGRAS QUE EVITAM DOR DE CABEÇA
═══════════════════════════════════════════

- Cole o erro inteiro, do jeito que apareceu. "Deu erro" não ajuda ninguém.
- Diga sempre a etapa e o passo. O ajudante responde pelo roteiro.
- Uma dúvida por mensagem. Três dúvidas juntas viram uma resposta pela metade.
- Nunca cole senha, token ou chave. Se precisar mostrar, troque por "XXXX".
- Print funciona: arraste a imagem pro chat (ou pro Claude Code) e pergunte.
- Se a resposta mandar rodar algo que apaga ou reinicia (rm, drop, restart,
  force), pergunte antes: "o que isso apaga?".
- Dentro do Claude Code também dá pra perguntar, sem mexer em nada: comece a
  mensagem com "Não faça nada ainda, só me explique:".
