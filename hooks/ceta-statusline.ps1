# Statusline: diretorio | modelo | badge CETA.
# Recebe o JSON de contexto do Claude Code por stdin.
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ctx = $null
try { $ctx = [Console]::In.ReadToEnd() | ConvertFrom-Json } catch {}

$esc = [char]27
$dim = "$esc[2m"; $cyan = "$esc[36m"; $amber = "$esc[38;5;172m"; $off = "$esc[0m"
$parts = @()

# Diretorio de trabalho (so o nome da pasta)
$dir = $null
if ($ctx -and $ctx.workspace -and $ctx.workspace.current_dir) { $dir = $ctx.workspace.current_dir }
elseif ($ctx -and $ctx.cwd) { $dir = $ctx.cwd }
if ($dir) { $parts += "$cyan" + (Split-Path $dir -Leaf) + $off }

# Modelo
if ($ctx -and $ctx.model -and $ctx.model.display_name) {
  $parts += "$dim" + $ctx.model.display_name + $off
}

# Badge CETA — le a flag com as mesmas defesas do caveman:
# recusa reparse point, limita tamanho, remove tudo fora de [a-z0-9-] e valida
# contra whitelist. Sem isso o conteudo do arquivo poderia injetar escapes ANSI
# no terminal a cada tecla.
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$flag = Join-Path $claudeDir '.ceta-active'
if (Test-Path $flag) {
  try {
    $item = Get-Item -LiteralPath $flag -Force -ErrorAction Stop
    if (-not ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -and $item.Length -le 64) {
      $raw = Get-Content -LiteralPath $flag -TotalCount 1 -ErrorAction Stop
      $mode = ([string]$raw).Trim().ToLowerInvariant() -replace '[^a-z0-9-]', ''
      if (@('lite','full','strict') -contains $mode) {
        $label = if ($mode -eq 'full') { '[CETA]' } else { "[CETA:$($mode.ToUpperInvariant())]" }
        $parts += "$amber$label$off"
      }
    }
  } catch {}
}

[Console]::Write(($parts -join "$dim | $off"))
