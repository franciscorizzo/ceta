# Embasamento científico

Nenhum estudo abaixo mede diretamente "carga cognitiva ao ler a resposta de uma IA" —
essa lacuna continua aberta, e é para isso que servem as medições em [`testes/`](../testes).
O que existe é evidência, revisada por pares, sobre os mecanismos que o CETA assume:
memória de trabalho limitada, efeito de sinalização, comunicação em loop fechado,
e o comportamento de pessoas e modelos diante de ambiguidade. A relação com cada
regra do protocolo é classificada como **direta** (o estudo testa o mesmo tipo de
efeito) ou **por analogia** (o domínio é diferente — aviação, saúde, aprendizagem
multimídia — e a transferência para chat com IA é inferência, não dado).

Pesquisa feita em 2026-09-14 por três buscas independentes, cada referência
confirmada por DOI, página da editora ou repositório oficial (Crossref, FAA/NTL,
ACM DL, arXiv, Europe PMC). Os itens que não passaram nessa barra ficam na lista
"Não verificado" no fim, junto com os achados que contradizem ou limitam o modelo.

## Carga cognitiva e sinalização

Sustentam: parágrafo curto, sem rótulo, com o essencial primeiro; negrito em um
trecho só; quatro campos como teto, não como meta.

- **Sweller, van Merriënboer & Paas (1998).** "Cognitive Architecture and
  Instructional Design". *Educational Psychology Review*, 10, 251–296.
  doi:10.1023/A:1022193728205 — memória de trabalho é limitada; material deve
  reduzir carga que não serve à tarefa. *Por analogia* (contexto instrucional).
- **Chandler & Sweller (1991).** "Cognitive Load Theory and the Format of
  Instruction". *Cognition and Instruction*, 8, 293–332.
  doi:10.1207/s1532690xci0804_2 — material "útil mas não essencial" prejudicou
  o aprendizado (efeito de redundância); fontes separadas que exigem integração
  mental geram carga extra. *Direto* quanto ao mecanismo, *por analogia* quanto
  ao meio.
- **Schneider, Beege, Nebel & Rey (2018).** "A meta-analysis of how signaling
  affects learning with media". *Educational Research Review*, 23, 1–24.
  doi:10.1016/j.edurev.2017.11.001 — 103 estudos, N=12.201: sinalização melhora
  retenção e transferência, reduz carga cognitiva. *Por analogia.*
- **Richter, Scheiter & Eitel (2016).** "Signaling text-picture relations in
  multimedia learning: a comprehensive meta-analysis". *Educational Research
  Review*, 17, 19–36. doi:10.1016/j.edurev.2015.12.003 — efeito pequeno a
  médio, maior em quem tem pouco conhecimento prévio. *Por analogia, com
  ressalva* (ver Kalyuga abaixo).
- **Joshi & Vogel (2024).** "Constrained Highlighting in a Document Reader can
  Improve Reading Comprehension". *CHI 2024*. doi:10.1145/3613904.3642314 —
  N=127: destaque limitado a ~150 palavras supera destaque livre ou ausente.
  *Por analogia* (o destaque era feito pelo leitor, não entregue pronto) —
  sustenta especificamente "negrito em exatamente um trecho".
- **Cowan (2001).** "The magical number 4 in short-term memory". *Behavioral
  and Brain Sciences*, 24, 87–114. doi:10.1017/S0140525X01003922 — o limite
  real é ~3–5 blocos de informação, não os "7±2" de Miller. *Por analogia* —
  sustenta o teto de quatro campos.
- **Shrestha, Lenz, Chaparro & Owens (2007).** "'F' Pattern Scanning of Text
  and Images in Web Pages". *Proc. HFES Annual Meeting*, 51, 1200–1204.
  doi:10.1177/154193120705101831 — eye tracking confirma leitura em varredura;
  o que vem cedo é lido com mais atenção. *Por analogia* — sustenta "o essencial
  na primeira frase".

**Contrário/limitação — Kalyuga (2007).** "Expertise Reversal Effect…".
*Educational Psychology Review*, 19, 509–539. doi:10.1007/s10648-007-9054-3 —
apoio que ajuda novato fica redundante, às vezes prejudicial, para quem já é
especialista. O usuário do CETA é especialista no próprio código: estrutura
demais pode virar carga, não reduzi-la. É o argumento a favor de manter o
readback curto, não de expandi-lo. Também é o argumento contra tratar todo
usuário como iniciante: `hooks/ceta-config.js:9` fixa `full` como nível
padrão, mas quem já se sabe especialista tem saída própria — `/ceta lite`
— em vez de precisar convencer a skill a confiar nele.

## Comunicação em loop fechado e formato fixo

