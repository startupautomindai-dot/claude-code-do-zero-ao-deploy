# Como criar skills no Claude Code

Skill é uma pasta com instruções que o Claude Code carrega sozinho quando a situação pede. Em vez de colar o mesmo prompt toda vez, você escreve uma vez e ele passa a seguir aquilo em todo projeto.

Exemplo real neste repositório: `skills/automind-ai-startup/` (o fluxo da live inteiro virou uma skill).

---

## 1. Estrutura mínima

```
minha-skill/
└── SKILL.md
```

Só isso já funciona. Com material de apoio:

```
minha-skill/
├── SKILL.md              # o essencial, curto
└── references/           # detalhes que só abrem quando precisa
    ├── 01-etapa.md
    └── 02-etapa.md
```

## 2. Onde colocar

| Pasta | Vale pra |
|---|---|
| `~/.claude/skills/minha-skill/` | Você, em todos os projetos |
| `.claude/skills/minha-skill/` (dentro do repo do projeto) | Todo mundo que abrir aquele projeto |

Depois de criar, feche e abra o Claude Code de novo.

## 3. O arquivo SKILL.md

```markdown
---
name: minha-skill
description: Use when [situação que dispara]. Also triggers on "palavra 1", "palavra 2".
---

# Título

## Princípio
Uma ou duas frases com a regra central.

## Quando aplicar cada coisa
| Situação | O que fazer | Referência |
|---|---|---|
| ... | ... | `references/01-etapa.md` |

## Erros comuns
| Erro | Correção |
|---|---|
| ... | ... |
```

### Regras do cabeçalho (entre os `---`)

- **`name`**: só letra minúscula, número e hífen. `automind-ai-startup` funciona; `Automind_AI_Startup` não.
- **`description`**: é o que o Claude Code lê pra decidir se abre a skill. Escreva **QUANDO usar**, não o que ela faz por dentro.
  - Ruim: `description: Faz spec, depois constrói por fases, depois audita`. Ele segue o resumo e pula o resto.
  - Bom: `description: Use when starting a new system or adding a feature, before writing code`.
  - Coloque as palavras que você realmente fala: "projeto novo", "vistoria", "deploy".

### Corpo

- **Curto.** O `SKILL.md` deve caber numa leitura rápida. Tabela e lista, não texto corrido.
- **Detalhe vai pra `references/`.** O `SKILL.md` aponta: "abra `references/06-seguranca.md` e siga o protocolo". O arquivo só entra no contexto quando precisa, e isso economiza tokens.
- **Regra, não história.** Nada de "no dia X aconteceu Y". Escreva o que fazer.
- **Um exemplo bom** vale mais que cinco mais ou menos.

## 4. Testar (não pule)

Skill que você não testou você não sabe se funciona. Abra o Claude Code numa pasta de projeto e pergunte sem citar o nome da skill:

```
claude -p "Um cliente quer um sistema novo de agendamento. Qual skill você carregaria primeiro e qual a primeira etapa dela? 3 linhas."
```

- **Escolheu a sua skill?** Funcionou.
- **Escolheu outra?** Melhore a `description` (mais palavras de gatilho) ou veja o item 5.
- **Rode 2 ou 3 vezes.** Uma resposta só pode ser sorte.

Pra chamar na mão, a qualquer momento: `/minha-skill`.

## 5. Tornar a skill obrigatória

Quando existem várias skills instaladas, outra pode "ganhar" a disputa. Aconteceu com a `automind-ai-startup`: no primeiro teste o Claude Code escolheu outra skill de processo.

A solução é o `CLAUDE.md`, porque instrução dele tem prioridade sobre qualquer skill. Adicione uma linha:

```markdown
## Regras obrigatórias
- Todo projeto e toda feature seguem a skill `minha-skill`. Carregar ANTES de qualquer outra skill de processo.
```

- `CLAUDE.md` na raiz do projeto: vale só naquele projeto.
- `CLAUDE.md` na sua pasta pessoal (ex.: `/home/seu-usuario/CLAUDE.md`): vale pra todos os projetos dentro dela.

Depois disso, teste de novo (item 4).

## 6. Manter atualizada

Deixe a skill num repositório Git e aponte a pasta de skills pra ela com um link simbólico:

```bash
git clone https://github.com/seu-usuario/suas-skills.git ~/suas-skills
ln -s ~/suas-skills/minha-skill ~/.claude/skills/minha-skill
```

Melhorou a skill? `git commit` + `git push`. Nas outras máquinas, `git pull`. Uma fonte só, nunca cópias soltas.

## 7. Segurança

- **Leia antes de instalar qualquer skill de terceiro.** Skill é instrução que o Claude Code segue com o SEU acesso (SSH, GitHub, banco).
- **Instale a partir do repositório original**, conferindo o endereço. Nunca por um nome de pacote que "parece" certo.
- **Nunca coloque senha, token, IP de servidor ou dado de cliente dentro de uma skill**, principalmente se o repositório for público.

## Checklist rápido

- [ ] Pasta com o nome da skill (minúsculas e hífen)
- [ ] `SKILL.md` com `name` e `description` ("Use when...")
- [ ] Corpo curto, detalhes em `references/`
- [ ] Testada com `claude -p` sem citar o nome, 2 ou 3 vezes
- [ ] Se tem que ser padrão: linha no `CLAUDE.md`
- [ ] Versionada no Git, instalada por link simbólico
- [ ] Sem segredo nenhum dentro
