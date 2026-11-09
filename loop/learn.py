"""PASO 2 del loop: APRENDER.

Convierte grupos de fallas en LECCIONES PERSISTIDAS. Una leccion no es prosa:
es un registro con (a) la evidencia que la provoco, (b) la regla, (c) el
artefacto de codigo que debe existir y (d) un test que hoy esta ROJO.

Ese test rojo es la prueba de que la leccion es real y, cuando se ponga verde,
la prueba de que el sucesor la heredo.

  python3 loop/learn.py runs/v0-train.failures.json
  python3 loop/learn.py runs/v0-train.failures.json --llm   # pule la redaccion
"""

import argparse
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

LESSONS = ROOT / "lessons" / "lessons.jsonl"
TESTS = ROOT / "tests"

# Catalogo determinista: defecto observado -> leccion propuesta.
# Es el "cerebro" del aprendizaje. Lo dejamos explicito a proposito: si el
# jurado pregunta "quien decidio la leccion", la respuesta es auditable.
CATALOG = {
    "odo_k_suffix": {
        "rule": "El kilometraje puede venir con sufijo 'k' (56k = 56000). Normalizar antes de guardar.",
        "artifact": "agents/common/tools/odometer.py::normalize_odometer",
        "test": [("normalize_odometer('56k kms')", 56000), ("normalize_odometer('120 k km')", 120000)],
        "import": "from agents.common.tools.odometer import normalize_odometer",
    },
    "odo_dot_sep": {
        "rule": "El punto se usa como separador de miles en MX (56.000 km = 56000). Normalizar.",
        "artifact": "agents/common/tools/odometer.py::normalize_odometer",
        "test": [("normalize_odometer('56.000 km')", 56000)],
        "import": "from agents.common.tools.odometer import normalize_odometer",
    },
    "odo_miles": {
        "rule": "Si la unidad es mi/millas, convertir a km con factor 1.60934 y redondear.",
        "artifact": "agents/common/tools/odometer.py::normalize_odometer",
        "test": [("normalize_odometer('35,000 mi')", 56327)],
        "import": "from agents.common.tools.odometer import normalize_odometer",
    },
    "price_usd": {
        "rule": "Precios en USD deben convertirse a MXN con el tipo de cambio fijo del benchmark (18.50).",
        "artifact": "agents/common/tools/money.py::normalize_price_mxn",
        "test": [("normalize_price_mxn('USD $13,500')", 249750)],
        "import": "from agents.common.tools.money import normalize_price_mxn",
    },
    "price_k_suffix": {
        "rule": "El precio puede venir con sufijo 'k' ($249k = 249000). Normalizar.",
        "artifact": "agents/common/tools/money.py::normalize_price_mxn",
        "test": [("normalize_price_mxn('$249k')", 249000)],
        "import": "from agents.common.tools.money import normalize_price_mxn",
    },
    "price_dot_sep": {
        "rule": "El punto como separador de miles tambien aplica al precio ($249.000 MXN = 249000).",
        "artifact": "agents/common/tools/money.py::normalize_price_mxn",
        "test": [("normalize_price_mxn('$249.000 MXN')", 249000)],
        "import": "from agents.common.tools.money import normalize_price_mxn",
    },
    "vin_invalid_checksum": {
        "rule": "Validar el digito verificador del VIN (ISO 3779). Si no cuadra, emitir bandera 'vin_invalid'.",
        "artifact": "agents/common/tools/validators.py::vin_flags",
        "test": [("vin_flags('3VWA11AA1AA000001')", "['vin_invalid']")],
        "import": "from agents.common.tools.validators import vin_flags",
        "raw_expected": True,
    },
    "year_model_impossible": {
        "rule": "Cruzar ano contra el rango de la generacion del modelo. Si es imposible, bandera 'year_model_mismatch'.",
        "artifact": "agents/common/tools/validators.py::year_model_flags",
        "test": [("year_model_flags('Kia', 'Rio', 2011)", "['year_model_mismatch']")],
        "import": "from agents.common.tools.validators import year_model_flags",
        "raw_expected": True,
    },
    "salvage_wording": {
        "rule": "Detectar lenguaje de salvamento/perdida total/titulo de recuperacion y emitir bandera 'salvage'.",
        "artifact": "agents/common/tools/validators.py::salvage_flags",
        "test": [("salvage_flags('fue perdida total, rehabilitado')", "['salvage']")],
        "import": "from agents.common.tools.validators import salvage_flags",
        "raw_expected": True,
    },
    "duplicate_vin": {
        "rule": "Antes de dar de alta, buscar el VIN en inventario. Si ya existe: NO crear fila nueva, "
                "marcar accion 'merged_duplicate' y bandera 'duplicate'.",
        "artifact": "agents/<version>/agent.py::ingest (dedupe por VIN contra store.find_by_vin)",
        "test": "integrity:no_duplicate_inventory",
        "import": None,
        "stage": "process",
    },
    "write_interrupted": {
        "rule": "Confirmar SOLO despues de que la escritura quedo persistida. Si la escritura falla, "
                "reintentar y, si vuelve a fallar, marcar accion 'failed' sin confirmar.",
        "artifact": "agents/<version>/agent.py::ingest (orden save -> confirm)",
        "test": "integrity:no_phantom_confirmation",
        "import": None,
        "stage": "process",
    },
}

