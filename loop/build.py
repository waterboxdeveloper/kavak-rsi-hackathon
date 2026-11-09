"""PASO 3 del loop: CONSTRUIR EL SUCESOR (con Codex).

Aqui Codex no es nuestro copiloto: es el organo de construccion del sistema.
Este script arma el prompt con (codigo del predecesor + lecciones activas +
tests rojos) e invoca `codex exec` para que escriba la version siguiente.

  python3 loop/build.py --from v0 --to v1
  python3 loop/build.py --from v1 --to v2 --print-prompt   # solo imprime

Si `codex` no esta instalado, guarda el prompt en runs/ para pegarlo a mano.
Eso tambien cuenta, pero hay que decirlo en la demo: "aqui hubo intervencion
humana" (la rubrica pide distinguirlo).
"""

import argparse
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CONTRATO = """CONTRATO (obligatorio):
- Archivo a escribir: agents/{to}/agent.py
- Debe exponer: VERSION = "{to}"  y  ingest(cases, store, engine, lessons) -> list[record]
- record = {{case_id, make, model, year, odometer_km, price_mxn, vin, flags, action}}
  action in: "created" | "merged_duplicate" | "rejected" | "failed"
- Las herramientas nuevas van en agents/common/tools/<tema>.py y se importan.
- CADA comportamiento aprendido debe ir envuelto en `if "Lx" in lessons:`
  usando el id exacto de la leccion. Esto NO es opcional: es lo que permite
  apagar una leccion y ver reaparecer la falla (ablation).
- NO modifiques bench/, lessons/, tests/ ni agents/v0/. Son la vara de medir.
- Solo stdlib de Python. Sin dependencias nuevas.
"""


def read_lessons():
    path = ROOT / "lessons" / "lessons.jsonl"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.open() if l.strip()]


def build_prompt(src, dst):
    lessons = [l for l in read_lessons() if l.get("enabled", True)]
    pred = (ROOT / "agents" / src / "agent.py").read_text()

    bloques = []
    for l in lessons:
        bloques.append(
            f"### {l['id']}  (defecto: {l['defect']})\n"
            f"- disparador: {l['trigger']}\n"
            f"- evidencia : casos {l.get('evidence_cases') or '-'} en {l['evidence_run']}\n"
            f"- REGLA     : {l['rule']}\n"
            f"- artefacto : {l['artifact']}\n"
            f"- test rojo : {l['test']}\n"
            f"- guarda con: if \"{l['id']}\" in lessons:\n"
        )

    tools = sorted(p.name for p in (ROOT / "agents" / "common" / "tools").glob("*.py"))

    return f"""Eres el constructor de la siguiente version de un sistema de ingesta de
anuncios de autos usados. Tu trabajo es escribir {dst} a partir de {src} mas las
lecciones que el sistema aprendio de sus propias corridas.

{CONTRATO.format(to=dst)}

## Codigo del predecesor ({src})
```python
{pred}
```

## Herramientas que ya existen en agents/common/tools/
{tools or "(ninguna todavia)"}

Utilidades disponibles que SI debes reutilizar:
- agents/common/vin.py        -> is_valid(vin), check_digit(vin)
- agents/common/constants.py  -> USD_MXN, MILES_TO_KM, MODEL_YEARS
- store.find_by_vin(vin), store.save(record), store.confirm(case_id)

## Lecciones a heredar ({len(lessons)})
{chr(10).join(bloques) or "(ninguna)"}

## Criterio de exito
Al terminar, estos comandos deben pasar:
  RSI_AGENT={dst} python3 -m pytest tests/ -q
  python3 agents/run.py --version {dst} --split holdout && python3 bench/score.py runs/{dst}-holdout.json

Escribe los archivos directamente. Explica en 3 lineas que cambio y por que.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", default="v0")
    ap.add_argument("--to", dest="dst", default="v1")
    ap.add_argument("--print-prompt", action="store_true")
    ap.add_argument("--model", default="gpt-5-codex")
    args = ap.parse_args()

    prompt = build_prompt(args.src, args.dst)
    dest = ROOT / "runs" / f"build-prompt-{args.src}-to-{args.dst}.md"
    dest.write_text(prompt)
    (ROOT / "agents" / args.dst).mkdir(parents=True, exist_ok=True)
    init = ROOT / "agents" / args.dst / "__init__.py"
    init.touch()

    print(f"prompt de construccion -> {dest.relative_to(ROOT)}")
    if args.print_prompt:
        print("\n" + prompt)
        return

    if not shutil.which("codex"):
        print("\n!! `codex` no esta en el PATH.")
        print("   Instala el CLI (npm i -g @openai/codex) o pega el prompt a mano:")
        print(f"   cat {dest.relative_to(ROOT)}")
        print("   Si lo pegas a mano, dilo en la demo: hubo intervencion humana.")
        return

    print(f"invocando Codex ({args.model}) para construir {args.dst}...\n")
    subprocess.run(
        ["codex", "exec", "--model", args.model, "--full-auto", prompt],
        cwd=ROOT, check=False,
    )


if __name__ == "__main__":
    main()
