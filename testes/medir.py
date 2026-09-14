"""Mede o protocolo CETA contra um baseline limpo, em ciclo completo.

Cada run conversa até o aceite oculto (testes/aceite/<fixture>) passar, com
no máximo MAX_TURNOS mensagens do usuário. Turno sem edição terminado em
pergunta recebe `resposta`; qualquer outro turno que não passou recebe
`correcao` e conta como retrabalho. Os dois textos ficam em cenario.json.

Braço baseline: plugin desligado via --settings. Subagentes não servem de
controle: herdam o protocolo da sessão que os cria.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MAX_TURNOS = 3
TOOLS = ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
DESLIGA = json.dumps({"enabledPlugins": {"ceta@ceta": False}})
CLAUDE = shutil.which("claude") or "claude"
IGNORAR = {"__pycache__", ".pytest_cache", "cenario.json"}
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def rodar_claude(cwd, prompt, modelo, desligar_plugin, resume=None, plugin_dir=None):
    cmd = [CLAUDE, "-p", prompt, "--output-format", "json", "--model", modelo,
           "--allowedTools", *TOOLS]
    if desligar_plugin or plugin_dir:
        cmd += ["--settings", DESLIGA]
    if plugin_dir:
        cmd += ["--plugin-dir", str(plugin_dir)]
    if resume:
        cmd += ["--resume", resume]
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=900)
    try:
        return json.loads(p.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return {"is_error": True, "result": p.stderr.decode("utf-8", "replace")[-300:]}


def snapshot(raiz):
    raiz = Path(raiz)
    return {str(f.relative_to(raiz)): f.read_bytes() for f in raiz.rglob("*")
            if f.is_file() and not IGNORAR & set(f.relative_to(raiz).parts)}


def pytest_ok(cwd, alvo=None):
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + ([str(alvo)] if alvo else [])
    return subprocess.run(cmd, cwd=cwd, capture_output=True, env=ENV).returncode == 0


def aceito(cwd, aceite):
    return pytest_ok(cwd) and pytest_ok(cwd, aceite)


def formato(texto):
    return {
        "rotulos": bool(re.search(r"^\s*[CETA]:", texto, re.M)),
        "negritos": len(re.findall(r"\*\*[^*]+\*\*", texto)),
        "perguntas": texto.count("?"),
        "chars": len(texto),
    }


def um_run(braco, i, fixture, cen, aceite, modelo, plugin_dir=None):
    cwd = tempfile.mkdtemp(prefix=f"ceta-{fixture.name}-{braco}{i}-")
    shutil.copytree(fixture, cwd, dirs_exist_ok=True, ignore=shutil.ignore_patterns(*IGNORAR))
    turnos, msg, sid, correcoes, editou_1o = [], cen["prompt"], None, 0, False
    for n in range(MAX_TURNOS):
        antes = snapshot(cwd)
        d = rodar_claude(cwd, msg, modelo, braco == "baseline", resume=sid,
                         plugin_dir=plugin_dir if braco == "skill" else None)
        turnos.append(d)
        sid = d.get("session_id") or sid
        editou = snapshot(cwd) != antes
        if n == 0:
            editou_1o = editou
        if d.get("is_error") or aceito(cwd, aceite):
            break
        if not editou and (d.get("result") or "").rstrip().endswith("?"):
            msg = cen["resposta"]
        else:
            msg = cen["correcao"]
            correcoes += 1
    uso = lambda k: sum((t.get("usage") or {}).get(k, 0) for t in turnos)
    primeira = turnos[0].get("result") or ""
    return {
        "braco": braco, "run": i,
        "erro": any(t.get("is_error") for t in turnos),
        "editou_no_1o_turno": editou_1o,
        "mensagens_usuario": len(turnos),
        "correcoes": correcoes,
        "aceito_no_fim": aceito(cwd, aceite),
        "num_turns": sum(t.get("num_turns") or 0 for t in turnos),
        "output_tokens": uso("output_tokens"),
        "input_tokens": uso("input_tokens") + uso("cache_read_input_tokens") + uso("cache_creation_input_tokens"),
        "custo_usd": round(sum(t.get("total_cost_usd") or 0 for t in turnos), 4),
        "duracao_s": round(sum(t.get("duration_ms") or 0 for t in turnos) / 1000, 1),
        "formato_1o_turno": formato(primeira),
        "textos": [t.get("result") or "" for t in turnos],
    }


def media(rs, k):
    v = [r[k] for r in rs]
    return statistics.mean(v) if v else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("--modelo", default="opus")
    ap.add_argument("--fixture", default="cpf")
    ap.add_argument("--paralelo", type=int, default=5)
    ap.add_argument("--bracos", default="baseline,skill")
    ap.add_argument("--plugin-dir", help="variante da skill; desliga o plugin instalado no braço skill")
    ap.add_argument("--rotulo", default="")
    a = ap.parse_args()

    fixture = AQUI / "fixtures" / a.fixture
    aceite = AQUI / "aceite" / a.fixture
    cen = json.loads((fixture / "cenario.json").read_text(encoding="utf-8"))
    jobs = [(b, i) for b in a.bracos.split(",") for i in range(1, a.n + 1)]
    with cf.ThreadPoolExecutor(a.paralelo) as ex:
        res = list(ex.map(lambda j: um_run(j[0], j[1], fixture, cen, aceite, a.modelo, a.plugin_dir), jobs))

    saida = AQUI / "resultados"
    saida.mkdir(exist_ok=True)
    arq = saida / f"{time.strftime('%Y%m%d-%H%M%S')}-{a.fixture}{'-' + a.rotulo if a.rotulo else ''}.json"
    arq.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = {b: [r for r in res if r["braco"] == b and not r["erro"]] for b in ("baseline", "skill")}
    campos = ["output_tokens", "input_tokens", "custo_usd", "num_turns", "duracao_s", "mensagens_usuario", "correcoes"]
    print(f"{'':20}{'baseline':>12}{'skill':>12}{'economia':>11}")
    for k in campos:
        b, s = media(ok["baseline"], k), media(ok["skill"], k)
        eco = f"{(1 - s / b) * 100:.0f}%" if b else "-"
        print(f"{k:20}{b:>12.2f}{s:>12.2f}{eco:>11}")
    for b in ("baseline", "skill"):
        rs = ok[b]
        print(f"{b}: validos {len(rs)}/{a.n} | editou no 1o turno {sum(r['editou_no_1o_turno'] for r in rs)} "
              f"| precisou correcao {sum(r['correcoes'] > 0 for r in rs)} | aceito no fim {sum(r['aceito_no_fim'] for r in rs)}")
    print(f"detalhes: {arq}")


if __name__ == "__main__":
    main()
