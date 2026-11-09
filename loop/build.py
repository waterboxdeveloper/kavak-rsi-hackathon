"""PASO 3 del loop: CONSTRUIR EL SUCESOR (con un agente de codigo).

Aqui el agente de codigo no es nuestro copiloto: es el organo de construccion
del sistema. Este script arma el prompt con (codigo del predecesor + lecciones
activas + tests rojos) y lo manda a construir.

  python3 loop/build.py --from v0 --to v1
  python3 loop/build.py --from v1 --to v2 --print-prompt      # solo imprime
  python3 loop/build.py --from v0 --to v1 --builder claude    # el otro agente

OJO, y esto es lo importante de entender: el constructor es INTERCAMBIABLE.
Lo unico que lo acopla al sistema son las 3 lineas de BUILDERS de abajo: un
subproceso que recibe texto y escribe archivos. Codex y Claude Code son
sustituibles sin tocar nada mas; el valor del proyecto esta en el banco de
casos, la evidencia y los tests, no en cual CLI invocamos.

Si el CLI no esta instalado, guarda el prompt en runs/ para pegarlo a mano.
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

# El constructor, intercambiable. Cada entrada devuelve el comando a ejecutar.
#
# Verificado contra codex-cli 0.150.0 el 9 nov 2026: `codex exec` NO acepta
# --full-auto (lo rechaza al parsear); el flag correcto para que pueda escribir
# archivos es --sandbox workspace-write. Si cambias de version, revisa primero
# `codex exec --help`.
BUILDERS = {
    "codex": lambda prompt, model: (
        ["codex", "exec", "--sandbox", "workspace-write"]
        + (["--model", model] if model else [])
        + [prompt]
    ),
    "claude": lambda prompt, model: (
        ["claude", "-p", "--permission-mode", "acceptEdits"]
        + (["--model", model] if model else [])
        + [prompt]
    ),
}

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
    n_lessons = len(lessons)

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

## Lecciones a heredar ({n_lessons})
{chr(10).join(bloques) or "(ninguna)"}

## Criterio de exito
Al terminar, estos comandos deben pasar (pytest NO esta instalado; usa el
corredor del repo, que no tiene dependencias):
  RSI_AGENT={dst} python3 run_tests.py        # los {n_lessons} tests deben quedar VERDES
  python3 agents/run.py --version {dst} --split holdout
  python3 bench/score.py runs/{dst}-holdout.json

Escribe los archivos directamente. Explica en 3 lineas que cambio y por que.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", default="v0")
    ap.add_argument("--to", dest="dst", default="v1")
    ap.add_argument("--print-prompt", action="store_true")
    ap.add_argument("--builder", default="codex", choices=sorted(BUILDERS))
    ap.add_argument("--model", default=None,
                    help="opcional; por default usa el modelo configurado en el CLI")
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

    if not shutil.which(args.builder):
        print(f"\n!! `{args.builder}` no esta en el PATH.")
        print("   Opciones: instalar el CLI, usar --builder con el otro agente,")
        print(f"   o pegar el prompt a mano:  cat {dest.relative_to(ROOT)}")
        print("   Si lo pegas a mano, dilo en la demo: hubo intervencion humana.")
        return

    cmd = BUILDERS[args.builder](prompt, args.model)
    print(f"invocando {args.builder} ({args.model or 'modelo por default'}) "
          f"para construir {args.dst}...\n")
    # El prompt es largo, asi que mostramos el comando sin el (ultimo elemento).
    print(f"  $ {' '.join(cmd[:-1])} <prompt>\n")
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    print(f"\n{args.builder} termino con codigo {result.returncode}")
    print("Ahora verifica que no toco la vara de medir:")
    print("  git status --short bench/ lessons/ tests/ agents/v0/")


if __name__ == "__main__":
    main()
