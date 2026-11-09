"""Test de la leccion L1 -- generado por loop/learn.py.

Evidencia original: C002, C012, C017
Regla: El kilometraje puede venir con sufijo 'k' (56k = 56000). Normalizar antes de guardar.

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.odometer import normalize_odometer


def test_l1_1():
    assert normalize_odometer('56k kms') == 56000

def test_l1_2():
    assert normalize_odometer('120 k km') == 120000

