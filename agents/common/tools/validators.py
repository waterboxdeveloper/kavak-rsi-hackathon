"""Validaciones derivadas de las lecciones de V0."""

import re
import unicodedata

from agents.common.constants import MODEL_YEARS
from agents.common.vin import is_valid


def vin_flags(vin):
    """Marca VIN ausente, mal formado o con checksum invalido."""
    return [] if is_valid(vin) else ["vin_invalid"]


def salvage_flags(description):
    """Detecta lenguaje comun de salvamento y perdida total."""
    if not description:
        return []

    text = unicodedata.normalize("NFD", str(description).lower())
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    patterns = (
        r"\bsalvament\w*",
        r"\bperdida\s+total\b",
        r"\btitulo\s+de\s+recuperacion\b",
        r"\brehabilitad\w*",
        r"\breconstruid\w*",
        r"\btotal\s+loss\b",
        r"\bsalvage\b",
        r"\brebuilt\b",
        r"\breconstructed\b",
    )
    return ["salvage"] if any(re.search(pattern, text) for pattern in patterns) else []


def year_model_flags(make, model, year):
    """Marca anos fuera del rango conocido de la generacion del modelo."""
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
