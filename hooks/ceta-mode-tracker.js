#!/usr/bin/env node
'use strict';
// UserPromptSubmit: detecta troca de nível ou desligamento em linguagem natural.

const { VALID_MODES, writeFlag, getActiveMode } = require('./ceta-config');

let raw = '';
process.stdin.on('data', (c) => { raw += c; });
process.stdin.on('end', () => {
  let prompt = '';
  try {
    prompt = (JSON.parse(raw).prompt || '').toString();
  } catch (e) {
    prompt = raw;
  }

  const slash = prompt.match(/\/ceta\s+(\w+)/i);
  const wanted = slash && slash[1].toLowerCase();

  if (wanted && VALID_MODES.includes(wanted)) {
    writeFlag(wanted);
    process.stdout.write(wanted === 'off' ? 'CETA desligado.' : 'CETA agora em nível: ' + wanted);
    return;
  }

  if (/\b(para|parar|desliga|desligar|encerra)\s+(o\s+)?ceta\b/i.test(prompt) ||
      /\bceta\s+(off|desligado)\b/i.test(prompt) ||
      /\bmodo\s+normal\b/i.test(prompt)) {
    writeFlag('off');
    process.stdout.write('CETA desligado.');
    return;
  }

  if (/\b(liga|ligar|ativa|ativar|volta)\s+(o\s+)?ceta\b/i.test(prompt) ||
      /\bceta\s+(on|ligado)\b/i.test(prompt)) {
    writeFlag('full');
    process.stdout.write('CETA ativo — nível: full');
    return;
  }

  const mode = getActiveMode();
  process.stdout.write(mode === 'off' ? '' : 'CETA ativo — nível: ' + mode);
});
