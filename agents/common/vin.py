"""VIN: generacion y validacion del digito verificador (ISO 3779).

El digito 9 de un VIN es un checksum de los otros 16. Es una regla publica y
verificable, o sea: una falla *objetiva* que el sistema puede aprender a
detectar. Perfecta para el benchmark.
"""

ALPHABET = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"  # sin I, O, Q

TRANSLIT = {
    **{str(d): d for d in range(10)},
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
    "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
}

WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]


def check_digit(vin: str) -> str:
    """Calcula el digito verificador que *deberia* tener este VIN."""
    total = sum(TRANSLIT[c] * w for c, w in zip(vin.upper(), WEIGHTS))
    rem = total % 11
    return "X" if rem == 10 else str(rem)


def is_valid(vin: str) -> bool:
    """True si el VIN tiene 17 caracteres validos y el checksum cuadra."""
    if not vin or len(vin) != 17:
        return False
    vin = vin.upper()
    if any(c not in ALPHABET for c in vin):
        return False
    return vin[8] == check_digit(vin)


def with_valid_check_digit(vin16_plus: str) -> str:
    """Toma 17 caracteres y devuelve el VIN con el digito 9 corregido."""
    vin = vin16_plus.upper()
    return vin[:8] + check_digit(vin) + vin[9:]


def corrupt_check_digit(vin: str) -> str:
    """Rompe a proposito el checksum (para generar casos invalidos)."""
    good = vin[8]
    bad = "1" if good != "1" else "2"
    return vin[:8] + bad + vin[9:]
