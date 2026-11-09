"""Test de la leccion L4 -- generado por loop/learn.py.

Evidencia original: C005, C012, C020
Regla: Detectar lenguaje de salvamento/perdida total/titulo de recuperacion y emitir bandera 'salvage'.

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.validators import salvage_flags


def test_l4_1():
    assert salvage_flags('fue perdida total, rehabilitado') == ['salvage']