# Regla de disciplina del loop: no aprendemos lecciones de PROCESO mientras
# siga habiendo ruido de extraccion. Con 45 casos fallando, no se puede
# atribuir una falla de integridad a la logica de proceso -- podria ser efecto
# de un campo mal parseado. Primero se limpia la senal, luego se diagnostica.
# Esto es lo que produce de forma natural la cadena V0 -> V1 -> V2.
def stage_of(defect):
    return CATALOG.get(defect, {}).get("stage", "field")

UNIT_TEST_TPL = '''"""Test de la leccion {lid} -- generado por loop/learn.py.

Evidencia original: {evidence}
Regla: {rule}

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

{imp}


{bodies}
'''

INTEGRITY_TEST_TPL = '''"""Test de la leccion {lid} -- generado por loop/learn.py.

Evidencia original: {evidence}
Regla: {rule}

Corre el agente completo y exige el chequeo de integridad `{check}`.
Version bajo prueba: variable de entorno RSI_AGENT (default v1).
"""

import importlib
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.common.engine import get_engine
from agents.common.store import InventoryStore
from agents.run import load_cases, load_enabled_lessons
from bench.score import score


def test_{check}():
    version = os.environ.get("RSI_AGENT", "v1")
    cases = load_cases("all")
    module = importlib.import_module(f"agents.{{version}}.agent")
    store = InventoryStore(crash_ids=[c["id"] for c in cases if c.get("simulate_write_crash")])
    records = module.ingest(cases, store, get_engine("stub"), load_enabled_lessons())
    result = score({{"version": version, "split": "all", "records": records,
                    "store": store.snapshot()}})
    chk = result["integrity"]["{check}"]
    assert chk["passed"], f"{check} fallo: {{chk['evidence']}}"
'''


def next_lesson_id(existing):
    nums = [int(l["id"][1:]) for l in existing if l["id"][1:].isdigit()]
    return f"L{max(nums) + 1 if nums else 1}"


def read_lessons():
    if not LESSONS.exists():
        return []
    return [json.loads(l) for l in LESSONS.open() if l.strip()]


