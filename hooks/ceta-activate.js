#!/usr/bin/env node
'use strict';
// SessionStart: injeta o protocolo CETA como contexto oculto, filtrado pelo nível ativo.
// Lê o SKILL.md em runtime — ele é a única fonte de verdade.

const fs = require('fs');
const path = require('path');
const { getActiveMode, writeFlag, clearFlag } = require('./ceta-config');

const mode = getActiveMode();

if (mode === 'off') {
  clearFlag();
  process.stdout.write('OK');
  process.exit(0);
}

writeFlag(mode);

let skill = '';
try {
  skill = fs.readFileSync(path.join(__dirname, '..', 'skills', 'ceta', 'SKILL.md'), 'utf8');
} catch (e) { /* usa fallback abaixo */ }

let output;

if (skill) {
  const body = skill.replace(/^---[\s\S]*?---\s*/, '');
  // Mantém apenas a linha da tabela de intensidade correspondente ao nível ativo.
  const filtered = body.split('\n').filter((line) => {
    const row = line.match(/^\|\s*\*\*(\S+?)\*\*\s*\|/);
    return !row || row[1] === mode;
  });
  output = 'CETA ATIVO — nível: ' + mode + '\n\n' + filtered.join('\n');
} else {
  output =
    'CETA ATIVO — nível: ' + mode + '\n\n' +
    'Você preenche Contexto, Erro, Tentou/Testou e Ajuda a partir do que o usuário disse e do que você investigar. ' +
    'O usuário nunca preenche formulário.\n\n' +
    'ATIVO EM TODA RESPOSTA. Não reverte depois de muitos turnos. Continua ativo na dúvida. ' +
    'Desliga só com "para ceta" ou "ceta off".';
}

process.stdout.write(output);
