"""Validaciones derivadas de L3, L4 y L6."""

import re
import unicodedata

from agents.common.constants import MODEL_YEARS
from agents.common.vin import is_valid


def vin_flags(vin):
    """Emite la bandera de VIN cuando el formato o checksum no es valido."""
    return [] if is_valid(vin) else ["vin_invalid"]


def salvage_flags(description):
    """Detecta lenguaje de salvamento, perdida total o recuperacion."""
    if not description:
        return []

    text = unicodedata.normalize("NFD", str(description).casefold())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    patterns = (
        r"\bsalvament\w*",
        r"\bsalvage\b",
        r"\bperdida\s+total\b",
        r"\btitulo\s+de\s+recuperacion\b",
        r"\brehabilitad\w*",
        r"\breconstruid\w*",
    )
    return ["salvage"] if any(re.search(pattern, text) for pattern in patterns) else []


def year_model_flags(make, model, year):
    """Emite la bandera si el año queda fuera del rango catalogado."""
    if make is None or model is None or year is None:
        return []
    try:
        year = int(year)
    except (TypeError, ValueError):
        return []

    years = MODEL_YEARS.get((make, model))
    if years and not (years[0] <= year <= years[1]):
        return ["year_model_mismatch"]
    return []
