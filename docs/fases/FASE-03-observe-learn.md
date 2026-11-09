# FASE-03 — Observar y aprender (el corazón del proyecto)

| | |
|---|---|
| **Estado** | ✅ hecha |
| **Fecha** | 9 nov 2026 |
| **Archivos** | `loop/observe.py`, `loop/learn.py`, `run_tests.py`, `lessons/lessons.jsonl`, `tests/` |
| **Commits** | `fbe5572` feat(loop) · `5674ff1` feat(lessons) |

## Objetivo
Que el sistema convierta sus propias fallas en **lecciones persistidas**, cada
una con su evidencia, su regla, el artefacto de código donde debe vivir y un
test que hoy está rojo.

## Por qué estas dos piezas son el proyecto

Todo lo demás es infraestructura. El criterio 3 de la rúbrica (25%) pregunta
exactamente tres cosas, y son estos dos scripts:

| La rúbrica pregunta | Dónde está la respuesta |
|---|---|
| ¿Qué **señal** permitió detectar la falla? | `loop/observe.py` |
| ¿Cómo se **guardó** la lección? | `lessons/lessons.jsonl` + `tests/` |
| ¿Cómo se **incorporó** al sucesor? | `loop/build.py` (FASE-04) |

---

## Paso 1 · `observe.py` — de "falló" a evidencia puntual

Agrupa las fallas por tipo de defecto y guarda hasta 3 ejemplos concretos de
cada uno, con el texto del anuncio, lo esperado y lo obtenido.

```bash
make observe     # python3 loop/observe.py runs/v0-train.json
```

```
== fallas observadas en v0 (train) ==

  [ 5 casos] odo_k_suffix  campos: flags, odometer_km, price_mxn
      C002: VENDO Volkswagen Jetta 2017 / 30k kms / $193,000 / credito dispon
      esperado {'odometer_km': 30000}  ->  obtenido {'odometer_km': 30}

  [ 5 casos] price_usd  campos: flags, odometer_km, price_mxn
      C003: 2020 Hyundai Grand i10 impecable, siempre en garage. Kilometraje
      esperado {'price_mxn': 264994}  ->  obtenido {'price_mxn': 14324}

  [ 5 casos] vin_invalid_checksum  campos: flags, price_mxn
      esperado {'flags': ['vin_invalid']}  ->  obtenido {'flags': []}
  ...
  [ 1 casos] write_interrupted  campos: integrity:no_phantom_confirmation
```

**Nota de diseño:** sólo observamos el split `train`. Los 20 casos `holdout`
jamás entran al loop. Si el sistema aprendiera de ellos, la mejora que
presentamos sería memoria disfrazada de aprendizaje.

---

## Paso 2 · `learn.py` — de evidencia a lección con candado

### Anatomía de una lección

```json
{
  "id": "L1",
  "defect": "odo_k_suffix",
  "trigger": "5 casos fallaron en flags, odometer_km, price_mxn",
  "evidence_run": "runs/v0-train.json",
  "evidence_cases": ["C002", "C012", "C017"],
  "rule": "El kilometraje puede venir con sufijo 'k' (56k = 56000). Normalizar antes de guardar.",
  "artifact": "agents/common/tools/odometer.py::normalize_odometer",
  "test": "tests/test_lesson_L1.py",
  "enabled": true,
  "learned_from": "v0",
  "inherited_by": []
}
```

Cuatro propiedades deliberadas:

1. **`evidence_cases` + `evidence_run`** — la lección es trazable a la corrida
   que la provocó. Sin esto es una opinión con formato JSON.
2. **`artifact`** — no basta "acuérdate de esto": la lección nombra la función
   que debe existir. Convierte un aprendizaje en una obligación de código.
3. **`test`** — el candado (abajo).
4. **`enabled`** — el interruptor del ablation.

### El test rojo: el mecanismo clave

Junto a cada lección, `learn.py` **genera** su test:

```python
"""Test de la leccion L1 -- generado por loop/learn.py.
Evidencia original: C002, C012, C017
Hoy este test esta ROJO. Se pone verde cuando el sucesor hereda la leccion.
"""
from agents.common.tools.odometer import normalize_odometer

def test_l1_1():
    assert normalize_odometer('56k kms') == 56000
def test_l1_2():
    assert normalize_odometer('120 k km') == 120000
```

Hoy truena: `agents/common/tools/odometer.py` no existe. Y eso es la medición
que queremos:

- 🔴 rojo = la lección describe algo que de verdad falta
- 🟢 verde = el sucesor la heredó

Un test es **una lección que se defiende sola para siempre**. Si en una
iteración futura alguien rompe la conversión de millas, el test grita. La
lección no depende de que nadie se acuerde.

