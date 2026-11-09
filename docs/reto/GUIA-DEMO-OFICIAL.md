# Guía oficial para la demostración

> **Material de la organización, transcrito literal.** Nuestro guion
> cronometrado, ya aterrizado a este proyecto, está en
> [`docs/demo/guion-3min.md`](../demo/guion-3min.md).

## Cómo mostrar el aprendizaje

Pueden usar cualquier problema que permita observar el ciclo completo. En tres
minutos, una falla bien explicada y una comparación clara alcanzan para que el
jurado siga el razonamiento.

### 0:00–0:40 / Corran la versión inicial

Presenten el problema en una frase. Corran el caso, señalen dónde se rompe y
digan qué resultado esperaban. Enseñen el registro, la salida o la prueba que
hace visible la falla.

### 0:40–1:45 / Enseñen qué aprendió y qué construyó

Abran la lección guardada y señalen qué parte del sucesor cambió por ella.
Muestren al sucesor haciendo su tarea. Si hubo intervención humana, cuenten en
qué punto ocurrió.

### 1:45–3:00 / Comparen resultados

Enseñen qué pasa al correr las versiones sobre los mismos casos de evaluación
y expliquen qué atribuyen a la lección. Cierren contando cómo utilizaron
Codex.

## Ejemplo / De pedidos a reembolsos

- **Versión inicial.** El agente de pedidos recibe dos veces el evento E-17 y
  crea dos registros. Detecta la repetición y guarda una regla de
  deduplicación por ID. Al volver a correr el mismo evento, la prueba revela
  si el duplicado quedó resuelto.
- **Primer sucesor.** El sistema usa esa regla para construir un agente de
  devoluciones. Ese sucesor evita duplicados, pero al interrumpirse una
  escritura descubre otra falla: confirmó una devolución que nunca quedó
  guardada.
- **Segundo sucesor.** El agente de devoluciones usa esa evidencia al
  construir un agente de reembolsos. Este conserva la deduplicación y confirma
  solo después de guardar. En un banco común de seis casos, las tres versiones
  resuelven 2, 4 y 6. Si desactivan una lección, vuelve la falla
  correspondiente.

## Para los 2 minutos de preguntas

Tengan a mano una ejecución, la lección que salió de ella y el cambio que el
sucesor heredó. El jurado puede preguntar cómo aislaron el efecto del cambio o
qué haría fallar la última versión.

---
---

# ⬇️ Cómo se traduce a NUESTRO proyecto

## El ejemplo oficial, lado a lado con el nuestro

La guía usa pedidos → devoluciones → reembolsos. Nosotros copiamos **el
patrón**, no el dominio — y nos tocaron las mismas dos fallas de proceso, lo
cual no es coincidencia: son los errores clásicos de cualquier sistema que
escribe en una base de datos.

| | Ejemplo oficial | Nuestro proyecto |
|---|---|---|
| Versión inicial | agente de pedidos duplica el evento E-17 | V0 lee `30k kms` como 30 km y `USD $14,324` como 14,324 pesos |
| Lección | deduplicación por ID | 9 lecciones: normalización de km y precio, checksum de VIN, salvamento, año imposible |
| Primer sucesor | agente de devoluciones | V1, escrito por Codex |
| Falla que aparece después | confirmó una devolución que nunca se guardó | **la misma**: confirmación fantasma, más VIN duplicado |
| Segundo sucesor | agente de reembolsos | V2: conserva todo y confirma sólo después de guardar |
| Banco común | 6 casos → 2, 4, 6 | **60 casos, 20 apartados** → 5/20 → … |
| Ablation | desactivan una lección y vuelve la falla | `make ablate L=L5 V=v2` → vuelven exactamente 8 casos |

**Dónde vamos más lejos que el ejemplo:** 60 casos en vez de 6, con 20
apartados que el loop nunca ve; scoring determinista campo a campo; y cada
lección fijada con un test generado que nace rojo.

## Los 3 artefactos de los 2 minutos de preguntas

La guía pide tener tres cosas a la mano. Las nuestras, con ruta exacta:

| Lo que piden | El nuestro |
|---|---|
| Una ejecución | `runs/v0-holdout.json` |
| La lección que salió de ella | `lessons/lessons.jsonl`, línea 1 (L1) |
| El cambio que el sucesor heredó | `git show` del commit de V1, más `tests/test_lesson_L1.py` en verde |

## Las dos preguntas que anuncian

**«¿Cómo aislaron el efecto del cambio?»**
> Mismo banco con semilla fija, mismo scorer, y 20 casos que el loop nunca
> vio. Además cada lección vive detrás de un interruptor: la apagamos en vivo
> y reaparecen exactamente los casos que arreglaba, ni uno más.

**«¿Qué haría fallar la última versión?»**
> Un anuncio sin VIN, dos monedas en el mismo texto, o un modelo fuera de
> nuestro catálogo de 8. No es especulación: el reporte lo imprime solo en su
> sección «Qué sigue fallando».

## Lo que la guía pide y es fácil olvidar

> *«Si hubo intervención humana, cuenten en qué punto ocurrió.»*

Nuestra respuesta tiene nombre y commit: **Codex se pasó de listo en el primer
intento** y arregló dos bugs cuya lección estaba diferida, saltando a 20/20.
Corregimos el contrato del constructor y reconstruimos. Decirlo sin que lo
pregunten nos hace ver más sólidos, no más débiles — y además es la respuesta
más interesante que vamos a dar.
