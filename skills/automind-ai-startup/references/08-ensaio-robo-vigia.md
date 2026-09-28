# 08 — Ensaio, robô de jornada e vigia: o cliente não é o testador

## Por que existe

Teste que roda contra backend simulado passa e o cliente acha o bug no dia seguinte. As falhas que chegam no cliente quase nunca estão na função que acabou de ser mexida: estão na **sincronização entre aparelhos**, nos **dados reais de meses** e na **conta que não fecha entre telas**. Nada disso aparece com mock. Esta etapa fecha esse buraco com três peças obrigatórias em todo sistema que já tem cliente usando.

## 1. Ambiente de ensaio

Cópia do sistema no mesmo servidor, separada da produção:

- Banco, auth, API e n8n próprios. **Chaves próprias**: nenhuma igual à produção (conferir por script).
- Portas só em `127.0.0.1`. O robô acessa por túnel SSH. Nada exposto na internet.
- **Dados:** script que copia a produção (só leitura, `pg_dump`) pro ensaio, agendado toda madrugada e rodado antes de cada bateria.
- **Fluxos do n8n:** copiados da produção com host do banco e chaves trocados pelos do ensaio. **Ficam de fora** os que falam com o mundo externo (WhatsApp, e-mail, IA paga, agendados, monitor): o ensaio nunca manda mensagem pra cliente.
- **Login do robô:** no ensaio, o login de um cliente real recebe uma senha de robô. A produção fica intocada; conferir que a mesma senha é recusada na produção.
- Reiniciar ou recriar container do ensaio é livre. Na produção, seguir a regra de confirmação. Recriar container desfaz `docker network connect` manual: religar sempre.

## 2. Robô de jornada

Script (Playwright) que usa o sistema **como o cliente usa**, contra o ensaio:

- Sobe a versão **ainda não publicada** do front local e desvia as chamadas de API/webhook de produção pro ensaio. Todo o resto do domínio da empresa fica bloqueado.
- **Dois aparelhos com o mesmo login** (desktop e celular), porque metade dos bugs é de sincronização.
- Faz a rotina real, com os pontos de entrada que a tela usa (formulário + botão): criar, importar, lançar com data antiga, transferir, lançar pelo segundo aparelho, editar, excluir.
- **Depois de cada passo**, confere:
  1. aparelho A = aparelho B, item por item;
  2. app = banco, com a conta refeita **pelo robô** direto das linhas do banco (nunca reusar a função do app pra conferir o app);
  3. total do painel = soma dos itens;
  4. subtotais (por categoria, marca etc.) fecham com o total;
  5. excluído não volta (2 sincronizações em cada aparelho);
  6. a data gravada é a escolhida, não a de hoje.
- **Provar que o robô reprova:** injetar um defeito numa cópia do front (ex.: saída baixando 1 a menos) e exigir que ele falhe. Robô que só passa não prova nada.
- **Toda reclamação de cliente vira um passo do robô** antes de ser dada como resolvida.

## 3. Portão de publicação

Um único comando de publicação (`scripts/publicar.sh`) que, **em ordem e parando no primeiro erro**:

1. roda os testes locais (tem que dar 0 falhas);
2. roda o robô de jornada no ensaio (tem que passar inteiro);
3. carimba a versão (os aparelhos se atualizam sozinhos);
4. faz backup da produção, publica, confere hash e abre a produção exigindo zero erro de página;
5. commit + push.

Publicar por fora do portão (scp na mão, copiar arquivo) é proibido.

## 4. Vigia diário

Função **só leitura** no banco (`vigia_consistencia()`, executável só pela chave de serviço) com as regras de consistência do domínio: estoque negativo, par de transferência faltando, lançamento duplicado, registro órfão, tabela sem RLS. Um fluxo agendado roda de manhã e **só avisa no WhatsApp quando há problema**, antes de o cliente abrir o sistema. Contas de teste ficam de fora da contagem.

## Checklist de entrega (anexar no relatório)

- [ ] Ensaio atualizado com dados de hoje
- [ ] Robô: N conferências, 0 falhas (colar o placar)
- [ ] Robô reprovou a cópia com defeito injetado (quando o robô for novo ou mudar)
- [ ] Publicado pelo portão, versão X, hash conferido, produção sem erro
- [ ] Cenário novo no robô pra cada reclamação atendida
