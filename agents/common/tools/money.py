"""Normalizacion determinista de precios derivada de L2, L7 y L9."""

import re

from agents.common.constants import USD_MXN


def normalize_price_mxn(
    raw,
    *,
    convert_usd=True,
    handle_k=True,
    handle_dot=True,
):
    """Convierte un precio crudo a MXN.

    ``handle_dot`` trata el punto como separador de miles; las comas ya son
    soportadas por el comportamiento ingenuo de V0.
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

    if handle_k and re.search(r"(?<=\d)\s*k\b|\bmil\b", text):
        value *= 1000

    if convert_usd and re.search(r"\busd\b", text):
        value = round(value * USD_MXN)

    return value
