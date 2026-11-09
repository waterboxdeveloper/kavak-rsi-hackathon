"""Test de la leccion L3 -- generado por loop/learn.py.

Evidencia original: C004, C014, C019
Regla: Validar el digito verificador del VIN (ISO 3779). Si no cuadra, emitir bandera 'vin_invalid'.

Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from agents.common.tools.validators import vin_flags


def test_l3_1():
    assert vin_flags('3VWA11AA1AA000001') == ['vin_invalid']

