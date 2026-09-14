'use strict';
// Estado compartilhado do plugin CETA: leitura/escrita do nível ativo.

const fs = require('fs');
const path = require('path');
const os = require('os');

const VALID_MODES = ['lite', 'full', 'strict', 'off'];
const DEFAULT_MODE = 'full';
const MAX_FLAG_BYTES = 32;

function claudeDir() {
  return process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
}

function flagPath() {
  return path.join(claudeDir(), '.ceta-active');
}

// Recusa symlink para não ser usado como primitiva de escrita arbitrária.
function refuseSymlink(p) {
  try {
    if (fs.lstatSync(p).isSymbolicLink()) return true;
  } catch (e) { /* não existe: ok */ }
  return false;
}

function readFlag() {
  const p = flagPath();
  if (refuseSymlink(p)) return null;
  try {
    const raw = fs.readFileSync(p, 'utf8').slice(0, MAX_FLAG_BYTES).trim().toLowerCase();
    return VALID_MODES.includes(raw) ? raw : null;
  } catch (e) {
    return null;
  }
}

function writeFlag(mode) {
  if (!VALID_MODES.includes(mode)) return false;
  const p = flagPath();
  if (refuseSymlink(p)) return false;
  try {
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, mode, { encoding: 'utf8', mode: 0o600 });
    return true;
  } catch (e) {
    return false;
  }
}

function clearFlag() {
  try { fs.unlinkSync(flagPath()); } catch (e) {}
}

function getActiveMode() {
  return readFlag() || DEFAULT_MODE;
}

module.exports = { VALID_MODES, DEFAULT_MODE, flagPath, readFlag, writeFlag, clearFlag, getActiveMode };
