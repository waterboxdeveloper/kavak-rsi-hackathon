# Registro de decisiones y su impacto

> Cada decisión grande del proyecto: qué se decidió, **qué impacta**, qué
> alternativa se descartó, y si se puede revertir. En orden cronológico.
>
> Para qué sirve esto: si el jurado pregunta *"¿por qué así?"* la respuesta
> está escrita, no improvisada. Y si una decisión resulta mala, aquí está el
> botón de regreso.

---

## D01 · Dominio: ingesta de anuncios de autos usados

**Qué:** el agente convierte texto libre de anuncios en ficha de inventario.

**Impacta:** es el negocio de Kavak y los jueces incluyen gente de Kavak →
puntúa en Impacto (25 %). Pero sobre todo: **existe respuesta correcta
verificable.** `30k kms` son 30,000 y punto, no es opinión.

**Alternativa descartada:** agente de soporte (más vistoso, scoring difuso) y
detección de fraude (impacto altísimo, imposible de medir en 10 horas).

**Reversible:** no a estas alturas. Todo el banco depende de esto.

---

## D02 · Datos sintéticos, con el defecto de cada caso etiquetado

**Qué:** generamos los 60 anuncios nosotros, y cada uno sabe qué defecto trae.

**Impacta:** es el superpoder del proyecto. Permite decir *"la lección L5
arregló exactamente estos 8 casos, ni uno más"*. Con datos reales eso sería
casi imposible de afirmar.

**Costo real:** es la crítica más justa que nos pueden hacer. Un anuncio real
es más sucio. **Hay que decirlo antes de que lo pregunten.**

**Alternativa descartada:** datos públicos scrapeados — sin respuesta conocida
no hay juez, y sin juez no hay loop.

**Reversible:** sí, cambiando `bench/`. El resto del sistema no se entera.

---

## D03 · El benchmark primero, antes de escribir el agente

**Qué:** la FASE-01 fue el examen, no el código.

**Impacta:** toda la demo se apoya en *"las mismas versiones, sobre los mismos
casos"*. Si el banco se mueve a media competencia, esa frase no vale nada.

**Alternativa descartada:** empezar por el agente (más divertido) y medir
después. Es cómo se arruinan estos proyectos: acabas ajustando el examen para
que el resultado se vea bien.

**Reversible:** no. Es la vara de medir.

---

## D04 · 40 casos para aprender, 20 apartados para calificar

**Qué:** el loop sólo ve los 40 de `train`. Los 20 de `holdout` nunca entran.

**Impacta:** **es el número que presentamos.** Sin esta separación estaríamos
midiendo memoria y no aprendizaje, y lo peor es que no nos daríamos cuenta.
La rúbrica lo pide textual: *"reserven casos que el sistema no haya visto"*.

**Costo:** la línea base se ve peor (5/20 en vez de 15/60). Vale la pena.

**Reversible:** sí, pero hacerlo invalidaría toda comparación previa.

---

## D05 · Scoring determinista, cero juez-LLM

**Qué:** `bench/score.py` compara campo a campo. Ningún LLM califica.

**Impacta:** el número es indiscutible frente al jurado. Un LLM calificando
vuelve el resultado opinable justo cuando piden rigor — y además no es
reproducible entre corridas.

**Costo:** sólo podemos medir cosas con respuesta exacta. Nada de "¿quedó
bien redactado?".

**Reversible:** sí, pero sería un retroceso.

---

## D06 · Python stdlib, cero dependencias en el camino crítico

**Qué:** nada de `pip install` para correr la demo. `openai` y `pytest` son
opcionales y de hecho no están instalados.

**Impacta:** en un hackathon de 10 horas, pelearse con `pip` en 4 laptops
distintas es tiempo tirado. Hoy nos salvó: no hubo un solo problema de
entorno. Por eso escribimos `run_tests.py` en vez de usar pytest.

**Reversible:** sí, trivialmente.

---

## D07 · El motor de extracción devuelve valores CRUDOS

**Qué:** `engine.py` entrega `"30k kms"`, no `30000`. Normalizar es trabajo
del agente.

**Impacta:** dos cosas. **(a)** La falla vive en código que el sistema puede
reescribir, no dentro del modelo. **(b)** Cubre un riesgo real: si el LLM
extrajera *y* normalizara, probablemente acertaría `30k kms` solito y no
tendríamos fallas que estudiar — el proyecto se quedaría sin combustible.

**Alternativa descartada:** pedirle al LLM la ficha ya normalizada.

**Reversible:** sí, pero rompería la narrativa.

---

## D08 · V0 es malo a propósito, con un bug de proceso plantado

**Qué:** V0 agarra el primer número que ve, y confirma el alta **antes** de
guardarla.

**Impacta:** V0 no es un borrador a corregir, es **el insumo**. Sus errores
son la materia prima de las lecciones. El bug de proceso plantado es el que
más adelante origina V2.

**Ajuste que tuvimos que hacer:** la primera versión fallaba hasta en los
casos limpios → 0/20. **Una línea base debe ser mala, no inútil:** con 0/20 no
hay contraste y no se puede atribuir la mejora. Lo ajustamos para que resuelva
los 15 limpios y falle sólo en los defectos.

**Reversible:** sí, pero no se toca. `agents/v0/` está en la lista de lo que
el constructor no puede modificar.

---

## D09 · Contrato de interfaz fijado desde V0, con `lessons` en la firma

**Qué:** toda versión expone `ingest(cases, store, engine, lessons)`. V0
recibe `lessons` y lo ignora.

