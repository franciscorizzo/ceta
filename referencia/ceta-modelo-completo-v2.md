# CETA — Modelo Cognitivo-Operacional para Estruturação de Demandas de Suporte

> Extraído de `CETA_Modelo_Completo_v2.md`, fonte do notebook "The CETA Protocol:
> Structuring Support and Decision Logic" (Gemini Notebook / NotebookLM).

## 1. Origem do Modelo

O modelo CETA surgiu da necessidade prática de reduzir sobrecarga cognitiva em ambientes de alta complexidade, onde liderança técnica, produto e suporte coexistem. O problema central não era falta de capacidade técnica, mas **pedidos de ajuda mal formulados**, que consumiam energia de decisão e geravam dependência.

A construção do CETA foi iterativa, baseada em observação prática, refinamento conceitual e validação no cotidiano de times técnicos.

## 2. Definição do CETA

CETA é um acrônimo que representa quatro elementos obrigatórios para qualquer pedido de ajuda eficaz:

- C — Contexto
- E — Erro (ou Trava)
- T — Tentou / Testou
- A — Ajuda

O objetivo do CETA não é burocratizar o suporte, mas **estruturar o pensamento antes da interação**.

Em inglês (não oficial): **CETH** — Context, Error, Tried/Tested, Help.

## 3. Descrição dos Elementos

### 3.1 Contexto
Define o domínio do problema. Em qual fluxo, sistema, tarefa ou cenário o problema ocorre?
Sem contexto, toda decisão vira suposição.

### 3.2 Erro (ou Trava)
Define o ponto de falha observável. O que aconteceu de diferente do esperado? Onde não avançou?
Erro não é causa, é **sintoma observável**.

### 3.3 Tentou / Testou (Definição Formal)

Tentou/Testou **não significa apenas executar uma ação**, nem "mexer" no sistema ou adicionar logs de forma isolada.

```
Tentativa = Hipótese explícita + Teste realizado + Interpretação do resultado
```

Uma tentativa válida exige **raciocínio aplicado**, não apenas instrumentação.

#### 3.3.1 Hipótese
Explicita o que a pessoa acredita que pode estar causando o problema. Exemplos válidos:
- "Acreditei que o payload estivesse vindo vazio."
- "Pensei que fosse um problema de permissão."
- "Considerei que o erro estivesse na validação do campo."

Sem hipótese, não há tentativa — há apenas observação passiva.

#### 3.3.2 Teste
Ação mínima executada para validar ou refutar a hipótese: execução de fluxos alternativos, testes com dados controlados, simulações, instrumentação com `log.debug`.
O teste é um meio, não um fim.

#### 3.3.3 Interpretação
Conecta o teste à hipótese inicial. Exemplos:
- "O log mostrou que o payload chega corretamente, então descartei essa hipótese."
- "O comportamento confirmou que a validação falha antes de salvar."

Sem interpretação, o teste não produz aprendizado.

#### 3.3.4 O papel do `log.debug`
Não é uma tentativa por si só. É evidência empírica, instrumento de observação e suporte ao raciocínio.

> Log sem hipótese é ruído.
> Hipótese sem evidência é opinião.
> Tentativa é a união dos dois.

#### 3.3.5 Regra de Uso
Quando perguntado "o que você tentou?", a resposta esperada é:

> "Achei que o problema fosse X, então testei Y e observei Z."

Essa estrutura é o núcleo do aprendizado e da autonomia promovidos pelo modelo.

### 3.4 Ajuda
A solicitação exata necessária para destravar: validação, sugestão de contorno ou orientação.
O suporte existe para destravar o raciocínio, não para executar a tarefa no lugar do solicitante.

## 4. Fundamentação Teórica

