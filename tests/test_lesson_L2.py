"""Test de la leccion L2 -- generado por loop/learn.py.

Evidencia original: C003, C012, C018
Regla: Precios en USD deben convertirse a MXN con el tipo de cambio fijo del benchmark (18.50).

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.money import normalize_price_mxn


def test_l2_1():
    assert normalize_price_mxn('USD $13,500') == 249750

