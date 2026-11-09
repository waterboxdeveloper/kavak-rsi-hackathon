"""PASO 1 del loop: OBSERVAR.

Lee el score de una corrida y agrupa las fallas por tipo, con evidencia
concreta (caso, campo, lo que se esperaba vs lo que salio).

Esto es la "senal" de la que habla la rubrica: sin evidencia puntual, la
leccion que venga despues es opinion.

  python3 loop/observe.py runs/v0-train.json
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bench.score import load_cases, score


def rel(path):
    """Ruta relativa a la raiz del repo, acepte o no una ruta absoluta."""
    p = pathlib.Path(path).resolve()
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def observe(run_path, max_evidence=3):
    run = json.loads(pathlib.Path(run_path).read_text())
    result = score(run)
    cases = load_cases()
    records = {r["case_id"]: r for r in run["records"]}

    groups = {}
    for entry in result["cases"]:
        if entry["passed"]:
            continue
        case = cases[entry["case_id"]]
        for defect in case["defects"] or ["(limpio)"]:
            g = groups.setdefault(defect, {"defect": defect, "count": 0, "fields": set(), "evidence": []})
            g["count"] += 1
            g["fields"].update(entry["failed_fields"])
            if len(g["evidence"]) < max_evidence:
                got = records[entry["case_id"]]
                g["evidence"].append({
                    "case_id": case["id"],
                    "listing": case["listing"],
                    "expected": {f: case["expected"].get(f) for f in entry["failed_fields"]},
                    "got": {f: got.get(f) for f in entry["failed_fields"]},
                })

    for name, chk in result["integrity"].items():
        if chk["passed"]:
            continue
        defect = {"no_duplicate_inventory": "duplicate_vin",
                  "no_phantom_confirmation": "write_interrupted"}.get(name, name)
        g = groups.setdefault(defect, {"defect": defect, "count": 0, "fields": set(), "evidence": []})
        g["fields"].add(f"integrity:{name}")
        g["evidence"].append({"integrity_check": name, "evidence": chk["evidence"]})

    for g in groups.values():
        g["fields"] = sorted(g["fields"])

    out = {
        "source_run": rel(run_path),
        "version": run["version"],
        "split": run["split"],
        "totals": result["totals"],
        "failure_groups": sorted(groups.values(), key=lambda g: -g["count"]),
    }
    dest = ROOT / "runs" / f"{run['version']}-{run['split']}.failures.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    return out, dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_file")
    args = ap.parse_args()
    out, dest = observe(args.run_file)

    print(f"\n== fallas observadas en {out['version']} ({out['split']}) ==")
    for g in out["failure_groups"]:
        print(f"\n  [{g['count']:2d} casos] {g['defect']}  campos: {', '.join(g['fields'])}")
        for ev in g["evidence"][:1]:
            if "listing" in ev:
                print(f"      {ev['case_id']}: {ev['listing'][:76]}")
                print(f"      esperado {ev['expected']}  ->  obtenido {ev['got']}")
            else:
                print(f"      chequeo {ev['integrity_check']}: {ev['evidence']}")
    print(f"\n  -> {dest.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