| Base | Aplicação no CETA |
|---|---|
| Problem Framing | Um problema bem formulado está, em grande parte, resolvido. CETA é o framework mínimo de enquadramento. |
| Carga Cognitiva (Sweller) | A memória de trabalho suporta poucos elementos simultâneos. CETA reduz narrativas difusas a 4 dimensões acionáveis. |
| Metacognição (Flavell) | Exigir explicitação do que foi testado força reflexão, aprendizado ativo e autonomia. |
| OODA Loop (Boyd) | Observe → Contexto + Erro; Orient → Tentou/Testou; Decide → Ajuda; Act → Ação. |
| Lean Thinking | Pedidos mal formulados geram desperdício: retrabalho, espera, dependência. |
| Engenharia de Software | "No logs, no bugs" — sem evidência, não há diagnóstico. |

## 5. Funcionamento Prático

O CETA não é checklist rígido, é **linguagem compartilhada**. É a "menor estrutura possível que ainda funciona".

Exemplo de pedido adequado:

```
Contexto: Fluxo de cadastro X
Erro: Retorno Y ao salvar
Testou: Ajuste Z + log.debug do payload
Ajuda: Preciso validar se o caminho é esse
```

## 6. Regras Operacionais

- Suporte não é para resolver tudo, é para **destravar**.
- Pedido sem CETA pode ser devolvido.
- Liderança não debuga no lugar, ensina a debugar.

Mantras:
- "Sem testar, não existe ajuda."
- "Sem log, é opinião."
- "Ajuda sem estrutura cria dependência; estrutura cria autonomia."

## 7. Benefícios Organizacionais

- Redução de interrupções improdutivas
- Aumento de autonomia
- Decisões mais rápidas
- Escalabilidade humana
- Proteção da energia cognitiva da liderança

## 8. Analogia: Frasologia Aeronáutica

A frasologia da aviação foi desenvolvida pelo mesmo motivo do CETA: eliminar ambiguidades e reduzir sobrecarga cognitiva em momentos de alta complexidade. O OODA Loop, criado pelo piloto militar John Boyd, é uma das bases teóricas do CETA.

| Frasologia Aeronáutica | Pilar CETA | Função no Protocolo |
|---|---|---|
| Identificação & Posição | Contexto | Situa o sistema, fluxo ou ambiente sem gerar suposições |
| Anomalia / Condição | Erro (Sintoma) | Aponta a falha observável de forma objetiva |
| Ações Tomadas / Checagens | Tentou / Testou | Transmite hipótese, teste realizado e evidências/logs |
| Intenção / Solicitação ao ATC | Ajuda | Define a solicitação exata necessária para destravar |

Formato ultra-conciso (Slack/WhatsApp):

```
[CONTEXTO] Checkout / API de Pagamento
[SINTOMA]  ...
[AÇÕES]    ...
[SOLICITO] ...
```

## 9. Templates de Coleta (uso com humanos)

**Opção 1 — Direta e visual:**
```
Pra eu conseguir te ajudar mais rápido, preenche rapidinho o CETA:

*C — Contexto*
🏢 Qual empresa/sistema?
⚙️ Qual operação/fluxo estava fazendo?

*E — Erro*
❌ Qual o comportamento inesperado ou trava? (Sintoma observável)

*T — Tentou / Testou*
🧪 O que você já testou diferente?
📝 Tem log ou hipótese do que pode ser?

*A — Ajuda*
🤝 O que precisa agora? (Validação, como contornar, desbloqueio?)
```

**Opção 2 — Curta:**
```
Manda no padrão CETA pra gente ganhar tempo:
- (C)ontexto: Empresa e Operação
- (E)rro: O que travou?
- (T)entou: O que já validou/logou?
- (A)juda: O que precisa de mim?
```

## 10. Narrativa por Público

- **Diretoria** (eficiência e escala): resolve o custo oculto de pedidos mal formulados que drenam a energia da liderança. Escalabilidade humana, proteção de ativos, velocidade (OODA).
- **Scrum Masters** (fluxo e autonomia): linguagem compartilhada, não checklist burocrático. Elimina o "vai-e-vem" (Lean), força reflexão antes do pedido (Metacognição), suporte focado em destravar.
- **Devs** (prática e clareza): protocolo de debug contra "perguntas preguiçosas". "Sem tentativa, não existe ajuda", "Sem log, é opinião", "No logs, no bugs".
