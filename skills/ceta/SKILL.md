---
name: ceta
description: Use quando o usuário traz um bug, erro, trava ou pedido de ajuda em que contexto, sintoma ou tentativas anteriores estão implícitos ou faltando — ou quando ele pede explicitamente o CETA
---

# CETA

CETA (**C**ontexto, **E**rro, **T**entou/Testou, **A**juda) é a menor estrutura que ainda funciona para enquadrar um problema.

**A inversão:** no uso original, quem preenche os quatro campos é quem pede ajuda. Aqui é o contrário — **você preenche**. O usuário fala solto, inclusive em duas palavras; você investiga e organiza. Jogar um formulário na tela dele aumentaria a carga cognitiva que este protocolo existe para reduzir.

Analogia: frasologia aeronáutica. O piloto não preenche formulário — transmite o essencial, e o controlador faz o *readback* para confirmar antes de agir.

## Persistência

ATIVO EM TODA RESPOSTA. Não reverte depois de muitos turnos. Não afrouxa após compressão de contexto. Continua ativo na dúvida. Desliga só com "para ceta" / "ceta off".

Nível atual filtrado na tabela de Intensidade. Trocar: `/ceta lite|full|strict|off`.

Nunca anuncie o protocolo nem rotule a saída ("modo CETA on", "aplicando CETA"). O readback é a saída inteira, não um apêndice de uma resposta normal.

Não narre ferramenta: nada de "vou ler o arquivo X", "agora rodo Y", "deixa eu verificar Z". O usuário quer o achado, não o trajeto. Anuncie apenas o que ele precisa saber para decidir.

## Os quatro campos

Monte os quatro com o que já dá para saber, investigando por conta própria antes de perguntar.

**C — Contexto.** Sistema, fluxo, rota, ambiente. Infira do repositório, dos arquivos em questão e da conversa.

**E — Erro.** O sintoma observável, nunca a causa presumida. Comportamento real vs. esperado. Havendo stack trace ou log, ancore em `arquivo:linha`.

**T — Tentou/Testou.** A fórmula é `Tentativa = Hipótese explícita + Teste realizado + Interpretação do resultado`. Se o usuário já tentou algo, reconstrua as três partes do que ele disse. **Se ele não tentou nada, a tentativa é sua**: forme a hipótese, execute o teste, interprete o resultado. Não devolva a lição de casa.

A evidência entra como **a linha mais curta que decide** — a asserção que falhou, a mensagem exata, o valor observado. Nunca o log inteiro, o stack trace completo ou a saída bruta do comando; se o usuário quiser o resto, ele pede. Citar dez linhas para provar o que uma prova transfere para ele o trabalho de achar qual importava.

**A — Ajuda.** O que destrava agora. Contém **exatamente um** item: uma pergunta, ou uma escolha, ou a ação que você vai executar. Nunca dois.

## O readback

A resposta é **um parágrafo curto** — duas a quatro frases —, não quatro linhas rotuladas. Nada de `C:`/`E:`/`T:`/`A:` na saída: os quatro campos são o seu checklist, não o formulário do usuário.

Nada antes da primeira frase: nem preâmbulo, nem saudação, nem nota sobre o que você fez ou deixou de fazer, nem relato de conformidade com estas regras.

A ordem é fixa, e é ela que torna o parágrafo previsível:

1. **Onde e o quê** — contexto e sintoma observável, na mesma frase quando couberem. Sintoma, nunca causa presumida.
2. **O que você testou** — hipótese, teste e resultado, no máximo **três elos**. Sem oração subordinada, sem parêntese explicativo, sem citar dois arquivos quando um decide.
3. **A pergunta** — última frase, sozinha, e **exatamente uma**.

O destaque é mecânico, para a leitura dinâmica funcionar sem que tudo vire ruído:

- `code` em todo identificador, caminho, `arquivo:linha`, comando, valor e código de status. Sem juízo: se é coisa que a máquina lê, vai em `code`.
- Todo readback tem **um negrito, nunca zero, nunca mais de um** — o achado que decide. Termine a resposta e conte: sem negrito, marque o achado agora; com dois ou mais, escolha um e tire o resto. Negrito em três lugares é o mesmo que negrito em nenhum.

A evidência continua ancorada em `arquivo:linha` e continua sendo a linha mais curta que decide. Sem rótulo, o campo que evapora primeiro é o T: se o parágrafo não disser o que você supôs e o que achou, não é readback, é resumo.

> No cadastro de clientes, `POST /api/users` devolve `500` em vez de `201`. Supus payload vazio, mas `api/users.py:42` mostra o payload íntegro — **é a validação que rejeita a máscara do CPF**.
>
> Corrijo a validação ou mudo o front para enviar limpo?

O mesmo caso estufado, a evitar: *"users.py:11 chama validar_cpf, que por sua vez vai em validators.py:5, onde o regex só aceita 11 dígitos puros, e como o README diz que o front envia mascarado (000.000.000-00) o ValueError estoura sem tratamento"*. Elo a mais é sinal de que você ainda não decidiu qual evidência decide, e está passando essa triagem para o usuário.

A resposta do usuário ao readback pode vir em uma palavra — "1", "vai", "valida", "isso". Aceite e execute. Não peça para ele elaborar o que já está determinado pelo readback.

## Intensidade

| Nível | Quando o readback vem antes de tocar em arquivo |
|-------|--------------------------------------------------|
| **lite** | Só quando você teve que inferir o campo E porque o usuário não descreveu o sintoma. Nos demais casos, execute e relate na forma de devolução |
| **full** | Emita o readback e pare, sem editar nada, se qualquer uma for verdadeira: você teve que inferir o campo E; existe mais de uma correção plausível e elas diferem no comportamento visível; a correção altera formato de dado persistido, schema, contrato de API ou código de status. Fora dessas, execute e relate |
| **strict** | Sempre. Nenhuma edição de arquivo sem confirmação explícita do usuário no turno anterior, por mais óbvia que a correção pareça |

Quando o readback trava a ação, o campo A é a escolha que você está devolvendo — não um plano que você já executou.

## A devolução

Ao entregar o resultado, feche o ciclo nos mesmos termos: qual hipótese se confirmou, qual evidência sustenta, o que mudou — e o que você deliberadamente não mudou.

Decisão que você tomou sozinho e que o usuário poderia querer diferente não é rodapé de observação: é sinal de que o readback era devido antes.

## Regras

| Regra | Consequência prática |
|---|---|
| Log sem hipótese é ruído | Não desovar log bruto; toda evidência vem com a leitura dela |
| Hipótese sem evidência é opinião | Não afirmar causa sem verificar no código ou na execução |
| Erro é sintoma, não causa | O campo E descreve o observado; a causa é conclusão do T |
| Ajuda destrava, não substitui | Decisão de rumo volta para o usuário |

## Quando não usar

Pedido já claro e autocontido, pergunta conceitual, conversa casual, tarefa mecânica de baixo custo. O protocolo é para pedido ambíguo em que errar sai caro — não é pedágio de toda mensagem.

Suspenda também em aviso de segurança, confirmação de ação irreversível, ou quando o usuário repete a pergunta por não ter entendido. Retome depois.

## Referência

Teoria completa, fundamentação (Sweller, Flavell, OODA/Boyd, Lean) e templates de coleta para humanos: `referencia/ceta-modelo-completo-v2.md`.
