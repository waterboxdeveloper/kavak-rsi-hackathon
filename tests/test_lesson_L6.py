"""Test de la leccion L6 -- generado por loop/learn.py.

Evidencia original: C010, C015, C025
Regla: Cruzar ano contra el rango de la generacion del modelo. Si es imposible, bandera 'year_model_mismatch'.

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.validators import year_model_flags


def test_l6_1():
    assert year_model_flags('Kia', 'Rio', 2011) == ['year_model_mismatch']

