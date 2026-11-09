"""Normalizacion determinista de precios a pesos mexicanos."""

import re

from agents.common.constants import USD_MXN


_ALL_LESSONS = frozenset(("L2", "L7", "L9"))


def normalize_price_mxn(raw, lessons=None):
    """Devuelve el precio normalizado a MXN, respetando las lecciones activas."""
    if not raw:
        return None

    if lessons is None:
        lessons = _ALL_LESSONS

    text = str(raw).strip().lower()
    number_match = re.search(r"[\d.,]+", text)
    if not number_match:
        return None

    original_number = number_match.group(0)
    number = original_number.replace(",", "")

    # L9: el punto es separador de miles en precios MXN.
    if "L9" in lessons and re.fullmatch(r"\d{1,3}(?:\.\d{3})+", original_number):
        number = original_number.replace(".", "").replace(",", "")

    # Sin L9, conserva la lectura ingenua de V0 para puntos.
    integer_match = re.match(r"\d+", number)
    if not integer_match:
        return None
    value = int(integer_match.group(0))

    if "L7" in lessons and re.search(r"(?:\bk\b|(?<=\d)k\b)", text):
        value *= 1000

    if "L2" in lessons and re.search(r"\busd\b", text):
        value = round(value * USD_MXN)

    return value
