"""Reporte comparativo: la tabla que se proyecta en la demo.

Junta todos los runs/*.score.json y arma la tabla de versiones. Imprime en
markdown para pegarla directo en el .md de la fase.

  python3 report.py
  python3 report.py --split holdout
"""

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).parent


def load_scores():
    out = []
    for p in sorted((ROOT / "runs").glob("*.score.json")):
        out.append((p, json.loads(p.read_text())))
    return out


def load_lessons():
    path = ROOT / "lessons" / "lessons.jsonl"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.open() if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="holdout", choices=["all", "train", "holdout"])
    args = ap.parse_args()

    scores = load_scores()
    if not scores:
        print("no hay runs todavia -> corre `make demo`")
        return

    lessons = load_lessons()
    print(f"\n# Resultados (split: {args.split})\n")
    print("| version | lecciones activas | casos resueltos | integridad |")
    print("|---|---|---|---|")
    for path, s in scores:
        t = s["totals"].get(args.split) or s["totals"]["all"]
        if not t["total"]:
            continue
        ok = sum(1 for c in s["integrity"].values() if c["passed"])
        label = s["version"]
        if s.get("lessons_ablated"):
            label += f" (sin {'+'.join(s['lessons_ablated'])})"
        activas = ",".join(s["lessons_enabled"]) or "-"
        print(f"| {label} | {activas} | {t['passed']}/{t['total']} | {ok}/{len(s['integrity'])} |")

    print(f"\n## Lecciones acumuladas ({len(lessons)})\n")
    if lessons:
        print("| id | defecto | regla | heredada por |")
        print("|---|---|---|---|")
        for l in lessons:
            est = "" if l.get("enabled", True) else " (APAGADA)"
            print(f"| {l['id']}{est} | {l['defect']} | {l['rule'][:70]} | {','.join(l.get('inherited_by') or []) or '-'} |")
    else:
        print("(ninguna todavia)")

    print("\n## Que sigue fallando\n")
    last = scores[-1][1]
    pend = {d: s for d, s in last["by_defect"].items() if s["passed"] < s["total"]}
    if pend:
        for d, s in sorted(pend.items(), key=lambda kv: kv[1]["passed"] / kv[1]["total"]):
            print(f"- `{d}`: {s['passed']}/{s['total']}")
    else:
        print("- nada en este banco. Siguiente paso: ampliar el banco de casos.")
    print()


if __name__ == "__main__":
    main()
