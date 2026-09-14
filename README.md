# CETA

Plugin do Claude Code que aplica o **protocolo CETA** — Contexto, Erro, Tentou/Testou, Ajuda — à conversa entre você e a IA.

## A inversão

No modelo original, quem pede ajuda preenche os quatro campos. Aqui é o contrário: **o Claude preenche**. Você fala solto, inclusive em duas palavras; ele investiga o repositório, monta os quatro campos e devolve um *readback* de quatro linhas antes de agir.

Jogar um formulário na tela do usuário aumentaria justamente a carga cognitiva que o protocolo existe para reduzir.

```
você:  nao salva

       C: cadastro de clientes, POST /api/users
       E: não salva; users.py:11 estoura ValueError sem catch → 500, esperado 201
       T: supus máscara → validators.py:5 exige \d{11} → rejeita, ValueError sem catch
       A: corrijo a validação para aceitar máscara ou mudo o front pra enviar limpo?

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
