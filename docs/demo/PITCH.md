# El pitch — 3 minutos, palabra por palabra

> La tesis que lo sostiene todo, y que hay que decir en la primera frase:
>
> ## 🔑 Un sistema que pasa todo en verde a la primera no tiene nada que enseñarte.
>
> No porque esté mal hecho. Porque un sistema sin fallas **no sabe qué
> mejorar**. Las fallas no son el accidente del proyecto: son la materia
> prima. Y la prueba de que lo creemos es que hoy **tiramos a la basura una
> versión que sacó 20 de 20.**

**Dos personas:** quien habla y quien teclea. Los comandos pre-escritos en un
archivo, se copian y se pegan. Nadie teclea en vivo bajo presión.

---

## 0:00 – 0:25 · El gancho

> «Les voy a decir algo que suena al revés.
>
> Si un sistema de IA pasa todas sus pruebas en verde a la primera, no sirve
> de mucho. No porque esté mal hecho: porque **no tiene nada que enseñarte.**
> Un sistema sin fallas no puede mejorar, no sabe qué mejorar.
>
> Hoy construimos uno que trata sus propios errores como materia prima. Y para
> que vean que lo decimos en serio: **tiramos a la basura una versión que sacó
> veinte de veinte.** Al final les cuento por qué.»

🖥️ **Pantalla:** el diagrama del ciclo (página del loop, paso 1).

---

## 0:25 – 0:50 · El problema y la falla

**Teclear:** `make v0`

> «Kavak recibe anuncios de autos escritos por personas. Alguien tiene que
> convertirlos en inventario confiable.
>
> Este anuncio dice **USD $14,324**. Nuestro primer agente lo guardó como
> catorce mil trescientos veinticuatro **pesos**… un auto de doscientos
> sesenta y cinco mil. Y aquí, **30k kms**: registró un Jetta con treinta
> kilómetros.
>
> **Cinco de veinte casos.** Ésa es nuestra línea base, y es mala a propósito.»

🖥️ **Señalar:** `holdout 5/20` · `integridad 0/2`

---

## 0:50 – 1:40 · Qué aprendió, y cuándo se negó a aprender

**Teclear:** `make observe` y luego `make learn`

> «El sistema no dice "falló". Dice **qué campo, en qué casos, qué esperaba y
> qué obtuvo**. De ahí escribió nueve lecciones. Cada una trae la regla, la
> función donde debe vivir, y **un test que nace rojo.**»

**Teclear:** `make test` → 9 rojos

> «Nueve tests en rojo. El sistema sabe nueve cosas y ninguna está
> implementada todavía.
>
> Pero miren esto, que es mi parte favorita. **También detectó dos fallas más
> graves**: que daba de alta el mismo auto dos veces, y que le decía "listo" al
> cliente por un alta que nunca se guardó.
>
> **Y se negó a aprenderlas.** Su razón, textual: *"todavía hay treinta y ocho
> casos con ruido de extracción, no se puede atribuir causa aún"*. Primero
> limpia la señal, después diagnostica. Eso no se lo programamos como frase:
> es una regla del loop.»

🖥️ **Señalar:** las dos líneas `DIFERIDA` en la salida.

---

## 1:40 – 2:20 · Codex construye, y la confesión

**Teclear:** `make build` (o enseñar el resultado ya hecho) y `make test`

> «Codex recibió el código del predecesor, las nueve lecciones y los nueve
> tests rojos, y escribió el sucesor completo con sus herramientas. Los nueve
> tests se pusieron verdes. **Diecinueve de veinte.**
>
> Y aquí va la confesión que les prometí.
>
> El **primer** V1 que Codex escribió sacó **veinte de veinte, integridad
> perfecta**. Lo tiramos. Porque arregló además los dos bugs cuya lección
> estaba diferida, y **una mejora sin lección que la respalde no se puede
> apagar ni atribuir**: es un número bonito sin evidencia detrás.
>
> Endurecimos el contrato del constructor para prohibirle implementar nada que
> no tenga lección, y reconstruimos. **Las dos versiones están en el git
> log.** Ésa fue nuestra intervención humana, y ocurrió exactamente ahí.»

🖥️ **Pantalla:** `git log --oneline` con los dos commits de V1.

---

## 2:20 – 3:00 · Acumulación y la prueba

**Teclear:** `make report`

> «Sin el ruido de extracción, las dos fallas de proceso quedaron aisladas y
> nacieron dos lecciones nuevas. V2 hereda once.
>
> **V2 no lee mejor que V1: trabaja mejor.** Ahí está el salto de integridad,
> de cero a dos. Dejó de duplicar autos y dejó de mentirle al cliente.»