Para las dos lecciones de proceso el test no es unitario: corre el agente
completo y exige el chequeo de integridad del lote
(`no_duplicate_inventory`, `no_phantom_confirmation`).

### Por qué hay un catálogo explícito en el código

`learn.py` tiene un `CATALOG` que mapea defecto observado → lección propuesta.
Es una decisión consciente y hay que poder defenderla:

- **Lo que el sistema decide solo:** *qué* defectos existen, *cuántos* casos
  afecta cada uno, *cuáles* son atribuibles ahora, *cuándo* hay suficiente
  evidencia, y qué test generar con qué casos.
- **Lo que pusimos nosotros:** el repertorio de reglas posibles.

La alternativa —dejar que el LLM invente la regla libremente— se ve más
impresionante en la demo y es peor en la práctica: reglas no reproducibles,
imposibles de auditar y que cambian entre corridas. Dejamos la puerta abierta
con `--llm`, que hace que el modelo **redacte** la regla a partir de la
evidencia, conservando el artefacto y el test deterministas.

> Para el jurado: *"¿quién decidió la lección?"* → la decisión es auditable,
> está en `loop/learn.py:CATALOG` y la atribución a casos concretos sale de la
> evidencia, no del modelo.

---

## Lo mejor de esta fase: las lecciones DIFERIDAS

```
== lecciones nuevas: 9 (acumuladas: 9) ==
  L1 [odo_k_suffix] · L2 [price_usd] · L3 [vin_invalid_checksum]
  L4 [salvage_wording] · L5 [odo_miles] · L6 [year_model_impossible]
  L7 [price_k_suffix] · L8 [odo_dot_sep] · L9 [price_dot_sep]

  DIFERIDA  [write_interrupted] -> es una falla de proceso y todavía hay
            38 casos con ruido de extracción.
            No se puede atribuir causa aún. Se aprende en la siguiente iteración.
  DIFERIDA  [duplicate_vin]     -> idem
```

El sistema **detectó** las dos fallas de proceso y **se negó a aprender de
ellas todavía**. La regla está en el código:

```python
# No aprendemos lecciones de PROCESO mientras siga habiendo ruido de
# extracción. Con 38 casos fallando, no se puede atribuir una falla de
# integridad a la lógica de proceso: podría ser efecto de un campo mal
# parseado. Primero se limpia la señal, luego se diagnostica.
```

Dos razones por las que esto vale mucho:

1. **Es metodología honesta.** Un confirmación-fantasma podría ser consecuencia
   de un campo mal parseado. Atribuir causa con ruido encima es cómo nacen las
   conclusiones falsas.
2. **Genera la cadena de versiones sin forzarla.** V1 limpia el ruido → las
   fallas de proceso quedan aisladas → nacen L10 y L11 → eso *justifica* V2.
   La escalera V0→V1→V2 no es un guion de demo: es consecuencia de la
   disciplina de diagnóstico.

---

## Verificaciones hechas en esta fase

| Qué verificamos | Cómo | Resultado |
|---|---|---|
| El banco es determinista | `generate_cases.py` 2× + `shasum` | hash idéntico `54b7651…` ✅ |
| `learn.py` es idempotente | correrlo 2× sobre las mismas fallas | `lecciones nuevas: 0` · no duplica ✅ |
| Los tests nacen rojos | `make test` | `0 verdes / 9 rojos` ✅ |
| El ablation no rompe nada | `run.py --ablate L5` | apaga L5, deja las otras 8 activas ✅ |

Nota: `pytest` no está instalado en esta máquina, así que escribimos
`run_tests.py` (stdlib, 0 dependencias) con salida ROJO/VERDE a color. Los
archivos de test siguen siendo compatibles con pytest si alguien lo instala.
En un hackathon, pelearse con `pip` en varias laptops es tiempo tirado.

## Evidencia citable en la demo
- `runs/v0-train.failures.json` — la señal agrupada
- `lessons/lessons.jsonl` — la memoria del sistema, 9 líneas
- `tests/test_lesson_L*.py` — los 9 candados, hoy rojos

## Intervención humana
El loop (observe/learn) lo escribimos nosotros, incluido el catálogo de reglas
posibles. **Las 9 lecciones y los 9 tests NO se escribieron a mano:** los
generó `learn.py` a partir de `runs/v0-train.failures.json`. Están versionados
en el commit `5674ff1` para que se pueda auditar.

## Siguiente
[FASE-04 — Codex construye V1](FASE-04-build-v1.md). Es el único paso que
falta correr y el que tiene riesgo real.
