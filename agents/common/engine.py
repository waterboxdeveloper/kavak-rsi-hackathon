"""Capa de extraccion: de texto libre a campos *crudos*.

Dos motores intercambiables:

  stub   -> regex deterministas. No necesita internet ni API key. Lo usamos
            para ensayar la demo sin gastar tokens y para que el benchmark sea
            100% reproducible.
  openai -> un LLM lee el anuncio y devuelve los campos tal como aparecen.

OJO (decision de diseno importante): el motor devuelve los valores *crudos*
("56k kms", "USD $13,500"). Normalizar es trabajo del agente, no del motor.
Asi la falla y la leccion viven en codigo que el sistema puede reescribir.
"""

import json
import os
import re

from .constants import MODELS


# ---------------------------------------------------------------------------
# Motor stub (determinista)
# ---------------------------------------------------------------------------
class StubEngine:
    name = "stub"

    def extract(self, listing: str) -> dict:
        make, model = self._find_model(listing)
        return {
            "make": make,
            "model": model,
            "year": self._first(r"\b(19|20)\d{2}\b", listing, group=0),
            "odometer_raw": self._span(r"[\d.,]+\s*(?:k\s*)?(?:kms?|mi|millas)\b", listing),
            "price_raw": self._span(r"(?:USD\s*)?\$\s*[\d.,]+\s*(?:k\b|mil\b|MXN\b|USD\b)?", listing),
            "vin": self._first(r"\b[A-HJ-NPR-Z0-9]{17}\b", listing, group=0),
            "description": listing,
        }

    @staticmethod
    def _find_model(listing: str):
        low = listing.lower()
        for mk, md, _ in MODELS:
            if md.lower() in low:
                return mk, md
        return None, None

    @staticmethod
    def _first(pattern, text, group=1):
        m = re.search(pattern, text, re.I)
        return m.group(group) if m else None

    @staticmethod
    def _span(pattern, text):
        m = re.search(pattern, text, re.I)
        return m.group(0).strip() if m else None


# ---------------------------------------------------------------------------
# Motor OpenAI
# ---------------------------------------------------------------------------
PROMPT = """Eres un extractor de datos de anuncios de autos usados.
Devuelve SOLO un JSON con estas llaves:
  make, model, year, odometer_raw, price_raw, vin, description

Reglas:
- odometer_raw y price_raw deben ir EXACTAMENTE como aparecen en el anuncio
  (no normalices, no convieras unidades ni monedas).
- year como entero. Si falta un dato, usa null.

Anuncio:
---
{listing}
---"""


class OpenAIEngine:
    name = "openai"

    def __init__(self, model="gpt-5"):
        from openai import OpenAI  # import diferido: solo si se usa

        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model

    def extract(self, listing: str) -> dict:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": PROMPT.format(listing=listing)}],
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        data["description"] = listing
        return data


def get_engine(name="stub"):
    if name == "stub":
        return StubEngine()
    if name == "openai":
        return OpenAIEngine()
    raise ValueError(f"motor desconocido: {name}")