Sustentam: readback como confirmação antes de agir; formato fixo (C→E→T→A)
como estrutura de passagem de informação.

- **Prinzo, Hendrix & Hendrix (2006).** "The Outcome of ATC Message Complexity
  on Pilot Readback Performance". FAA, DOT/FAA/AM-06/25. — em 50h de
  comunicação piloto-controlador, erros de readback e pedidos de repetição
  sobem com a complexidade e o número de tópicos por mensagem. *Direto* —
  sustenta o limite estrutural do T (três elos).
- **Morrow, Lee & Rodvold (1993).** "Analysis of Problems in Routine
  Controller-Pilot Communication". *Int. J. of Aviation Psychology*, 3(4),
  285–302. doi:10.1207/s15327108ijap0304_3 — readbacks incorretos ou parciais
  aparecem mais quanto maior e mais composta é a mensagem. *Por analogia.*
- **Cardosi, Falzarano & Han (1998).** "Pilot-controller communication
  errors: an analysis of ASRS reports". FAA, DOT/FAA/AR-98/17 — tipifica erro
  de readback, erro de *hearback* (quem recebe não confere) e ausência de
  readback. *Por analogia.*
- **Starmer et al., I-PASS Study Group (2014).** "Changes in medical errors
  after implementation of a handoff program". *NEJM*, 371, 1803–1812.
  doi:10.1056/NEJMsa1405556 — 9 hospitais: erros médicos −23%, eventos
  adversos evitáveis −30%, sem piorar o fluxo. O protocolo fecha com síntese
  de quem recebe — um readback. *Por analogia* (estudo antes/depois, não
  randomizado).
- **Müller et al. (2018).** "Impact of the communication and patient hand-off
  tool SBAR on patient safety: a systematic review". *BMJ Open*, 8, e022202.
  doi:10.1136/bmjopen-2018-022202 — evidência **moderada**: 8 de 26 desfechos
  melhoraram, mais forte na comunicação por telefone. SBAR é o parente mais
  próximo do CETA (Situação/Contexto, Background, Avaliação, Recomendação).
- **El-Shafy et al. (2018).** "Closed-Loop Communication Improves Task
  Completion in Pediatric Trauma Resuscitation". *J. Surg. Educ.*, 75, 58–64.
  doi:10.1016/j.jsurg.2017.06.025 — 89 vídeos, 387 ordens: ordens em loop
  fechado concluídas 3,6× mais rápido (HR 3,6; IC95% 2,5–5,3). Só 26% das
  ordens usaram o loop. *Por analogia* — confirmar antes de agir não atrasa.
- **Diaz & Dawson (2020).** "Impact of Simulation-Based Closed-Loop
  Communication Training on Medical Errors in a Pediatric ED". *Am. J. Med.
  Qual.*, 35, 474–478. doi:10.1177/1062860620912480 — erros caem de 19 para 5
  por período (razão 3,8; p=0,008). Amostra pequena (n=9+9).

