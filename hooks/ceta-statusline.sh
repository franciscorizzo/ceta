#!/usr/bin/env bash
# Statusline: diretorio | modelo | badge CETA. Recebe JSON por stdin.
ctx=$(cat)
esc=$'\033'; dim="${esc}[2m"; cyan="${esc}[36m"; amber="${esc}[38;5;172m"; off="${esc}[0m"
parts=()

dir=$(printf '%s' "$ctx" | sed -n 's/.*"current_dir"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -z "$dir" ] && dir=$(printf '%s' "$ctx" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -n "$dir" ] && parts+=("${cyan}$(basename "${dir//\//}")${off}")

model=$(printf '%s' "$ctx" | sed -n 's/.*"display_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -n "$model" ] && parts+=("${dim}${model}${off}")

claude_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
flag="$claude_dir/.ceta-active"
if [ -f "$flag" ] && [ ! -L "$flag" ] && [ "$(wc -c < "$flag")" -le 64 ]; then
  mode=$(head -c 64 "$flag" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9-')
  case "$mode" in
    full)         parts+=("${amber}[CETA]${off}") ;;
    lite|strict)  parts+=("${amber}[CETA:$(printf '%s' "$mode" | tr '[:lower:]' '[:upper:]')]${off}") ;;
  esac
fi

sep="${dim} | ${off}"; out=""
for p in "${parts[@]}"; do [ -n "$out" ] && out="$out$sep"; out="$out$p"; done
printf '%s' "$out"
