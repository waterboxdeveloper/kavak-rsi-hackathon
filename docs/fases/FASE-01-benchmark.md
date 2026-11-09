# FASE-01 — El banco de casos (la vara de medir)

| | |
|---|---|
| **Estado** | ✅ hecha |
| **Fecha** | 9 nov 2026 |
| **Archivos** | `bench/generate_cases.py`, `bench/cases.jsonl`, `bench/score.py` |

## Objetivo
60 casos con respuesta conocida y defectos inyectados a propósito, más un
scorer determinista. Congelado: no se vuelve a tocar.

## Por qué
Esta fase va **primero** aunque sea la menos vistosa. Toda la demo se apoya en
una frase: *"las mismas versiones, sobre los mismos casos, dan 5 → 16 → 19."*
Si el banco cambia a media competencia, esa frase no vale nada.

Tres decisiones dentro:

- **Semilla fija (`random.Random(7)`).** El banco de hoy es idéntico al de
  mañana. Reproducibilidad > variedad.
- **40 train / 20 holdout.** El loop aprende sólo de los 40. Los 20 son el
  número que presentamos. Sin esta separación estaríamos midiendo memoria.
- **Scoring campo a campo, cero juez-LLM.** Un LLM calificando vuelve el
  resultado opinable justo cuando el jurado pide rigor.

## Estructura de un caso

```json
{
  "id": "C002",
  "split": "train",
  "listing": "VENDO Volkswagen Jetta 2017 / 30k kms / $193,000 / credito disponible, acepto cambio / vin: ...",
  "expected": {"make":"Volkswagen","model":"Jetta","year":2017,
               "odometer_km":30000,"price_mxn":193000,"vin":"...","flags":[]},
  "defects": ["odo_k_suffix"]
}
```

El campo `defects` es el que hace posible la atribución quirúrgica: cuando una
lección entra, sabemos exactamente qué subconjunto debió moverse.

## Los 11 defectos inyectados

| Defecto | Casos | Cómo se ve en el anuncio | Nivel |
|---|---|---|---|
| `odo_k_suffix` | 8 | `30k kms` | campo |
| `odo_miles` | 8 | `71,458 mi` | campo |
| `odo_dot_sep` | 4 | `85.000 km` | campo |
| `price_usd` | 8 | `USD $14,324` | campo |
| `price_k_suffix` | 4 | `$93k` | campo |
| `price_dot_sep` | 4 | `$364.000 MXN` | campo |
| `vin_invalid_checksum` | 8 | VIN con dígito 9 corrupto | campo |
| `year_model_impossible` | 8 | `Honda City 2011` (la gen. empieza 2015) | campo |
| `salvage_wording` | 8 | "fue pérdida total, rehabilitado" | campo |
| `duplicate_vin` | 2 | el mismo VIN en dos anuncios | **proceso** |
| `write_interrupted` | 2 | la escritura al inventario falla la 1ª vez | **proceso** |
| *(limpios)* | 15 | sin defecto | — |

La columna **Nivel** es la clave de la narrativa: los defectos de *campo* se
arreglan en V1; los de *proceso* sólo se vuelven diagnosticables cuando el
ruido de extracción ya desapareció, y ésos producen V2.

## Comandos exactos
```bash
make bench
python3 bench/score.py runs/v0-all.json    # el scorer, ya con una corrida
```

## Resultado observado
```
escritos 60 casos en bench/cases.jsonl  (40 train / 20 holdout)
   15  (limpio)
    8  odo_k_suffix
    8  price_usd
    8  vin_invalid_checksum
    8  salvage_wording
    8  odo_miles
    8  year_model_impossible
    4  price_k_suffix
    4  odo_dot_sep
    4  price_dot_sep
    2  write_interrupted
    2  duplicate_vin
```

## Los 2 chequeos de integridad

Aparte del conteo de casos, el scorer evalúa el lote completo:

- `no_duplicate_inventory` — un VIN repetido no debe generar un alta nueva.
- `no_phantom_confirmation` — no se confirma nada que no quedó persistido.

Son binarios y a nivel lote, así que no se pueden "casi" pasar. V0 falla los
dos; V2 debe pasar los dos.

## Intervención humana
Toda. El banco lo diseñamos nosotros; es el instrumento de medición, no parte
del sistema que aprende.

## Qué aprendimos
El primer `naive_int` que escribimos fallaba incluso en `56,000 km`, lo que
dejaba a V0 en 0/20. Una línea base de cero no se puede mejorar de forma
legible: no hay contraste. Lo ajustamos para que V0 resuelva los 15 casos
limpios y falle sólo en los defectos. **Una línea base debe ser mala, no
inútil.**

## Siguiente
[FASE-02 — V0, el extractor ingenuo](FASE-02-v0-extractor.md).
