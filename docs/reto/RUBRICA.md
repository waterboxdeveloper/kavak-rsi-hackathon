# Rúbrica oficial del RSI Hackathon

> **Material de la organización, transcrito literal.** No editar el contenido:
> es la vara con la que nos van a calificar. Las notas de nuestro proyecto van
> en el bloque del final, claramente separadas.

**Formato.** 3 minutos de demostración y 2 minutos de preguntas.

Construyan un sistema de agentes que aprenda de sus ejecuciones y use lo
aprendido para construir un sistema sucesor funcional. En la demo, muestren
qué cambió entre versiones y qué efecto tuvo ese cambio.

---

## 1. Impacto / 25 %

Expliquen quién se beneficiaría del sistema, qué problema resuelve y por qué
importa. Midan un resultado que tenga sentido para ese problema, como errores
por lote, casos resueltos o tiempo de revisión.

**Qué mostrar.** Comparen la versión inicial y la sucesora sobre los mismos
casos de evaluación. Si pueden, reserven casos que el sistema no haya visto al
aprender y expliquen qué sigue fallando.

## 2. Aplicación de Codex / 25 %

Cuenten cómo utilizaron Codex en su proyecto.

## 3. Uso creativo de habilidades / 25 %

Expliquen cómo diseñaron el ciclo de aprendizaje. Identifiquen qué señal
permitió detectar una falla, cómo se guardó la lección y cómo se incorporó al
construir el sucesor.

**Qué mostrar.** Enseñen una lección concreta que cambie el comportamiento del
sucesor. Puede quedar en una prueba, una herramienta, una regla o un cambio en
el flujo. Si el sucesor vuelve a aprender y crea otra versión, muestren qué se
acumuló.

## 4. Demostración y presentación / 25 %

Hagan fácil seguir la secuencia entre una falla, una decisión del sistema y el
resultado de la siguiente versión. Distingan las acciones del sistema de las
intervenciones del equipo.

**Qué mostrar.** Corran un caso representativo, enseñen el cambio que produjo
el sistema y hagan visible el antes y el después. Si usaron una base previa,
digan qué trajeron y qué construyeron durante el hackathon.

---
---

# ⬇️ Cómo responde NUESTRO proyecto a cada criterio

Esta parte sí es nuestra. Cada fila apunta al archivo que lo demuestra, para
que ninguna respuesta dependa de la memoria de quien presente.

## 1. Impacto — qué decimos

| La rúbrica pide | Nuestra respuesta | Evidencia |
|---|---|---|
| Quién se beneficia | Quien captura inventario en Kavak y quien compra el auto. Un anuncio mal capturado publica un auto de 265 mil pesos en 14 mil, o uno con 30 km que en realidad trae 30,000 | `docs/NUESTRA-PROPUESTA.md` |
| Qué problema resuelve | Anuncios escritos por personas → ficha de inventario confiable, con banderas de riesgo (salvamento, VIN inválido, año imposible) | `bench/cases.jsonl` |
| Resultado medido | **Casos resueltos** sobre un banco fijo, más 2 chequeos de integridad del lote | `runs/*.score.json` |
| Misma evaluación entre versiones | Mismo banco, semilla fija, mismo scorer | `bench/generate_cases.py` |
| **Casos que no vio al aprender** | **20 de 60 apartados.** El loop sólo ve los 40 de train | `bench/cases.jsonl` campo `split` |
| Qué sigue fallando | El reporte lo imprime solo en su última sección | `report.py` |

## 2. Aplicación de Codex — qué decimos

> *Codex no fue nuestro copiloto: fue el **órgano de construcción** del
> sistema. `loop/build.py` le entrega el código del predecesor y las lecciones
> que el sistema aprendió de sus propias corridas, y Codex escribe el sucesor
> completo con sus herramientas. V0 y el loop son nuestros; **V1 lo escribió
> Codex***.

Y el remate honesto, que vale más que la frase anterior:

> *En el primer intento Codex se pasó de listo: arregló además dos bugs de
> proceso cuya lección el sistema había diferido a propósito, y saltó a 20/20.
> Eso destruía la evidencia, porque una mejora sin lección no se puede
> atribuir ni apagar. Corregimos el contrato del constructor para prohibirle
> implementar nada que no tenga lección, y reconstruimos. **El hallazgo está
> en el historial de git.***

Evidencia a la mano: `runs/build-prompt-v0-to-v1.md` (el prompt exacto) y
`git log` (el primer intento quedó commiteado como evidencia).

## 3. Uso creativo de habilidades — qué decimos

| La rúbrica pide | Nuestra respuesta | Evidencia |
|---|---|---|
| Qué **señal** detectó la falla | Comparación campo a campo contra la respuesta conocida, agrupada por tipo de defecto con caso, campo, esperado y obtenido | `loop/observe.py` |
| Cómo se **guardó** la lección | Regla + función donde debe vivir + **un test generado que nace rojo** | `lessons/lessons.jsonl`, `tests/` |
| Cómo se **incorporó** | El prompt de construcción lleva cada lección con su id, y el sucesor debe envolver el comportamiento en `if "Lx" in lessons:` | `loop/build.py` |
| Una **lección concreta** | L5: millas → km. Vive en una función, en un test y en un interruptor | `tests/test_lesson_L5.py` |
| **Qué se acumuló** | 9 lecciones de V0; las 2 de proceso quedaron diferidas y nacen de V1 → 11 en V2 | `lessons/lessons.jsonl` |

**La parte creativa que hay que contar sí o sí:** el sistema **se negó a
aprender** las dos fallas de proceso mientras había 38 casos de ruido de
extracción, porque no se podía atribuir la causa. Eso es lo que genera la
cadena de versiones sin que nosotros la guionáramos.

## 4. Demostración y presentación — qué decimos

| La rúbrica pide | Dónde está |
|---|---|
| Secuencia falla → decisión → resultado | `docs/demo/guion-3min.md`, y el recorrido visual en `docs/demo/loop-visual.html` |
| **Distinguir sistema vs. equipo** | Cada fase tiene sección «Intervención humana». Los commits dicen quién escribió qué |
| Caso representativo | `USD $14,324` guardado como 14,324 pesos |
| Antes y después visible | `make report` |
| Qué trajimos vs. hoy | El repo nació hoy; sólo `intro.md` es previo | `docs/fases/FASE-00-setup.md` |

---

## Autoevaluación honesta

| Criterio | Cómo vamos | Hueco |
|---|---|---|
| 1 · Impacto | sólido: holdout real y «qué sigue fallando» automático | el banco es sintético |
| 2 · Codex | sólido: es el constructor, no el copiloto, y tenemos el hallazgo | — |
| 3 · Habilidades | sólido: lección → función → test → interruptor, más las diferidas | el repertorio de reglas es humano |
| 4 · Demo | pendiente de ensayar con cronómetro | V2 aún no existe |
