"""Normalizacion de kilometrajes derivada de L1, L5 y L8."""

import re

from agents.common.constants import MILES_TO_KM


def normalize_odometer(
    raw,
    *,
    handle_k=True,
    handle_miles=True,
    handle_dot=True,
):
    """Convierte un kilometraje crudo a kilometros.

    Los argumentos permiten que el agente active cada comportamiento de forma
    independiente durante una ablacion. Con los valores por defecto, la
    herramienta aplica las tres normalizaciones aprendidas.
    """
    if not raw:
        return None

    text = str(raw).strip().lower()
    match = re.search(r"[\d.,]+", text)
    if not match:
        return None

    number = match.group(0).replace(",", "")
    if handle_dot:
        number = number.replace(".", "")

    integer = re.match(r"\d+", number)
    if not integer:
        return None
    value = int(integer.group(0))

    if handle_k and re.search(r"(?<=\d)\s*k\b", text):
        value *= 1000

    if handle_miles and re.search(r"\b(?:mi|millas|miles)\b", text):
        value = round(value * MILES_TO_KM)

    return value
