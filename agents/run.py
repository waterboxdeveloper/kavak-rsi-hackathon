"""Runner: corre una version del agente sobre el banco de casos.

  python3 agents/run.py --version v0
  python3 agents/run.py --version v1 --split holdout
  python3 agents/run.py --version v2 --ablate L2      # apaga una leccion

Guarda el resultado en runs/<version>[-ablate-Lx]-<split>.json
"""

import argparse
import importlib
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.common.engine import get_engine
from agents.common.store import InventoryStore


def load_cases(split="all"):
    path = ROOT / "bench" / "cases.jsonl"
    if not path.exists():
        sys.exit("falta bench/cases.jsonl -> corre `make bench`")
    cases = [json.loads(line) for line in path.open() if line.strip()]
    if split != "all":
        cases = [c for c in cases if c["split"] == split]
    return cases


def load_enabled_lessons(ablate=()):
    """Lee lessons/lessons.jsonl y devuelve los ids activos."""
    path = ROOT / "lessons" / "lessons.jsonl"
    if not path.exists():
        return set()
    enabled = set()
    for line in path.open():
        if not line.strip():
            continue
        lesson = json.loads(line)
        if lesson.get("enabled", True) and lesson["id"] not in ablate:
            enabled.add(lesson["id"])
    return enabled


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v0")
    ap.add_argument("--split", default="all", choices=["all", "train", "holdout"])
    ap.add_argument("--engine", default="stub", choices=["stub", "openai"])
    ap.add_argument("--ablate", default="", help="ids de lecciones a apagar, coma")
    args = ap.parse_args()

    ablate = {x.strip() for x in args.ablate.split(",") if x.strip()}
    cases = load_cases(args.split)
    lessons = load_enabled_lessons(ablate)

    module = importlib.import_module(f"agents.{args.version}.agent")
    crash_ids = [c["id"] for c in cases if c.get("simulate_write_crash")]
    store = InventoryStore(crash_ids=crash_ids)

    t0 = time.time()
    records = module.ingest(cases, store, get_engine(args.engine), lessons)
    elapsed = round(time.time() - t0, 3)

    suffix = f"-ablate-{'+'.join(sorted(ablate))}" if ablate else ""
    out = ROOT / "runs" / f"{args.version}{suffix}-{args.split}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "version": args.version,
        "split": args.split,
        "engine": args.engine,
        "lessons_enabled": sorted(lessons),
        "lessons_ablated": sorted(ablate),
        "seconds": elapsed,
        "records": records,
        "store": store.snapshot(),
    }, ensure_ascii=False, indent=2))

    print(f"[{args.version}] {len(records)} casos en {elapsed}s")
    print(f"  lecciones activas: {sorted(lessons) or '(ninguna)'}")
    if ablate:
        print(f"  lecciones APAGADAS: {sorted(ablate)}")
    print(f"  -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
