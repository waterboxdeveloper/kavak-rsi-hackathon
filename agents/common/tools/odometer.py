"""Normalizacion determinista de kilometrajes de anuncios."""

import re

from agents.common.constants import MILES_TO_KM


_ALL_LESSONS = frozenset(("L1", "L5", "L8"))


def normalize_odometer(raw, lessons=None):
    """Devuelve el kilometraje normalizado a kilometros.

    ``lessons`` es opcional para que los tests unitarios de cada artefacto
    puedan ejercitar la herramienta directamente. El agente siempre lo pasa
    explicitamente para que la ablacion funcione.
    """
    if not raw:
        return None

    if lessons is None:
        lessons = _ALL_LESSONS

    text = str(raw).strip().lower()
    number_match = re.search(r"[\d.,]+", text)
    if not number_match:
        return None

    number = number_match.group(0)

    # La coma ya era un separador soportado por V0.
    number = number.replace(",", "")

    # L8: en este dominio un punto entre grupos de tres digitos separa miles.
    if "L8" in lessons and re.fullmatch(r"\d{1,3}(?:\.\d{3})+", number_match.group(0)):
        number = number_match.group(0).replace(".", "").replace(",", "")

    # Sin L8, conserva la semantica ingenua de V0: toma el primer entero.
    integer_match = re.match(r"\d+", number)
    if not integer_match:
        return None
    value = int(integer_match.group(0))

    if "L1" in lessons and re.search(r"(?:\bk\b|(?<=\d)k\b)", text):
        value *= 1000

    if "L5" in lessons and re.search(r"\b(?:mi|millas|miles)\b", text):
        value = round(value * MILES_TO_KM)

    return value