**Contrário — Monan (1988).** "Human factors in aviation operations: the
hearback problem". NASA-CR-177398, 417 relatos ASRS. O controlador não
contestar um readback não garante que ele esteja correto: o readback não
protege se quem ouve não confere. No CETA, equivale a responder "1" sem ler
o parágrafo. Pedir confirmação de novo antes de agir reabriria a
interrupção que o design já decidiu evitar (`SKILL.md`, seção "O
readback"), então o fechamento fica para depois de agir, não antes: "A
devolução" relata o que mudou nos mesmos termos da escolha, o mesmo
padrão de síntese do receptor que o I-PASS usa. Não corrige o risco de o
usuário não ler a devolução — isso não tem correção de protocolo.

## Interação humano-IA e ambiguidade

Sustentam: perguntar antes de agir quando a instrução é ambígua; usar gatilho
observável em vez de o modelo julgar sozinho se "está claro"; devolver a
decisão ao usuário em vez de decidir por ele.

- **Horvitz (1999).** "Principles of Mixed-Initiative User Interfaces". *CHI
  '99*. doi:10.1145/302979.303030 — projeto para o sistema decidir, sob
  incerteza, quando abrir diálogo com o usuário e quando agir sozinho.
  *Direto*, como princípio de projeto (não é um experimento com métrica).
- **Horvitz & Apacible (2003).** "Learning and Reasoning about Interruption".
  *ICMI 2003* — modelos que estimam o custo esperado de interromper para
  decidir entre avisar agora ou adiar. *Direto* — é o cálculo por trás do gate.
- **Vijayvargiya, Zhou, Yerukola, Sap & Neubig (2025).** "Ambig-SWE". arXiv
  2502.13069 (preprint, aceito ICLR 2026) — agentes de engenharia de software
  distinguem mal instrução ambígua de bem especificada; interagir com o
  usuário melhora o desempenho em até 74%. *Direto.*
- **Mu et al. (2024).** "ClarifyGPT: A Framework for Enhancing LLM-based Code
  Generation via Requirements Clarification". *FSE 2024* — detectar
  ambiguidade e perguntar antes de gerar código elevou o Pass@1 do GPT-4 de
  62,43% para 69,60% (média de 5 benchmarks). *Direto.*
- **Zhang et al. (2024).** "CLAMBER". *ACL 2024*.
  doi:10.18653/v1/2024.acl-long.578 — LLMs têm utilidade prática limitada em
  identificar e esclarecer ambiguidade sozinhos, mesmo com CoT/few-shot; o
  prompting pode aumentar o excesso de confiança. *Direto* — é o motivo de o
  gate usar predicados observáveis ("teve que inferir E", "mais de uma
  correção plausível") em vez de pedir ao modelo para julgar "está claro?".
- **Aliannejadi, Zamani, Crestani & Croft (2019).** "Asking Clarifying
  Questions in Open-Domain Information-Seeking Conversations". *SIGIR '19*.
  doi:10.1145/3331184.3331265 — uma boa pergunta de esclarecimento mais que
  dobra a recuperação. *Por analogia* (domínio é busca, não código).
- **Parasuraman & Manzey (2010).** "Complacency and Bias in Human Use of
  Automation". *Human Factors*, 52(3), 381–410. doi:10.1177/0018720810376055
  — complacência e viés de automação afetam novatos e especialistas por
  igual, produzem erros de omissão e comissão, não somem com treino. *Por
  analogia* — o usuário não detecta bem o erro escondido num diff.
- **Perry, Srivastava, Kumar & Boneh (2023).** "Do Users Write More Insecure
  Code with AI Assistants?". *CCS '23*. doi:10.1145/3576915.3623157 — quem
  usou assistente de IA escreveu código menos seguro e confiava mais que o
  código era seguro. *Direto* — é o risco que o gate existe para evitar.
- **Mozannar, Bansal, Fourney & Horvitz (2024).** "Reading Between the
  Lines". *CHI 2024*. doi:10.1145/3613904.3641936 — estudo com 21
  programadores usando Copilot: verificar sugestões tem custo de tempo
  mensurável. *Direto* quanto ao mecanismo (revisar saída de IA custa), sem
  percentual confirmado na fonte.

**Contrário — Mark, Gudith & Klocke (2008).** "The Cost of Interrupted Work:
More Speed and Stress". *CHI 2008*, 107–110. doi:10.1145/1357054.1357072 —
tarefa interrompida termina mais rápido e sem perda de qualidade, mas com
mais estresse, frustração e pressão de tempo. É o contraponto direto: a
pergunta extra do CETA tem custo humano real, mesmo quando não piora o
resultado. Sustenta não perguntar quando o default já acerta sozinho — ver
a fixture `cpf` em [`testes/`](../testes).

## Contraponto histórico

- **Miller (1956).** "The Magical Number Seven, Plus or Minus Two".
  *Psychological Review*, 63, 81–97. doi:10.1037/h0043158 — a estimativa
  clássica de capacidade da memória de curto prazo, revista por Cowan (2001)
  acima.

## Não verificado

Apareceram em buscas ou resumos secundários, mas não foram confirmados numa
fonte primária (DOI, página da editora, ou o texto completo do artigo):

- Tamanhos de efeito exatos (Cohen's *g*) de Schneider et al. (2018) — só
  vistos como "forte/moderado" numa fonte secundária.
- "Quanto mais destaque, pior o desempenho" (citado como Fowler & Barker,
  1974) — aparece só em reportagens, sem o artigo original.
- Alpizar et al. (2020) e Xie et al. (2017), citados por fonte secundária.
- Nielsen (2006), o estudo original do padrão de leitura em "F" — é relatório
  de consultoria (Nielsen Norman Group), não revisado por pares.
- Tamanho de amostra exato de Perry et al. (2023).
- Percentuais de tempo relatados em Mozannar et al. (2024) — a página aberta
  trazia só o resumo.
- Formulação explícita de "utilidade esperada" no texto completo de Horvitz
  (1999) — a página acessada trazia só o resumo.

## O que a literatura não cobre

Nenhuma das referências acima testa diretamente carga cognitiva na leitura
de uma resposta de IA, nem compara ler um readback de parágrafo com revisar
um diff de código. Essa é a lacuna que as medições em
[`testes/medir.py`](../testes/medir.py) tentam preencher com indicadores
indiretos — tokens, turnos, edição sem confirmação, retrabalho — não com
carga cognitiva medida em pessoas.
