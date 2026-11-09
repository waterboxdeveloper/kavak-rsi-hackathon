"""Test de la leccion L8 -- generado por loop/learn.py.

Evidencia original: C009, C024, C039
Regla: El punto se usa como separador de miles en MX (56.000 km = 56000). Normalizar.

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.odometer import normalize_odometer


def test_l8_1():
    assert normalize_odometer('56.000 km') == 56000

