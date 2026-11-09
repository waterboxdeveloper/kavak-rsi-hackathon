"""Scorer determinista. CERO LLM aqui: un juez-LLM haria el numero discutible.

Un caso cuenta como RESUELTO solo si los 7 campos cuadran exacto
(make, model, year, odometer_km, price_mxn, vin, flags).

Ademas dos chequeos de INTEGRIDAD a nivel lote, que son fallas de proceso:
  no_duplicate_inventory -> un VIN repetido no debe crear inventario nuevo
  no_phantom_confirmation -> no confirmar nada que no quedo guardado

  python3 bench/score.py runs/v0-all.json
  python3 bench/score.py runs/v0-all.json --json
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.common.constants import SCORED_FIELDS


def load_cases():
    return {
        c["id"]: c
        for c in (json.loads(l) for l in (ROOT / "bench" / "cases.jsonl").open() if l.strip())
    }


def compare(expected, got):
    """Devuelve la lista de campos que no cuadran."""
    bad = []
    for field in SCORED_FIELDS:
        exp, val = expected.get(field), got.get(field)
        if field == "flags":
            exp, val = sorted(exp or []), sorted(val or [])
        if exp != val:
            bad.append(field)
    return bad


def integrity_checks(run, cases):
    checks = {}

    # 1) un VIN que ya existia no debe crear un alta nueva
    created_by_vin = {}
    for r in run["records"]:
        if r.get("action") == "created" and r.get("vin"):
            created_by_vin.setdefault(r["vin"], []).append(r["case_id"])
    dupes = {v: ids for v, ids in created_by_vin.items() if len(ids) > 1}
    checks["no_duplicate_inventory"] = {
        "passed": not dupes,
        "evidence": dupes,
    }

    # 2) ninguna confirmacion sin fila persistida
    saved = {r["case_id"] for r in run["store"]["rows"]}
    phantom = [c["case_id"] for c in run["store"]["confirmations"] if c["case_id"] not in saved]
    checks["no_phantom_confirmation"] = {
        "passed": not phantom,
        "evidence": phantom,
    }
    return checks


def score(run):
    cases = load_cases()
    per_case, by_defect = [], {}

    for r in run["records"]:
        case = cases[r["case_id"]]
        bad = compare(case["expected"], r)
        entry = {
            "case_id": r["case_id"],
            "split": case["split"],
            "passed": not bad,
            "failed_fields": bad,
            "defects": case["defects"],
        }
        per_case.append(entry)
        for d in case["defects"] or ["(limpio)"]:
            slot = by_defect.setdefault(d, {"total": 0, "passed": 0})
            slot["total"] += 1
            slot["passed"] += 0 if bad else 1

    checks = integrity_checks(run, cases)

    def tally(split):
        rows = [c for c in per_case if split in ("all", c["split"])]
        return {"passed": sum(1 for c in rows if c["passed"]), "total": len(rows)}

    return {
        "version": run["version"],
        "split": run["split"],
        "lessons_enabled": run.get("lessons_enabled", []),
        "lessons_ablated": run.get("lessons_ablated", []),
        "totals": {"all": tally("all"), "train": tally("train"), "holdout": tally("holdout")},
        "integrity": checks,
        "by_defect": by_defect,
        "cases": per_case,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    run = json.loads(pathlib.Path(args.run_file).read_text())
    result = score(run)

    out = ROOT / "runs" / (pathlib.Path(args.run_file).stem + ".score.json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    t = result["totals"]
    print(f"\n== {result['version']}  (split={result['split']}) ==")
    print(f"  casos resueltos : {t['all']['passed']}/{t['all']['total']}")
    if t["train"]["total"]:
        print(f"    train         : {t['train']['passed']}/{t['train']['total']}")
    if t["holdout"]["total"]:
        print(f"    holdout       : {t['holdout']['passed']}/{t['holdout']['total']}  <- el numero que presentamos")
    ok = sum(1 for c in result["integrity"].values() if c["passed"])
    print(f"  integridad      : {ok}/{len(result['integrity'])}")
    for name, chk in result["integrity"].items():
        mark = "OK " if chk["passed"] else "FALLA"
        print(f"    [{mark}] {name} {'' if chk['passed'] else chk['evidence']}")
    print("\n  por tipo de defecto:")
    for d, s in sorted(result["by_defect"].items(), key=lambda kv: (kv[1]["passed"] / kv[1]["total"], kv[0])):
        print(f"    {s['passed']:3d}/{s['total']:<3d}  {d}")
    print(f"\n  -> {out.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
