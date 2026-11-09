"""Inventario simulado: la "base de datos" donde el agente da de alta autos.

Incluye un modo de falla a proposito (`crash_ids`): la escritura se interrumpe
la primera vez. Sirve para que el sistema descubra solo que estaba
*confirmando antes de persistir* -- la falla de proceso que origina V2.
"""


class StoreCrash(RuntimeError):
    """La escritura se interrumpio (simula un timeout / caida de red)."""


class InventoryStore:
    def __init__(self, crash_ids=()):
        self.crash_ids = set(crash_ids)
        self._crashed_once = set()
        self.rows = []            # altas persistidas de verdad
        self.confirmations = []   # confirmaciones emitidas al usuario
        self.log = []             # bitacora cronologica de todo

    # --- escritura ---------------------------------------------------------
    def save(self, record):
        case_id = record.get("case_id")
        if case_id in self.crash_ids and case_id not in self._crashed_once:
            self._crashed_once.add(case_id)
            self.log.append({"event": "save_failed", "case_id": case_id})
            raise StoreCrash(f"escritura interrumpida para {case_id}")
        self.rows.append(record)
        self.log.append({"event": "saved", "case_id": case_id, "vin": record.get("vin")})
        return True

    def confirm(self, case_id, message="alta confirmada"):
        self.confirmations.append({"case_id": case_id, "message": message})
        self.log.append({"event": "confirmed", "case_id": case_id})

    # --- lectura -----------------------------------------------------------
    def find_by_vin(self, vin):
        return [r for r in self.rows if r.get("vin") == vin]

    def snapshot(self):
        return {
            "rows": self.rows,
            "confirmations": self.confirmations,
            "log": self.log,
        }
