"""Corredor de tests sin dependencias (los archivos tambien sirven con pytest).

Los tests de leccion son la vara ROJO -> VERDE de la demo. Por eso el corredor
no depende de instalar nada: en el hackathon no se pelea con pip.

  python3 run_tests.py                 # prueba v1 (default)
  RSI_AGENT=v2 python3 run_tests.py    # prueba v2
  python3 run_tests.py L3              # solo la leccion L3
"""

import importlib.util
import json
import os
import pathlib
import sys
import traceback

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))

GREEN, RED, DIM, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[0m"


def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lesson_rules():
    path = ROOT / "lessons" / "lessons.jsonl"
    if not path.exists():
        return {}
    return {l["id"]: l for l in (json.loads(x) for x in path.open() if x.strip())}


def main():
    wanted = {a.upper() for a in sys.argv[1:]}
    agent = os.environ.get("RSI_AGENT", "v1")
    rules = lesson_rules()

    files = sorted((ROOT / "tests").glob("test_lesson_*.py"))
    if wanted:
        files = [f for f in files if f.stem.split("_")[-1].upper() in wanted]
    if not files:
        print("no hay tests de leccion todavia -> corre `make learn`")
        return 0

    print(f"\n== tests de leccion (agente bajo prueba: {agent}) ==\n")
    passed = failed = 0
    for path in files:
        lid = path.stem.split("_")[-1].upper()
        rule = rules.get(lid, {}).get("rule", "")
        try:
            mod = load_module(path)
        except Exception as exc:
            failed += 1
            print(f"  {RED}ROJO {RESET} {lid}  {DIM}{rule[:58]}{RESET}")
            print(f"         {RED}{type(exc).__name__}: {exc}{RESET}")
            continue

        errors = []
        for name in sorted(n for n in dir(mod) if n.startswith("test_")):
            try:
                getattr(mod, name)()
            except Exception:
                errors.append((name, traceback.format_exc(limit=2).strip().splitlines()[-1]))

        if errors:
            failed += 1
            print(f"  {RED}ROJO {RESET} {lid}  {DIM}{rule[:58]}{RESET}")
            for name, err in errors:
                print(f"         {RED}{name}: {err}{RESET}")
        else:
            passed += 1
            print(f"  {GREEN}VERDE{RESET} {lid}  {DIM}{rule[:58]}{RESET}")

    print(f"\n  {GREEN}{passed} verdes{RESET} / {RED}{failed} rojos{RESET}\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