**Teclear:** `make ablate L=L5 V=v1`

> «Y la prueba de que esto no fue suerte. Apago **una sola** lección, la de
> millas a kilómetros. El marcador baja de diecinueve a dieciséis. **Caen tres
> casos: C045, C051 y C060.** Son exactamente los tres casos con defecto de
> millas del banco. **Ni uno más.**
>
> Por eso podemos decir que la mejora vino de la lección, y no de la suerte.
>
> Y sobre Codex: no fue nuestro copiloto, fue el **órgano de construcción**
> del sistema. Nosotros escribimos el examen y el loop. **V1 y V2 los escribió
> Codex**, y los prompts están guardados.»

---
---

## ⚠️ Si V2 no se alcanza a construir

Sustituir el bloque de 2:20 por esto. **No inventar números de V2.**

> «V1 todavía tiene los dos bugs de proceso vivos, y eso es correcto: sus
> lecciones están diferidas esperando esta segunda vuelta. El único caso que
> V1 no resuelve es precisamente el del VIN duplicado. **Lo que falta es
> exactamente lo que el sistema ya identificó como su siguiente lección**, y
> eso es lo que nos interesaba mostrar: el loop no se quedó sin trabajo, se
> quedó con una tarea nombrada.»

Es una versión honesta y sigue siendo fuerte: enseña que el sistema **sabe lo
que no sabe**.

---

## Números reales, para no equivocarse en vivo

| | V0 | V1 | V2 |
|---|---|---|---|
| Casos resueltos (holdout, 20) | **5/20** ✅medido | **19/20** ✅medido | pendiente |
| Integridad | 0/2 | 0/2 | pendiente |
| Lecciones activas | 0 | 9 | 11 |
| Tests de lección verdes | 0/9 | **9/9** ✅medido | pendiente |

| Ablation (medido en V1) | |
|---|---|
| V1 completa | 19/20 |
| V1 sin L5 | 16/20 |
| Casos que caen | C045, C051, C060 |
| Casos con `odo_miles` en holdout | C045, C051, C060 → **coinciden exacto** |

---

## Las 4 frases que tienen que salir sí o sí

Si el tiempo se va, se sacrifica cualquier cosa menos éstas:

1. **«Un sistema que pasa todo en verde no tiene nada que enseñarte.»**
2. **«Se negó a aprender dos fallas porque todavía no podía atribuir la causa.»**
3. **«Tiramos un 20/20 porque era un número sin evidencia detrás.»**
4. **«Apago una lección y caen exactamente los tres casos que arreglaba.»**

## Para los 2 minutos de preguntas

| Pregunta | Respuesta |
|---|---|
| ¿Cómo aislaron el efecto? | Banco fijo con semilla, 20 casos que el loop nunca vio, y cada lección detrás de un interruptor que apagamos en vivo |
| ¿Qué haría fallar a la última versión? | Anuncio sin VIN, dos monedas en el mismo texto, modelo fuera de nuestro catálogo de 8. El reporte lo imprime solo |
| ¿Quién decidió la lección? | El repertorio de reglas es nuestro; el sistema elige cuál aplica, a qué casos y **cuándo hay evidencia suficiente** |
| ¿Dónde hubo intervención humana? | En un punto exacto: endurecer el contrato del constructor tras el V1 que se pasó de listo. Está en el git log |
| ¿Qué trajeron y qué hicieron hoy? | El repo nació hoy. Sólo `intro.md` es previo |

---
---

# 🎙️ MODO ENSAYO

## Primero: el guion de arriba NO cabe en 3 minutos

Lo conté. A ritmo de demo (≈140 palabras por minuto en español) el guion
completo da **488 palabras ≈ 3:28**, más el tiempo que tardan los comandos en
correr. Nos pasamos entre 30 y 40 segundos, y a los 3:00 cortan.

Así que abajo está la **versión apretada**: las mismas ideas, 180 segundos
contados. Úsenla para ensayar; la de arriba sirve para entender el contenido.

| Bloque | Palabras | Hablado | + comando | Total |
|---|---|---|---|---|
| 1 · Gancho | 68 | 0:29 | — | **0:29** |
| 2 · La falla | 50 | 0:22 | 0:06 | **0:28** |
| 3 · Aprende y se niega | 88 | 0:38 | 0:08 | **0:46** |
| 4 · La confesión | 78 | 0:34 | — | **0:34** |
| 5 · La prueba | 80 | 0:35 | 0:08 | **0:43** |
| | **364** | | | **3:00** |

