"""Mede o protocolo CETA contra um baseline limpo, em ciclo completo.

Braço baseline: `claude -p` com o plugin desligado via --settings.
Braço skill: `claude -p` com o plugin ligado; se o primeiro turno devolver
uma pergunta sem editar nada, responde com RESPOSTA via --resume, que é o
custo real de chegar ao mesmo resultado.

Subagentes não servem de controle: herdam o protocolo da sessão que os cria.
"""
import argparse
import concurrent.futures as cf
import filecmp
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
PROMPT = "ta dando pau no cadastro, resolve ai"
RESPOSTA = "normaliza no backend e grava só os 11 dígitos"
FONTES = ["app/validators.py", "app/users.py", "test_users.py", "README.md"]
TOOLS = ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
DESLIGA = json.dumps({"enabledPlugins": {"ceta@ceta": False}})
CLAUDE = shutil.which("claude") or "claude"


def rodar_claude(cwd, prompt, modelo, desligar_plugin, resume=None):
    cmd = [CLAUDE, "-p", prompt, "--output-format", "json", "--model", modelo,
           "--allowedTools", *TOOLS]
    if desligar_plugin:
        cmd += ["--settings", DESLIGA]
    if resume:
        cmd += ["--resume", resume]
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=900)
    try:
        return json.loads(p.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return {"is_error": True, "result": p.stderr.decode("utf-8", "replace")[-300:]}


def testes_passam(cwd):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                       cwd=cwd, capture_output=True)
    return p.returncode == 0


def editados(fixture, cwd):
    return [f for f in FONTES if not filecmp.cmp(fixture / f, Path(cwd) / f, shallow=False)]


def formato(texto):
    return {
        "rotulos": bool(re.search(r"^\s*[CETA]:", texto, re.M)),
        "negritos": len(re.findall(r"\*\*[^*]+\*\*", texto)),
        "perguntas": texto.count("?"),
        "chars": len(texto),
    }


def um_run(braco, i, fixture, modelo):
    cwd = tempfile.mkdtemp(prefix=f"ceta-{braco}{i}-")
    shutil.copytree(fixture, cwd, dirs_exist_ok=True)
    turnos = []
    d = rodar_claude(cwd, PROMPT, modelo, desligar_plugin=(braco == "baseline"))
    turnos.append(d)
    ed1 = editados(fixture, cwd)
    primeira = d.get("result") or ""
    if braco == "skill" and not ed1 and primeira.rstrip().endswith("?") and not d.get("is_error"):
        turnos.append(rodar_claude(cwd, RESPOSTA, modelo, False, resume=d.get("session_id")))
    uso = lambda k: sum((t.get("usage") or {}).get(k, 0) for t in turnos)
    return {
        "braco": braco, "run": i,
        "erro": any(t.get("is_error") for t in turnos),
        "editou_sem_perguntar": bool(ed1),
        "turnos_usuario": len(turnos),
        "num_turns": sum(t.get("num_turns") or 0 for t in turnos),
        "output_tokens": uso("output_tokens"),
        "input_tokens": uso("input_tokens") + uso("cache_read_input_tokens") + uso("cache_creation_input_tokens"),
        "custo_usd": round(sum(t.get("total_cost_usd") or 0 for t in turnos), 4),
        "duracao_s": round(sum(t.get("duration_ms") or 0 for t in turnos) / 1000, 1),
        "testes_passam_no_fim": testes_passam(cwd),
        "formato_1o_turno": formato(primeira),
        "texto_1o_turno": primeira,
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
    a = ap.parse_args()

    fixture = AQUI / "fixtures" / a.fixture
    jobs = [(b, i) for b in ("baseline", "skill") for i in range(1, a.n + 1)]
    with cf.ThreadPoolExecutor(a.paralelo) as ex:
        res = list(ex.map(lambda j: um_run(j[0], j[1], fixture, a.modelo), jobs))

    saida = AQUI / "resultados"
    saida.mkdir(exist_ok=True)
    arq = saida / f"{time.strftime('%Y%m%d-%H%M%S')}-{a.fixture}.json"
    arq.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = {b: [r for r in res if r["braco"] == b and not r["erro"]] for b in ("baseline", "skill")}
    campos = ["output_tokens", "input_tokens", "custo_usd", "num_turns", "duracao_s"]
    print(f"{'':24}{'baseline':>12}{'skill':>12}{'economia':>11}")
    for k in campos:
        b, s = media(ok["baseline"], k), media(ok["skill"], k)
        eco = f"{(1 - s / b) * 100:.0f}%" if b else "-"
        print(f"{k:24}{b:>12.1f}{s:>12.1f}{eco:>11}")
    for b in ("baseline", "skill"):
        rs = ok[b]
        print(f"{b}: validos {len(rs)}/{a.n} | editou sem perguntar {sum(r['editou_sem_perguntar'] for r in rs)} "
              f"| testes passam no fim {sum(r['testes_passam_no_fim'] for r in rs)}")
    print(f"detalhes: {arq}")


if __name__ == "__main__":
    main()
