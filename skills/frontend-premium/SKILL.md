---
name: frontend-premium
description: Use when building, redesigning or fixing any user-facing UI — site, landing page, app, PWA, painel, dashboard, protótipo, tela, layout, CSS — before writing any CSS or components. Also triggers on "frontend", "interface", "identidade visual", "ficou feio", "cara de IA", "deixa mais bonito", "redesenhar", and when the client already has an official site or brand.
---

# Frontend premium

## Princípio

Frontend fica genérico por três motivos: CSS escrito sem referência visual, entrega declarada sem olhar o resultado, e aprovação só no fim. Esta skill fecha os três. **Nenhuma tela é entregue sem print verificado.**

## Processo (na ordem, sem pular)

**1. Referência antes de qualquer CSS.** Classifique e siga:

| Caso | O que fazer |
|---|---|
| Cliente tem site/marca | Extrair cores, fontes, raio, sombra e logo **reais** → `references/extrair-marca.md` |
| Sem marca | Direção estética deliberada. Se a skill `frontend-design` estiver instalada, carregue e siga o processo dela. Registre 1 frase de conceito + o elemento-assinatura |
| Painel/app interno | Sóbrio e denso de informação: 1 cor de destaque, neutros, tabela bem feita > card decorado |

**2. Tokens num arquivo só, antes de componente.** `tokens.css` (ou `theme` do Tailwind): 4–6 cores nomeadas em hex, 2 fontes no máximo (display + texto) e 1 mono se precisar, escala de tipo, escala de espaçamento (4/8), 1 raio padrão, 1 sombra (só pra elemento elevado). Componente nenhum usa valor solto fora dos tokens.

**3. Uma tela primeiro, a principal.** Construa só ela, com conteúdo real (nunca lorem ipsum; nome, número e foto de verdade). Rode a verificação (passo 6) e **mostre o print pro usuário aprovar a direção** antes de fazer as outras. Direção errada descoberta aqui custa 1 tela; no fim custa o projeto.

**4. Completude de cada tela.** Estados: loading, vazio (com ação), erro (com como resolver), sucesso, sem permissão. Botão com verbo do que acontece ("Salvar alterações", não "Enviar"); o toast repete o verbo ("Alterações salvas"). Foco visível no teclado, labels em campo, alt em imagem. Checklist completo: skill `automind-ai-startup`, `references/02-spec-sem-lacunas.md`.

**5. Evitar o visual de IA.** Revisar contra `references/anti-cara-de-ia.md` antes de mostrar qualquer coisa.

**6. Verificação visual — obrigatória a cada entrega:**

```bash
python3 scripts/verificar-visual.py <url-ou-file:///caminho/index.html> verificacao/
```

Prints em celular (390), tablet (768) e desktop (1280), mais auditoria de largura, console, imagens, contraste WCAG AA e emoji-como-ícone.
- **FALHA** = corrigir e rodar de novo até zerar.
- **ATENÇÃO** (raio, sombra, gradiente, fontes) = ajustar ou justificar em 1 linha.
- **Abrir e olhar os prints** (Read na imagem). O script não vê hierarquia, alinhamento nem "isso está feio". Você vê.
- Clicar em cada botão e link da tela (Playwright): nada pode ser enfeite que não faz nada.

**7. Entrega** com os prints de celular e desktop anexados, não "está pronto".

## Complementos (usar se instalados)

| Skill | Quando |
|---|---|
| `frontend-design` (Anthropic) | Passo 1 sem marca: direção estética e tipografia |
| `web-design-guidelines` (Vercel) | Depois do passo 6: auditoria do código da UI, com `arquivo:linha` |
| `vercel-react-best-practices` (Vercel) | Projeto React/Next.js: performance e estrutura |
| `shadcn` (skill ou MCP) | App React: componentes prontos e acessíveis em vez de reinventar botão/modal |

## Erros comuns

| Erro | Correção |
|---|---|
| Inventar paleta "bonita" pra cliente com marca | Extrair a real (`references/extrair-marca.md`) |
| Construir todas as telas e mostrar no fim | Uma tela, print, aprovação, depois o resto |
| "Está pronto" sem print | Passo 6 sempre, com prints anexados |
| Só o estado de sucesso | Os 5 estados em cada tela |
| Texto cinza-claro "elegante" | Contraste mínimo 4.5:1 (o script acusa) |
| Emoji como ícone | SVG de traço simples, mesmo estilo em todos |
