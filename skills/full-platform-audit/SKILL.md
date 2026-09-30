---
name: full-platform-audit
description: Use when asked to do a general/full inspection of a web app or platform ("inspeção geral", "análise de ponta a ponta", "o que está pendente", "o que falta na plataforma"). Prevents shallow audits that only screenshot each screen without actually clicking/testing each control.
---

# Auditoria completa de plataforma

Nasceu de um erro real: pedido pra fazer "inspeção geral em todas as funções, menu e etc" foi respondido navegando por cada tela e tirando print — sem clicar em cada botão. Resultado: o usuário passou 2+ horas descobrindo, um por um, bugs e lacunas reais que uma auditoria de verdade teria achado de uma vez (status de conexão que mentia, botão que só funcionava em alguns casos sem aviso, campo sem opção de editar, tela vazia sem função, oportunidade óbvia de integração entre duas telas que já existiam). Isso não é aceitável — o pedido de "inspeção" é implicitamente um pedido de teste funcional, não de tour visual.

## Regra central

**Print de tela ≠ teste.** Uma auditoria só conta como feita depois de:
1. Clicar em CADA botão/toggle/link de CADA tela (não só nos óbvios).
2. Preencher e submeter CADA formulário com dado real (não deixar em branco supondo que "deve funcionar").
3. Testar o MESMO fluxo em pelo menos 2 estados diferentes quando aplicável (ex: com dado presente e sem dado; conectado e desconectado; com permissão e sem permissão).
4. Ler o texto de cada mensagem de erro/vazio/tooltip e perguntar "isso reflete a realidade agora, ou só reflete uma condição que já foi verdade um dia?" — telas que checam "existe um valor salvo" em vez de "o estado real agora" são a fonte nº1 de bug tipo "diz que tá conectado mas não tá".

## Processo

1. **Listar TODAS as telas/menus/sub-abas** antes de começar — não pular nenhuma achando que "essa não deve ter nada demais". Usar a navegação real do app (clicar em cada item de menu), não confiar em memória de sessões passadas.
2. **Para cada tela, perguntar e testar de verdade:**
   - Existe alguma ação (botão/toggle) que parece condicional? Testar as DUAS condições (ligado/desligado, com/sem dado).
   - Existe algum texto fixo que descreve um estado (ex: "Configurado", "Conectado", "Disponível")? Verificar se esse texto vem de uma checagem em tempo real ou só da existência de um campo salvo — essa distinção é onde a maioria dos bugs desse tipo mora.
   - Existe uma lista vazia ou tela "ainda não construída"? Isso é uma pendência real — reportar, não ignorar.
   - Existem duas telas/menus que fazem sentido se conectarem (ex: um dado gerado numa tela que deveria aparecer/alimentar outra) e hoje não se falam? Isso é uma sugestão de produto que vale relatar mesmo sem ter sido pedida.
3. **Cruzar com o que já foi construído na sessão** — releia rapidamente o que foi implementado antes de dizer "está pendente"; não redescobrir o que já existe (mas também não presumir que existe sem testar).
4. **Compilar em 3 blocos, sempre**:
   - **Bugs reais encontrados e corrigidos** (com a causa raiz, não só o sintoma).
   - **Pendências reais** (tela vazia, função prometida mas não implementada).
   - **Sugestões de melhoria** (o que não foi pedido mas agrega valor, dado o que já existe).
5. Se o usuário disser "já te avisei disso" ou repetir uma reclamação — é sinal de que a correção anterior não foi realmente testada, só aplicada no código. Voltar e testar com Playwright/clique real antes de responder de novo.

## Por que isso importa

Ver também [[feedback-autonomia-testar-antes-reportar]] — esse é o mesmo princípio ("testar antes de reportar"), mas aplicado especificamente ao pedido de "inspeção/auditoria geral", que é fácil de responder de forma preguiçosa (só olhando telas) porque parece um pedido de leitura, não de teste.
