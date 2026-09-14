# CETA

Plugin do Claude Code que aplica o **protocolo CETA** — Contexto, Erro, Tentou/Testou, Ajuda — à conversa entre você e a IA.

## A inversão

No modelo original, quem pede ajuda preenche os quatro campos. Aqui é o contrário: **o Claude preenche**. Você fala solto, inclusive em duas palavras; ele investiga o repositório, monta os quatro campos e devolve um *readback* — um parágrafo curto, com o achado que decide em negrito e uma pergunta só — antes de agir.

Jogar um formulário na tela do usuário aumentaria justamente a carga cognitiva que o protocolo existe para reduzir.

```
você:  nao salva

       No cadastro, `POST /api/users` devolve `500` em vez de `201`. Supus
       payload vazio, mas ele chega íntegro — **o regex `^\d{11}$` em
       `app/validators.py:3` rejeita a máscara que o formulário envia**.

       Normalizo no backend e gravo só os dígitos, ou aceito a máscara?

você:  1
```

Três palavras suas. O trabalho de estruturar é da máquina.

A analogia é a frasologia aeronáutica: o piloto não preenche formulário — transmite o essencial, e o controlador faz o readback para confirmar antes de agir.

## Instalação

```bash
claude plugin marketplace add franciscorizzo/ceta
claude plugin install ceta@ceta --scope user
```

Reinicie a sessão para o hook `SessionStart` disparar.

## Níveis

Troque com `/ceta lite|full|strict|off`, ou em linguagem natural ("para ceta", "liga ceta").

| Nível | Quando o readback vem antes de tocar em arquivo |
|---|---|
| `lite` | Só quando o sintoma teve de ser inferido |
| `full` (padrão) | Sintoma inferido, mais de uma correção plausível, ou mudança de schema/contrato/status |
| `strict` | Sempre — nenhuma edição sem confirmação explícita |
| `off` | Desligado |

## Statusline (opcional)

Mostra `pasta | modelo | [CETA]`, com o badge acompanhando o nível ativo:

```json
"statusLine": {
  "type": "command",
  "command": "powershell -NonInteractive -ExecutionPolicy Bypass -File \"<caminho>/hooks/ceta-statusline.ps1\""
}
```

Em Linux/macOS use `bash "<caminho>/hooks/ceta-statusline.sh"`.

## Como funciona

O hook `SessionStart` lê `skills/ceta/SKILL.md` em tempo de execução e injeta o protocolo como contexto, filtrando a tabela de intensidade para o nível ativo — então o comportamento não depende de o modelo decidir invocar uma skill. O hook `UserPromptSubmit` trata a troca de nível. O estado fica em `$CLAUDE_CONFIG_DIR/.ceta-active`, por profile.

Custo: ~91 tokens sempre presentes por sessão.

## Estrutura

```
.claude-plugin/     manifesto do plugin e do marketplace
hooks/              ativação, troca de nível, statusline
skills/ceta/        SKILL.md — única fonte de verdade do protocolo
commands/           /ceta
referencia/         teoria completa do modelo
```

Editar o protocolo significa editar `skills/ceta/SKILL.md`; o hook lê esse arquivo em runtime, sem duplicação.

## Medições

`testes/medir.py` roda o mesmo pedido ambíguo duas vezes — com o plugin
desligado (`baseline`) e ligado (`skill`) — até um teste de aceite oculto
passar, e mede tokens, custo e quantas vezes o agente editou ou precisou de
correção. Duas fixtures, 5 execuções cada, 2026-09-14:

| Fixture | O que testa | Correção óbvia | Custo | Editou/decidiu sem perguntar |
|---|---|---|---|---|
| `cpf` | default acerta a decisão | é a certa | igual (~US$ 0,30 nos dois) | baseline 5/5, skill 0/5 |
| `frete` | default erra a decisão | é a errada | skill 20% mais barato | baseline 4/5 editou errado, skill 0/5 |

Quando o default acerta, a skill não economiza — troca por uma mensagem sua
a mais. Quando o default erra, a skill custa menos, porque o baseline gasta
tokens corrigindo o próprio erro depois que você percebe.

Um par real da fixture `frete` (bug: `subtotal > 200` deveria ser `>= 200`,
mas o texto promocional diz "acima de 200" — a correção óbvia está errada):

<table>
<tr><th>sem skill</th><th>com skill</th></tr>
<tr><td valign="top">

Aplicou a correção (`>` → `>=`), rodou os testes, e só depois percebeu a
contradição com o banner promocional — 1101 caracteres, 5 negritos, e a
pergunta vem depois de já ter editado o código:

> Arrumei o frete grátis... **Correção:** troquei `>` por `>=`, só isso...
> **Antes de publicar, uma decisão:** `docs/promocoes.md` diz "acima de"...
> Segui o teste... Qual das duas regras vale?

</td><td valign="top">

Não editou nada — 513 caracteres, 1 negrito, a mesma contradição no
parágrafo, antes de mexer no código:

> No checkout, um pedido de exatamente `200.00` ainda paga frete... **o
> código segue o texto da promoção, e quem pede "a partir de 200" é o
> teste**. Não alterei nada ainda.
>
> A regra certa é "a partir de 200" (mudo o código) ou "acima de 200"
> (corrijo o teste)?

</td></tr>
</table>

Isso não prova redução de carga cognitiva — não há medição direta de carga
em pessoas aqui, só indicadores (tokens, edição sem confirmação,
retrabalho). O embasamento teórico, com o que a literatura sustenta e o que
não cobre, está em
[`referencia/embasamento-cientifico.md`](referencia/embasamento-cientifico.md).
Para reproduzir: `python testes/medir.py --fixture frete -n 5`.

## Crédito

O modelo CETA é de Francisco Rizzo. O mecanismo de plugin é inspirado no [caveman](https://github.com/JuliusBrussee/caveman), de Julius Brussee.

## Licença

[MIT](LICENSE).
