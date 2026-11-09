"""Test de la leccion L9 -- generado por loop/learn.py.

Evidencia original: C014, C029
Regla: El punto como separador de miles tambien aplica al precio ($249.000 MXN = 249000).

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.money import normalize_price_mxn


def test_l9_1():
    assert normalize_price_mxn('$249.000 MXN') == 249000

