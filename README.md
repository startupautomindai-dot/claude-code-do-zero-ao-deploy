# Claude Code — do zero ao deploy

Fluxo que uso na Automind AI pra construir sistemas com o Claude Code: da ideia bruta até o deploy, com validação, vistoria e auditoria de segurança antes de ir pra produção.

Página da live, com o roteiro visual: https://dicaslive.automindai.ia.br/

Duas formas de pegar o material: clonar este repositório (vem a skill pronta) ou baixar arquivo por arquivo na página da live.

## O que tem aqui

| Pasta/arquivo | Pra quê |
|---|---|
| `PASSO-A-PASSO-COMPLETO.md` | Documento mestre. Comece por ele |
| `prompts/` | Os prompts de cada etapa, na ordem do fluxo, pra copiar e colar |
| `skills/automind-ai-startup/` | O fluxo inteiro (spec → fases → validação → vistoria → segurança → deploy) como skill |
| `skills/frontend-premium/` | Skill de frontend: marca real, tokens, aprovação da 1ª tela e verificação visual automática |
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
cp -r claude-code-do-zero-ao-deploy/skills/* ~/.claude/skills/
```

Abra o Claude Code de novo. As skills entram sozinhas:
- `automind-ai-startup`: projeto novo, feature, vistoria, auditoria, deploy. Na mão: `/automind-ai-startup`.
- `frontend-premium`: qualquer tela, site, landing ou painel. Na mão: `/frontend-premium`.

Pra garantir que elas tenham prioridade sobre outras skills instaladas, veja o item 5 de [`COMO-CRIAR-SKILLS.md`](COMO-CRIAR-SKILLS.md).

### Verificação visual (vem com a `frontend-premium`)

```bash
pip install playwright && playwright install chromium
python3 ~/.claude/skills/frontend-premium/scripts/verificar-visual.py https://seu-site.com.br
```

Gera prints em celular, tablet e desktop e aponta estouro de largura, erro de console, imagem quebrada, contraste abaixo do WCAG AA, emoji como ícone e sinais de "cara de IA".

### Skills de terceiros que combinam com a `frontend-premium`

- [`frontend-design`](https://github.com/anthropics/skills) (Anthropic): direção estética quando o projeto não tem marca.
- [`web-design-guidelines` e `react-best-practices`](https://github.com/vercel-labs/agent-skills) (Vercel): auditoria de UI e boas práticas de React/Next.js.
- [`shadcn`](https://github.com/shadcn-ui/ui/tree/main/skills/shadcn): componentes React prontos e acessíveis.

Leia antes de instalar. O `web-design-guidelines` baixa as regras da internet a cada uso.

Quer criar a sua? Veja [`COMO-CRIAR-SKILLS.md`](COMO-CRIAR-SKILLS.md).

Antes de instalar qualquer skill (esta ou de terceiros), leia o conteúdo. Skill é instrução que o Claude Code vai seguir com o seu acesso.

## Licença

MIT. Pode usar, adaptar e redistribuir.
