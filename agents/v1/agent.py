"""V1 -- extractor con las nueve lecciones heredadas de V0."""

import re

from agents.common.tools.money import normalize_price_mxn
from agents.common.tools.odometer import normalize_odometer
from agents.common.tools.validators import salvage_flags, vin_flags, year_model_flags


VERSION = "v1"


def naive_int(raw):
    """Parseo base de V0, conservado para la ablacion de las lecciones."""
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

        odometer_raw = raw.get("odometer_raw")
        odometer_km = naive_int(odometer_raw)
        odometer_options = {
            "handle_k": False,
            "handle_miles": False,
            "handle_dot": False,
        }
        if "L1" in lessons:
            odometer_options["handle_k"] = True
        if "L5" in lessons:
            odometer_options["handle_miles"] = True
        if "L8" in lessons:
            odometer_options["handle_dot"] = True
        if any(odometer_options.values()):
            odometer_km = normalize_odometer(odometer_raw, **odometer_options)

        price_raw = raw.get("price_raw")
        price_mxn = naive_int(price_raw)
        price_options = {
            "convert_usd": False,
            "handle_k": False,
            "handle_dot": False,
        }
        if "L2" in lessons:
            price_options["convert_usd"] = True
        if "L7" in lessons:
            price_options["handle_k"] = True
        if "L9" in lessons:
            price_options["handle_dot"] = True
        if any(price_options.values()):
            price_mxn = normalize_price_mxn(price_raw, **price_options)

        year = int(raw["year"]) if raw.get("year") else None
        flags = []
        if "L3" in lessons:
            flags.extend(vin_flags(raw.get("vin")))
        if "L4" in lessons:
            flags.extend(salvage_flags(raw.get("description") or case["listing"]))
        if "L6" in lessons:
            flags.extend(year_model_flags(raw.get("make"), raw.get("model"), year))

        record = {
            "case_id": case["id"],
            "make": raw.get("make"),
            "model": raw.get("model"),
            "year": year,
            "odometer_km": odometer_km,
            "price_mxn": price_mxn,
            "vin": raw.get("vin"),
            "flags": flags,
            "action": "created",
        }

        # V1 conserva exactamente el flujo de V0: confirmar antes de guardar.
        store.confirm(case["id"])
        try:
            store.save(record)
        except Exception:
            record["action"] = "failed"

        records.append(record)
    return records
