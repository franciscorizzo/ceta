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

## Crédito

O modelo CETA é de Francisco Rizzo. O mecanismo de plugin é inspirado no [caveman](https://github.com/JuliusBrussee/caveman), de Julius Brussee.
