"""Test de la leccion L5 -- generado por loop/learn.py.

Evidencia original: C006, C015, C021
Regla: Si la unidad es mi/millas, convertir a km con factor 1.60934 y redondear.

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.odometer import normalize_odometer


def test_l5_1():
    assert normalize_odometer('35,000 mi') == 56327

