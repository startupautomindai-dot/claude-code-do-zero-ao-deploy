# Extrair a marca real do cliente

Cliente reconhece a própria marca na hora. Paleta "parecida" ou logo trocado por círculo com sigla sinaliza que ninguém prestou atenção. Extraia os valores reais; não chute.

## 1. Baixar o HTML e o CSS brutos

Use `curl`, não resumo de página. Ferramenta que resume via LLM perde hex, nome de fonte e valores exatos.

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
mkdir -p marca && cd marca
curl -sL "https://site-do-cliente.com.br" -A "$UA" -o index.html
# listar CSS linkados (prestar atenção em design-tokens, variables, theme)
grep -oE '<link[^>]+\.css[^"]*"' index.html | grep -oE 'href="[^"]+"' | cut -d'"' -f2
# baixar cada um (completar URL relativa com o domínio)
curl -sL "https://site-do-cliente.com.br/caminho/style.css" -A "$UA" -o style.css
```

## 2. Tirar os valores de dentro do CSS

```bash
# variáveis de cor
grep -ohE '\-\-[a-zA-Z0-9-]*:\s*#[0-9a-fA-F]{3,8}' *.css index.html | sort | uniq -c | sort -rn | head -20
# cores mais usadas no geral
grep -ohE '#[0-9a-fA-F]{6}\b' *.css index.html | sort | uniq -c | sort -rn | head -15
# fontes
grep -ohE 'font-family:[^;}]+' *.css index.html | sort | uniq -c | sort -rn | head
# raio padrão (o mais frequente é o da marca; quase sempre 4-8px, não 16-24px)
grep -ohE 'border-radius:[^;}]+' *.css index.html | sort | uniq -c | sort -rn | head
# peso dos títulos (geralmente 500-600, não 700-800)
grep -ohE 'h[1-3][^{]*\{[^}]*font-weight:[^;}]+' *.css index.html | head
# sombra de card (site corporativo costuma usar borda fina de 1px e nenhuma sombra)
grep -ohE 'box-shadow:[^;}]+' *.css index.html | sort | uniq -c | sort -rn | head
```

Sem nenhum `.css` baixado, o CSS está dentro do `index.html` (os comandos acima já olham os dois). Site montado com JavaScript (CSS não aparece no HTML): abra no Playwright e leia os valores computados:

```js
getComputedStyle(document.querySelector('header')).backgroundColor
getComputedStyle(document.querySelector('h1')).fontFamily
```

## 3. Logo e imagens reais

```bash
grep -oE '<img[^>]+>' index.html | grep -iE 'logo|brand|marca'
grep -oE 'https?://[^"'\'' )]+\.(svg|png|webp)' index.html *.css | grep -i logo | sort -u
```

Prefira SVG. Sem logo acessível: peça ao cliente, e nunca invente um substituto.

## 4. Registrar nos tokens

Tudo que foi extraído vai pro `tokens.css` com um comentário de origem (`/* site oficial, header */`). Depois compare lado a lado o print do seu app com o print do site oficial: o fundo bate? a tipografia bate? o raio bate?
