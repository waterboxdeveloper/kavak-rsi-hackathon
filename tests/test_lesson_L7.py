"""Test de la leccion L7 -- generado por loop/learn.py.

Evidencia original: C008, C023, C038
Regla: El precio puede venir con sufijo 'k' ($249k = 249000). Normalizar.

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.money import normalize_price_mxn


def test_l7_1():
    assert normalize_price_mxn('$249k') == 249000

