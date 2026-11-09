# FASE-02 — V0, el extractor ingenuo (la línea base)

| | |
|---|---|
| **Estado** | ✅ hecha |
| **Fecha** | 9 nov 2026 |
| **Archivos** | `agents/v0/agent.py`, `agents/run.py`, `agents/common/engine.py`, `agents/common/store.py` |
| **Commit** | `2645c8c` feat(agents): V0 extractor ingenuo + runner con soporte de ablation |

## Objetivo
La primera versión del agente, **mala a propósito**, y su calificación en el
examen. Ése es el "antes" contra el que se compara todo.

## Por qué una versión mala es un entregable

Suena raro escribir código malo a propósito, así que vale explicarlo: V0 no es
un borrador que vamos a corregir. V0 es **el insumo del sistema**. Sus errores
son la materia prima de las lecciones. Si V0 fuera bueno, no habría nada que
aprender y no habría proyecto.

La regla de oro de V0 es "agarra el primer número que veas":

```python
def naive_int(raw):
    s = re.sub(r"(?<=\d),(?=\d{3})", "", str(raw))  # tolera "56,000"
    m = re.search(r"\d+", s)
    return int(m.group(0)) if m else None
```

Y trae un bug de proceso plantado a mano:

```python
store.confirm(case["id"])    # "listo, ya quedó"
try:
    store.save(record)       # ...y AHORA lo guardamos
except Exception:
    record["action"] = "failed"
```

Confirma antes de persistir. Si la escritura falla, el cliente ya recibió un
"listo" que es mentira. Nadie lo nota hasta que el sistema mire su propia
bitácora — que es justo lo que va a pasar en la FASE-05.

## Tres decisiones de diseño que importan

### 1. El contrato de interfaz, fijado desde V0

Toda versión (V0, V1, V2…) expone exactamente lo mismo:

```python
VERSION = "v0"
ingest(cases, store, engine, lessons) -> list[record]
```

Es lo que permite que el runner, el scorer y los tests sirvan igual para una
versión escrita a mano que para una escrita por Codex. **Sin contrato, cada
versión nueva obligaría a reescribir las herramientas de medición**, y ahí se
va la comparabilidad.

### 2. El parámetro `lessons` existe desde V0, aunque V0 no lo use

V0 recibe el conjunto de lecciones activas y lo ignora (no tiene ninguna).
Pero el parámetro ya está en la firma, así que V1 y V2 pueden envolver cada
comportamiento aprendido en `if "L5" in lessons:` sin cambiar el contrato.
**Eso es lo que hace posible el ablation** sin reconstruir el agente.

### 3. El motor devuelve valores *crudos*

`engine.py` entrega `odometer_raw: "30k kms"`, no `30000`. Normalizar es
trabajo del agente, no del motor. Así la falla vive en código que el sistema
puede reescribir.

Esto también cubre un riesgo real: si usáramos el LLM para extraer *y*
normalizar, el LLM probablemente acertaría `30k kms` solito y no tendríamos
fallas que estudiar. Al separar las dos responsabilidades, la falla queda
donde la queremos: en la capa de parseo determinista.

Hay dos motores intercambiables:
- `stub` (default): regex deterministas, sin red ni API key. Reproducible.
- `openai`: un LLM lee el anuncio. Mismo contrato, misma salida cruda.

## Comandos exactos
```bash
make v0
# equivale a:
python3 agents/run.py --version v0 --split all
python3 bench/score.py runs/v0-all.json
python3 agents/run.py --version v0 --split holdout
python3 bench/score.py runs/v0-holdout.json
```

## Resultado observado — LA LÍNEA BASE

```
== v0  (split=all) ==
  casos resueltos : 15/60
    train         : 10/40
    holdout       : 5/20     <- el número que presentamos
  integridad      : 0/2
    [FALLA] no_duplicate_inventory {'KFBF5KYM1J47ZTAM9': ['C003','C019'],
                                    '7JJHHPGG2VFBFF9JC': ['C043','C056']}
    [FALLA] no_phantom_confirmation ['C010', 'C051']

  por tipo de defecto:
      0/2    duplicate_vin
      0/4    odo_dot_sep
      0/8    odo_k_suffix
      0/8    odo_miles
      0/4    price_dot_sep
      0/4    price_k_suffix
      0/8    price_usd
      0/8    salvage_wording
      0/8    vin_invalid_checksum
      0/2    write_interrupted
      0/8    year_model_impossible
     15/15   (limpio)
```

Lectura: **resuelve el 100% de los casos limpios y el 0% de todos los
defectos.** Es la línea base ideal — el perfil de error es perfectamente
nítido, cada defecto es un objetivo separado y atribuible.

## Evidencia citable en la demo
- `runs/v0-holdout.json` — la traza completa (incluye la bitácora del store)
- `runs/v0-holdout.score.json` — la calificación desglosada

Para la demo, el caso estrella es `price_usd`: el anuncio dice `USD $14,324` y
V0 guarda **14,324 pesos** un auto de **265,000 pesos**. Eso se entiende en
tres segundos sin explicar nada técnico.

## Intervención humana
Toda. V0 y el runner los escribimos nosotros. A partir de la FASE-04 el código
de los agentes lo escribe el sistema.

## Qué salió mal / qué aprendimos
Mi primer `naive_int` tomaba el primer grupo de dígitos sin tolerar la coma de
miles, así que `"56,000 km"` daba 56 y V0 sacaba **0/20**. Lo ajusté para que
tolere la coma.

**Una línea base debe ser mala, no inútil.** Con 0/20 no hay contraste: no se
puede distinguir si la mejora vino de las lecciones o de que todo estaba roto.
El punto de partida tiene que fallar *selectivamente*.

## Siguiente
[FASE-03 — observar y aprender](FASE-03-observe-learn.md).
