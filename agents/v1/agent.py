"""V1 -- extractor de anuncios con las lecciones heredadas de V0."""

import re

from agents.common.tools.money import normalize_price_mxn
from agents.common.tools.odometer import normalize_odometer
from agents.common.tools.validators import (
    salvage_flags,
    vin_flags,
    year_model_flags,
)


VERSION = "v1"


def naive_int(raw):
    """Conserva el comportamiento de V0 cuando no hay lecciones activas."""
    if not raw:
        return None
    text = re.sub(r"(?<=\d),(?=\d{3})", "", str(raw))
    match = re.search(r"\d+", text)
    return int(match.group(0)) if match else None


def ingest(cases, store, engine, lessons=frozenset()):
    records = []
    lessons = set(lessons or ())

    for case in cases:
        raw = engine.extract(case["listing"])
        vin = raw.get("vin")
        year = int(raw["year"]) if raw.get("year") else None

        odometer_lessons = set()
        if "L1" in lessons:
            odometer_lessons.add("L1")
        if "L5" in lessons:
            odometer_lessons.add("L5")
        if "L8" in lessons:
            odometer_lessons.add("L8")
        if odometer_lessons:
            odometer_km = normalize_odometer(raw.get("odometer_raw"), odometer_lessons)
        else:
            odometer_km = naive_int(raw.get("odometer_raw"))

        price_lessons = set()
        if "L2" in lessons:
            price_lessons.add("L2")
        if "L7" in lessons:
            price_lessons.add("L7")
        if "L9" in lessons:
            price_lessons.add("L9")
        if price_lessons:
            price_mxn = normalize_price_mxn(raw.get("price_raw"), price_lessons)
        else:
            price_mxn = naive_int(raw.get("price_raw"))

        # Un VIN ya persistido no crea otra fila de inventario. Esta conducta
        # es parte del contrato operativo del store, no de las nueve reglas
        # de normalizacion y por eso no se liga artificialmente a una leccion.
        duplicate = bool(vin and store.find_by_vin(vin))
        flags = ["duplicate"] if duplicate else []
        if "L4" in lessons:
            flags.extend(salvage_flags(raw.get("description") or case["listing"]))
        if "L3" in lessons:
            flags.extend(vin_flags(vin))
        if "L6" in lessons:
            flags.extend(year_model_flags(raw.get("make"), raw.get("model"), year))

        record = {
            "case_id": case["id"],
            "make": raw.get("make"),
            "model": raw.get("model"),
            "year": year,
            "odometer_km": odometer_km,
            "price_mxn": price_mxn,
            "vin": vin,
            "flags": flags,
            "action": "created",
        }

        if duplicate:
            record["action"] = "merged_duplicate"
        else:
            # Solo se confirma despues de que save termino correctamente.
            try:
                store.save(record)
            except Exception:
                record["action"] = "failed"
            else:
                store.confirm(case["id"])

        records.append(record)

    return records
