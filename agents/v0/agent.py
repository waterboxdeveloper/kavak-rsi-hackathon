"""V0 -- Extractor de anuncios. La version ingenua, escrita a mano.

Esta version es *a proposito* ingenua. Hace lo que haria cualquiera el primer
dia: saca el primer numero que encuentra, confia en el VIN, no valida nada y
confirma el alta antes de guardarla.

No la arregles. Sus fallas son el combustible del sistema.

CONTRATO que toda version debe respetar (V1 y V2 tambien):
    VERSION: str
    ingest(cases, store, engine, lessons) -> list[record]

    record = {case_id, make, model, year, odometer_km, price_mxn, vin,
              flags: list[str], action: "created"|"merged_duplicate"|"rejected"|"failed"}

    `lessons` es el conjunto de ids de lecciones ACTIVAS. Cada comportamiento
    aprendido debe ir dentro de `if "Lx" in lessons:` para que el ablation
    (apagar una leccion) funcione sin reconstruir el agente.
"""

import re

VERSION = "v0"


def naive_int(raw):
    """Parseo ingenuo: quita separadores de miles con coma y toma el 1er numero.

    Funciona para '56,000 km' y '$249,000'.
    Falla para '56k kms', '56.000 km', '35,000 mi' y 'USD $13,500'.
    """
    if not raw:
        return None
    s = re.sub(r"(?<=\d),(?=\d{3})", "", str(raw))
    m = re.search(r"\d+", s)
    return int(m.group(0)) if m else None


def ingest(cases, store, engine, lessons=frozenset()):
    records = []
    for case in cases:
        raw = engine.extract(case["listing"])

        record = {
            "case_id": case["id"],
            "make": raw.get("make"),
            "model": raw.get("model"),
            "year": int(raw["year"]) if raw.get("year") else None,
            "odometer_km": naive_int(raw.get("odometer_raw")),
            "price_mxn": naive_int(raw.get("price_raw")),
            "vin": raw.get("vin"),
            "flags": [],          # V0 no valida nada
            "action": "created",
        }

        # BUG de proceso: confirmamos primero y guardamos despues. Si la
        # escritura falla, el usuario ya recibio un "listo" que es mentira.
        store.confirm(case["id"])
        try:
            store.save(record)
        except Exception:
            record["action"] = "failed"

        records.append(record)
    return records