**Impacta:** **es lo que hace posible el ablation.** Si el parámetro no
existiera desde el principio, cada versión nueva obligaría a cambiar el
runner, el scorer y los tests — y ahí se va la comparabilidad.

**Reversible:** no sin reescribir todo.

---

## D10 · Una lección tiene 4 partes, y una es un test que nace rojo

**Qué:** evidencia + regla + artefacto de código + test generado.

**Impacta:** es el mecanismo central. 🔴 rojo = la lección describe algo que
de verdad falta. 🟢 verde = el sucesor la heredó. **Un test es una lección que
se defiende sola para siempre**, y es la respuesta directa a *"¿cómo aislaron
el efecto?"*.

**Alternativa descartada:** guardar la lección como prosa. Se olvida, no se
puede verificar y no impide la regresión.

**Reversible:** no. Es el corazón.

---

## D11 · El repertorio de reglas lo escribimos nosotros (`learn.py:CATALOG`)

**Qué:** el sistema decide *qué* falló, *cuántos* casos, *cuál* lección
aplica y *cuándo* hay evidencia suficiente. El menú de reglas posibles es
humano.

**Impacta:** reglas auditables y reproducibles. La alternativa —LLM inventando
la regla libre— se ve más impresionante en la demo y es peor: cambia entre
corridas y no se puede auditar.

**Hay que declararlo:** está escrito en `docs/fases/FASE-03` y en
`NUESTRA-PROPUESTA.md` como límite. Dejamos la puerta abierta con `--llm`,
que hace que el modelo **redacte** la regla conservando el test determinista.

**Reversible:** sí, con `--llm`.

---

## D12 · Disciplina de etapas: diferir las lecciones de proceso

**Qué:** no se aprenden lecciones de proceso mientras haya ruido de
extracción. El sistema lo imprime: *"todavía hay 38 casos con ruido, no se
puede atribuir causa aún"*.

**Impacta:** es lo mejor del proyecto, por dos razones. **(a)** Es metodología
honesta: una confirmación fantasma podría ser *consecuencia* de un campo mal
parseado. **(b)** **Genera la cadena V0→V1→V2 sin guionarla.** La escalera no
es un truco de demo: es consecuencia de la disciplina de diagnóstico.

**Reversible:** sí, es una función de 3 líneas (`stage_of`). Pero quitarla
colapsaría la narrativa a una sola iteración.

---

## D13 · Codex es el constructor DENTRO del loop, no el copiloto

**Qué:** `loop/build.py` invoca `codex exec` con el predecesor + las
lecciones, y Codex escribe el sucesor completo.

**Impacta:** es el 25 % de «Aplicación de Codex». Casi todos van a decir
"usamos Codex para programar más rápido" — esa respuesta vale la mitad.

**Decisión extra:** lo dejamos **intercambiable** (`--builder claude`). Son 3
líneas de acoplamiento. Demuestra que el valor está en el banco, la evidencia
y los tests, no en el CLI.

**Reversible:** sí, un flag.

---

## D14 · Cada comportamiento aprendido va detrás de `if "Lx" in lessons:`

**Qué:** el constructor está obligado a envolver cada lección en su guarda.

**Impacta:** **es el cierre de la demo.** Apagas una lección, vuelven
exactamente los casos que arreglaba. Sin esto, "subimos de 5 a 19" es
anécdota; con esto es una afirmación causal defendible.

**Reversible:** no sin perder el ablation.

---

## D15 · `make test` ya no aborta cuando los tests están rojos

**Qué:** el target imprime una explicación y sale con 0.

**Impacta:** usabilidad pura, pero costó confusión real. `make: *** [test]
Error 1` parecía proyecto roto cuando era **la medición correcta**. Agregamos
también `make doctor` (diagnóstico de entorno) y `make reset` (volver al
punto cero para ensayar la demo).

**Reversible:** sí, irrelevante.

---

## D16 · Tiramos el primer V1 aunque sacó 20/20

**Qué:** Codex escribió un V1 que sacó **holdout 20/20, integridad 2/2, 9/9
tests verdes** — porque además implementó el dedupe por VIN y el
confirm-after-save, o sea las lecciones L10 y L11 **que estaban diferidas y no
venían en el prompt**.

**Por qué eso es malo aunque el número sea mejor:**

| Consecuencia | Gravedad |
|---|---|
| No queda nada que V2 pueda aprender | se cae la cadena y con ella el criterio de acumulación |
| Esos 2 comportamientos no tienen interruptor | no se pueden apagar ni atribuir → mejora sin evidencia |
| Salto de 5/20 a 20/20 en un paso | frente a un jurado técnico eso genera sospecha, no aplauso |

**Causa raíz, y fue nuestra:** el prompt prohibía tocar la vara de medir pero
nunca dijo *"no implementes nada que no tenga lección"*. Codex incluso avisó
que no lo haría, y lo hizo.

**Qué hicimos:**
1. El V1 pasado de listo quedó **commiteado como evidencia** (`68b99b3`).
2. Agregamos la sección **FRONTERA** al contrato del constructor.
3. Reconstruimos.

**Qué ganamos además del número:** la mejor respuesta a *"¿cómo distinguen las
acciones del sistema de las del equipo?"* — una intervención humana real,
documentada, con commit.

**Reversible:** sí. `git checkout 68b99b3 -- agents/v1 agents/common/tools`
recupera el 20/20 si se prefiere la historia de 2 versiones.

**Lo que sigue siendo decisión del equipo:** 3 versiones con 5→16→19 (fiel a
la rúbrica, muestra acumulación) vs. 2 versiones con 5→20 (más limpia, menos
profunda). Recomendación: la primera.