Está al límite. Dos reglas: **nadie improvisa frases nuevas**, y **quien
teclea lanza el comando mientras el otro sigue hablando** (no esperar en
silencio a que termine de correr).

---

## 🃏 Tarjetas · sólo lo que se dice

### Tarjeta 1 — Gancho · 0:29
🖥️ *diagrama del ciclo, paso 1*

> Les voy a decir algo que suena al revés: si un sistema de IA pasa todas sus
> pruebas en verde a la primera, **no tiene nada que enseñarte**. No sabe qué
> mejorar.
>
> Hoy construimos uno que trata sus propios errores como materia prima. Y para
> que vean que lo decimos en serio: **tiramos a la basura una versión que sacó
> veinte de veinte.** Al final les digo por qué.

### Tarjeta 2 — La falla · 0:28
⌨️ `make v0` *(lanzarlo al empezar a hablar)*

> Kavak recibe anuncios escritos por personas. Este dice **USD catorce mil
> trescientos**. Nuestro agente lo guardó como catorce mil **pesos**: un auto
> de doscientos sesenta y cinco mil.
>
> Y aquí, **treinta k kilómetros** — registró un Jetta con treinta kilómetros.
>
> **Cinco de veinte.** Línea base, mala a propósito.

### Tarjeta 3 — Aprende, y se niega · 0:46
⌨️ `make observe` → `make learn` → `make test`

> El sistema no dice "falló": dice **qué campo, en qué casos, qué esperaba y
> qué obtuvo**. Escribió nueve lecciones, cada una con su regla, su función, y
> **un test que nace rojo**.
>
> Y miren esto. También detectó dos fallas más graves: daba de alta el mismo
> auto dos veces, y le decía "listo" al cliente por algo que nunca se guardó.
>
> **Y se negó a aprenderlas.** Textual: *"todavía hay treinta y ocho casos con
> ruido, no se puede atribuir causa aún"*. Primero limpia, después diagnostica.

### Tarjeta 4 — La confesión · 0:34
🖥️ `git log --oneline` *(ya en pantalla, no teclear)*

> Codex recibió el código viejo, las nueve lecciones y los nueve tests rojos, y
> escribió el sucesor completo. Nueve verdes. **Diecinueve de veinte.**
>
> Y la confesión: el **primer** V1 que escribió sacó **veinte de veinte**,
> perfecto. **Lo tiramos.** Arregló además dos bugs cuya lección estaba
> diferida — y una mejora sin lección **no se puede apagar ni atribuir**.
>
> Endurecimos su contrato y reconstruimos. Está en el git log: **ésa fue
> nuestra intervención humana.**

### Tarjeta 5 — La prueba · 0:43
⌨️ `make report` → `make ablate L=L5 V=v1`

> V2 hereda once lecciones. **No lee mejor: trabaja mejor** — dejó de duplicar
> autos y de mentirle al cliente.
>
> Y la prueba: apago **una sola** lección, la de millas a kilómetros. Baja de
> diecinueve a dieciséis. **Caen tres casos: C045, C051, C060.** Son
> exactamente los tres de millas del banco. **Ni uno más.**
>
> Codex no fue nuestro copiloto: fue el **órgano de construcción**. Nosotros
> escribimos el examen y el loop; **V1 y V2 los escribió él.**

---

## Bitácora de ensayos — llenar a mano

Tres ensayos mínimo, con cronómetro. Si el tercero no baja de 3:00, se recorta
la tarjeta 3 (es la más larga y la más fácil de apretar).

| # | Tiempo total | Dónde se fue el tiempo | Qué frase se trabó | Ajuste |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## Reparto

| | Quién | Hace |
|---|---|---|
| Voz | | habla las 5 tarjetas, nunca teclea |
| Manos | | copia y pega los comandos, nunca habla |

## Checklist de 2 minutos antes

- [ ] `make doctor` sin nada en rojo
- [ ] `make clean && make demo` corre completo
- [ ] Comandos pegados en un archivo de texto, listos para copiar
- [ ] Terminal con letra grande, **una** ventana, sin pestañas de más
- [ ] Pestañas ya abiertas: `lessons/lessons.jsonl`, `tests/test_lesson_L5.py`,
      `runs/build-prompt-v0-to-v1.md`, `git log --oneline`
- [ ] Decidido quién es Voz y quién es Manos
- [ ] Las 4 frases que no se sacrifican, memorizadas

## Si algo truena en vivo

No se depura. Se abre el score guardado en `runs/evidencia/`, se dice *"aquí
está la corrida de hace un rato"* y se sigue. **Nunca** se pierde el tiempo
arreglando algo frente al jurado.
