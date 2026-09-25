# Sinais de "feito por IA": revisar antes de mostrar

Cada item abaixo é o padrão que sai quando não houve decisão. Pode aparecer se for escolha consciente pro projeto, justificada em 1 linha, nunca por padrão.

## Visual

| Sinal | No lugar |
|---|---|
| Emoji como ícone (🏠 📅 🚀) | SVG de traço simples, mesma espessura em todos |
| Canto muito arredondado em tudo (16-24px) | 1 raio padrão da marca, geralmente 4-8px |
| Sombra grande em todo card | Borda fina de 1px; sombra só em modal, dropdown e botão flutuante |
| Gradiente decorativo (roxo→azul, texto degradê) | Cor sólida; gradiente só se for da marca |
| Título em 700-800 em tudo | Hierarquia por tamanho e espaço; título em 500-600 |
| Hero com "número grande + label pequena + 3 cards de feature" | Abrir com o que é mais característico do negócio: produto real, foto real, dado real |
| Grade de 3 cards iguais com ícone em cima | Variar o layout conforme o conteúdo; nem tudo é card |
| Numeração decorativa (01 / 02 / 03) sem ser sequência | Só numerar quando a ordem importa |
| Moldura de celular pra "parecer app" | Responsivo de verdade |
| Glassmorphism, blur e brilho em tudo | Superfícies sólidas e contraste claro |
| Três looks que a IA repete: fundo creme com serifada e terracota; fundo quase preto com um único verde ácido; layout de jornal com filetes e zero raio | Legítimos só quando o projeto pede. Se caiu num deles sem motivo, refazer a direção |

## Texto

| Sinal | No lugar |
|---|---|
| "Transforme seu negócio", "Solução completa", "Revolucione" | Dizer o que faz, em palavras concretas do cliente |
| Botão "Enviar", "Clique aqui", "Saiba mais" | Verbo do resultado: "Agendar horário", "Baixar proposta" |
| Lorem ipsum, "João Silva", "Empresa XYZ" | Conteúdo real do cliente, ou peça antes de construir |
| Erro "Ops! Algo deu errado 😢" | O que aconteceu + como resolver, sem pedir desculpa |
| Estado vazio "Nada por aqui" | Convite pra agir: "Nenhum cliente ainda. Cadastrar o primeiro" |

## Estrutura

- Espaçamento irregular (margens "no olho"): usar só valores da escala de tokens.
- Alinhamentos quase iguais (texto a 22px e card a 24px da borda): tudo no mesmo grid.
- Hierarquia plana, tudo com o mesmo peso visual: 1 coisa principal por tela.
