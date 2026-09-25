# Claude Code — do zero ao deploy

Fluxo que uso na Automind AI pra construir sistemas com o Claude Code: da ideia bruta até o deploy, com validação, vistoria e auditoria de segurança antes de ir pra produção.

Página da live, com o roteiro visual: https://dicaslive.automindai.ia.br/

Duas formas de pegar o material: clonar este repositório (vem a skill pronta) ou baixar arquivo por arquivo na página da live.

## O que tem aqui

| Pasta/arquivo | Pra quê |
|---|---|
| `PASSO-A-PASSO-COMPLETO.md` | Documento mestre. Comece por ele |
| `prompts/` | Os prompts de cada etapa, na ordem do fluxo, pra copiar e colar |
| `skills/automind-ai-startup/` | O mesmo fluxo empacotado como skill do Claude Code |
| `COMO-CRIAR-SKILLS.md` | Como criar, testar e tornar obrigatória a sua própria skill |

### Ordem dos prompts

| Arquivo | Etapa | Onde usar |
|---|---|---|
| `00a-infra-do-zero.md` | VPS, Claude Code (Ubuntu/WSL, Opus 5.5), Supabase, n8n | Terminal + VPS |
| `00-contexto-infraestrutura.md` | Descrever a infra que você já tem | Anexar nos chats |
| `00b-acesso-claude-code.md` | Dar acesso real ao Claude Code (GitHub, SSH, Cloudflare, n8n) | Terminal |
| `01-prompt-deepseek.md` | Ideia → briefing estruturado | DeepSeek |
| `02-arquiteto-senior-reformulador.md` | Briefing → spec sem lacunas | Claude Projects |
| `03-prompt-claude-ia.md` | Spec → workspace do Claude Code (`CLAUDE.md` + fases) | Claude Projects |
| `04-validacao-funcional-pre-vistoria.md` | Tudo que deveria existir existe? | Claude Code |
| `05-vistoria-sem-corrigir.md` / `05-vistoria-com-correcao.md` | Vistoria ponta a ponta | Claude Code |
| `06-prompt-seguranca.md` | Auditoria de segurança em fases | Claude Code |
| `07-auditoria-geral-final.md` | Veredito final antes do deploy | Claude Code |
| `08-prompt-mais-usados.md` | Consulta rápida de prompts de segurança | — |

## Instalar a skill

Com o Claude Code já funcionando:

```bash
git clone https://github.com/startupautomindai-dot/claude-code-do-zero-ao-deploy.git
mkdir -p ~/.claude/skills
cp -r claude-code-do-zero-ao-deploy/skills/automind-ai-startup ~/.claude/skills/
```

Abra o Claude Code de novo. A skill entra sozinha quando você começa um projeto novo, pede uma feature, uma vistoria, uma auditoria ou vai fazer deploy. Pra chamar na mão: `/automind-ai-startup`.

Quer criar a sua? Veja [`COMO-CRIAR-SKILLS.md`](COMO-CRIAR-SKILLS.md).

Antes de instalar qualquer skill (esta ou de terceiros), leia o conteúdo. Skill é instrução que o Claude Code vai seguir com o seu acesso.

## Licença

MIT. Pode usar, adaptar e redistribuir.
