"""Genera el banco de casos del benchmark (bench/cases.jsonl).

Reglas del banco:
  - 60 casos: 40 `train` (el loop SI los ve al aprender) + 20 `holdout`
    (el loop NUNCA los ve; es el numero que presentamos).
  - Cada caso trae `defects`: las fallas inyectadas a proposito. Eso nos deja
    decir con precision "la leccion L2 arreglo exactamente estos 6 casos".
  - Semilla fija -> el mismo banco siempre. Sin reproducibilidad no hay
    comparacion valida entre versiones.

Uso:  python3 bench/generate_cases.py
"""

import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.constants import MILES_TO_KM, MODELS, USD_MXN
from agents.common import vin as vinlib

OUT = pathlib.Path(__file__).parent / "cases.jsonl"
RNG = random.Random(7)

EXTRAS_CLEAN = [
    "unico dueno, factura de agencia",
    "servicios en agencia, llantas nuevas",
    "credito disponible, acepto cambio",
    "impecable, siempre en garage",
]
EXTRAS_SALVAGE = [
    "auto de salvamento, ya reconstruido",
    "fue perdida total, rehabilitado",
    "titulo de recuperacion, checar bien",
]


def random_vin():
    body = "".join(RNG.choice(vinlib.ALPHABET) for _ in range(17))
    return vinlib.with_valid_check_digit(body)


def odometer_text(km, defect):
    """Escribe el kilometraje de forma 'sucia' segun el defecto."""
    if defect == "odo_k_suffix":
        return f"{km // 1000}k kms", km
    if defect == "odo_dot_sep":
        return f"{km // 1000}.{km % 1000:03d} km", km
    if defect == "odo_miles":
        miles = round(km / MILES_TO_KM)
        return f"{miles:,} mi", round(miles * MILES_TO_KM)
    return f"{km:,} km", km


def price_text(mxn, defect):
    """Escribe el precio de forma 'sucia' segun el defecto."""
    if defect == "price_k_suffix":
        return f"${mxn // 1000}k", (mxn // 1000) * 1000
    if defect == "price_usd":
        usd = round(mxn / USD_MXN)
        return f"USD ${usd:,}", round(usd * USD_MXN)
    if defect == "price_dot_sep":
        return f"${mxn // 1000}.{mxn % 1000:03d} MXN", mxn
    return f"${mxn:,}", mxn


# (odo_defect, price_defect, vin_defect, year_defect, salvage)
# ~45% de los casos salen limpios: queremos una linea base que resuelva algo,
# no un V0 que falle en todo (eso no se puede mejorar de forma legible).
PLAN = [
    (None, None, False, False, False),
    ("odo_k_suffix", None, False, False, False),
    (None, "price_usd", False, False, False),
    (None, None, True, False, False),
    (None, None, False, False, True),
    ("odo_miles", None, False, False, False),
    (None, None, False, False, False),
    (None, "price_k_suffix", False, False, False),
    ("odo_dot_sep", None, False, False, False),
    (None, None, False, True, False),
    (None, None, False, False, False),
    ("odo_k_suffix", "price_usd", False, False, True),
    (None, None, False, False, False),
    (None, "price_dot_sep", True, False, False),
    ("odo_miles", None, False, True, False),
]


def build_case(idx, split, plan, template_pool):
    odo_d, price_d, vin_bad, year_bad, salvage = plan
    mk, md, (y0, y1) = RNG.choice(MODELS)
    year = RNG.randint(y0, y1)
    if year_bad:
        year = y0 - RNG.randint(3, 6)  # ano imposible para esa generacion

    km = RNG.randint(18, 180) * 1000
    mxn = RNG.randint(80, 420) * 1000

    odo_txt, odo_expected = odometer_text(km, odo_d)
    price_txt, price_expected = price_text(mxn, price_d)

    vin = random_vin()
    if vin_bad:
        vin = vinlib.corrupt_check_digit(vin)

    extra = RNG.choice(EXTRAS_SALVAGE if salvage else EXTRAS_CLEAN)
    listing = template_pool.format(
        make=mk, model=md, year=year, odo=odo_txt, price=price_txt, vin=vin, extra=extra
    )

    flags = []
    if salvage:
        flags.append("salvage")
    if vin_bad:
        flags.append("vin_invalid")
    if year_bad:
        flags.append("year_model_mismatch")

    defects = [d for d in (odo_d, price_d) if d]
    if vin_bad:
        defects.append("vin_invalid_checksum")
    if year_bad:
        defects.append("year_model_impossible")
    if salvage:
        defects.append("salvage_wording")

    return {
        "id": f"C{idx:03d}",
        "split": split,
        "listing": listing,
        "expected": {
            "make": mk,
            "model": md,
            "year": year,
            "odometer_km": odo_expected,
            "price_mxn": price_expected,
            "vin": vin,
            "flags": sorted(flags),
        },
        "defects": sorted(defects),
    }


TEMPLATES = [
    "{make} {model} {year} -- {odo} -- {price} -- VIN {vin} -- {extra}",
    "VENDO {make} {model} {year} / {odo} / {price} / {extra} / vin: {vin}",
    "{year} {make} {model} {extra}. Kilometraje {odo}. Precio {price}. VIN {vin}",
    "*** {make} {model} {year} *** {price} ** {odo} ** {extra} ** {vin}",
]


def main():
    cases = []
    for i in range(60):
        split = "train" if i < 40 else "holdout"
        plan = PLAN[i % len(PLAN)]
        tpl = TEMPLATES[i % len(TEMPLATES)]
        cases.append(build_case(i + 1, split, plan, tpl))

    # --- fallas de PROCESO (las que originan V2) -------------------------
    # 1) VIN duplicado: el mismo auto publicado dos veces. El segundo anuncio
    #    NO debe crear inventario nuevo, debe marcarse `duplicate`.
    for src, dup in [(2, 18), (42, 55)]:
        a, b = cases[src], cases[dup]
        b["listing"] = b["listing"].replace(b["expected"]["vin"], a["expected"]["vin"])
        b["expected"]["vin"] = a["expected"]["vin"]
        b["expected"]["flags"] = sorted(set(b["expected"]["flags"]) | {"duplicate"})
        b["defects"] = sorted(set(b["defects"]) | {"duplicate_vin"})
        b["duplicate_of"] = a["id"]

    # 2) Escritura interrumpida: el store falla la primera vez. Confirmar
    #    antes de persistir produce una confirmacion fantasma.
    for i in (9, 50):
        cases[i]["simulate_write_crash"] = True
        cases[i]["defects"] = sorted(set(cases[i]["defects"]) | {"write_interrupted"})

    with OUT.open("w") as fh:
        for c in cases:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    train = sum(1 for c in cases if c["split"] == "train")
    print(f"escritos {len(cases)} casos en {OUT}  ({train} train / {len(cases)-train} holdout)")
    defect_counts = {}
    for c in cases:
        for d in c["defects"] or ["(limpio)"]:
            defect_counts[d] = defect_counts.get(d, 0) + 1
    for d, n in sorted(defect_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:3d}  {d}")


if __name__ == "__main__":
    main()