def write_test(lesson, spec, group):
    TESTS.mkdir(exist_ok=True)
    path = TESTS / f"test_lesson_{lesson['id']}.py"
    evidence = ", ".join(
        ev.get("case_id", ev.get("integrity_check", "?")) for ev in group["evidence"]
    )

    if isinstance(spec["test"], str) and spec["test"].startswith("integrity:"):
        check = spec["test"].split(":", 1)[1]
        path.write_text(INTEGRITY_TEST_TPL.format(
            lid=lesson["id"], evidence=evidence, rule=spec["rule"], check=check))
    else:
        bodies = []
        for i, (call, expected) in enumerate(spec["test"], 1):
            exp = expected if spec.get("raw_expected") else repr(expected)
            bodies.append(f"def test_{lesson['id'].lower()}_{i}():\n    assert {call} == {exp}\n")
        path.write_text(UNIT_TEST_TPL.format(
            lid=lesson["id"], evidence=evidence, rule=spec["rule"],
            imp=spec["import"], bodies="\n".join(bodies)))
    return str(path.relative_to(ROOT))


def polish_with_llm(rule, group):
    """Opcional: el LLM redacta la regla a partir de la evidencia cruda."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        ev = json.dumps(group["evidence"][:2], ensure_ascii=False)
        resp = client.chat.completions.create(
            model=os.environ.get("RSI_MODEL", "gpt-5"),
            messages=[{"role": "user", "content":
                       "Eres el modulo de aprendizaje de un sistema de agentes. Con esta evidencia "
                       f"de falla:\n{ev}\n\nEscribe UNA regla imperativa, concreta y verificable "
                       "(max 2 lineas, espanol, sin markdown) que evite la falla. "
                       f"Regla base propuesta: {rule}"}],
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:  # sin API key o sin red: seguimos deterministas
        print(f"  (aviso: no se pudo pulir con LLM: {exc})")
        return rule


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("failures_file")
    ap.add_argument("--llm", action="store_true", help="redactar la regla con el LLM")
    args = ap.parse_args()

    data = json.loads(pathlib.Path(args.failures_file).read_text())
    existing = read_lessons()
    known = {l["defect"] for l in existing}
    new, deferred = [], []

    # Hay ruido de extraccion pendiente?
    field_noise = sum(
        g["count"] for g in data["failure_groups"]
        if stage_of(g["defect"]) == "field" and g["defect"] in CATALOG
    )

    for group in data["failure_groups"]:
        defect = group["defect"]
        if defect in known or defect not in CATALOG:
            continue
        if stage_of(defect) == "process" and field_noise > 0:
            deferred.append((defect, field_noise))
            continue
        spec = CATALOG[defect]
        rule = polish_with_llm(spec["rule"], group) if args.llm else spec["rule"]
        lesson = {
            "id": next_lesson_id(existing + new),
            "defect": defect,
            "trigger": f"{group['count']} casos fallaron en {', '.join(group['fields'])}",
            "evidence_run": data["source_run"],
            "evidence_cases": [ev.get("case_id") for ev in group["evidence"] if ev.get("case_id")],
            "rule": rule,
            "artifact": spec["artifact"],
            "enabled": True,
            "learned_from": data["version"],
            "inherited_by": [],
        }
        lesson["test"] = write_test(lesson, spec, group)
        new.append(lesson)

    with LESSONS.open("a") as fh:
        for lesson in new:
            fh.write(json.dumps(lesson, ensure_ascii=False) + "\n")

    print(f"\n== lecciones nuevas: {len(new)} (acumuladas: {len(existing) + len(new)}) ==")
    for l in new:
        print(f"\n  {l['id']}  [{l['defect']}]  <- {l['trigger']}")
        print(f"      regla    : {l['rule']}")
        print(f"      artefacto: {l['artifact']}")
        print(f"      test ROJO: {l['test']}")
    if not new:
        print("  (nada nuevo que aprender de estas fallas)")
    for defect, noise in deferred:
        print(f"\n  DIFERIDA  [{defect}] -> es una falla de proceso y todavia hay "
              f"{noise} casos con ruido de extraccion.")
        print("      No se puede atribuir causa aun. Se aprende en la siguiente iteracion.")
    print(f"\n  -> {LESSONS.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
