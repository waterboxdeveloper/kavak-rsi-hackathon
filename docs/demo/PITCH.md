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

## 2:20 – 3:00 · La prueba, y la tarea que queda nombrada

**Teclear:** `make report`

> "De cinco a diecinueve de veinte, sobre los mismos veinte casos que el
> sistema nunca vio al aprender.
>
> Y fíjense en el único que **no** resuelve: el del VIN duplicado. Es
> precisamente una de las dos lecciones que el sistema decidió diferir.
> **El loop no se quedó sin trabajo: se quedó con una tarea nombrada.**
> Sabe lo que no sabe, y sabe por qué todavía no lo aprendió."

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

## ✅ Decisión del equipo: el pitch cierra en V1

**No construimos V2, y es a propósito.** La narrativa de cerrar en V1 demuestra
que entendimos la lógica del sistema, en vez de correr a inflar un número:

- El único caso que V1 no resuelve es el del **VIN duplicado**, que es
  exactamente una de las dos lecciones que el sistema **decidió diferir**.
- O sea: lo que falta no es un hueco, es **la siguiente tarea, ya nombrada por
  el propio sistema y con su razón escrita**.
- Eso enseña algo más difícil que un número alto: **el sistema sabe lo que no
  sabe.**

Si alguien pregunta por qué no hay V2, la respuesta es ésa, y se dice sin
disculparse. **Nada en este pitch afirma números que no medimos.**

---

## Números reales, para no equivocarse en vivo

**Todo lo de abajo está medido. Nada es proyección.**

| | V0 | V1 |
|---|---|---|
| Casos resueltos (holdout, 20) | **5/20** | **19/20** |
| Integridad (2 chequeos de lote) | 0/2 | 0/2 |
| Lecciones activas | 0 | 9 |
| Tests de lección verdes | 0/9 | **9/9** |
| Único caso sin resolver | — | **C056**, VIN duplicado |

### Ablation: cuatro lecciones, cuatro atribuciones exactas

V1 completa: **19/20**. Apagando una sola lección:

| Lección apagada | Marcador | Caen | Casos que caen | Casos con ese defecto en holdout |
|---|---|---|---|---|
| **L1** sufijo k en km | 16/20 | 3 | C042, C047, C057 | C042, C047, C057 ✅ |
| **L2** precio en USD | 16/20 | 3 | C042, C048, C057 | C042, C048, C057 ✅ |
| **L3** checksum de VIN | 16/20 | 3 | C044, C049, C059 | C044, C049, C059 ✅ |
| **L5** millas a km | 16/20 | 3 | C045, C051, C060 | C045, C051, C060 ✅ |

**Las cuatro coinciden exacto.** Si el jurado pide otra, se corre en vivo:
`make ablate L=L4 V=v1`.

---

## Las 4 frases que tienen que salir sí o sí

Si el tiempo se va, se sacrifica cualquier cosa menos éstas:

1. **«Un sistema que pasa todo en verde no tiene nada que enseñarte.»**
2. **«Se negó a aprender dos fallas porque todavía no podía atribuir la causa.»**
3. **«Tiramos un 20/20 porque era un número sin evidencia detrás.»**
4. **«Apago una lección y caen exactamente los tres casos que arreglaba.»**
5. **«El loop no se quedó sin trabajo: se quedó con una tarea nombrada.»**

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

> De cinco a **diecinueve de veinte**, sobre los mismos veinte casos que el
> sistema nunca vio al aprender.
>
> Y la prueba de que no fue suerte: apago **una sola** lección, la de millas a
> kilómetros. Baja a dieciséis. **Caen tres casos: C045, C051, C060** — son
> exactamente los tres casos de millas del banco. **Ni uno más.** Lo
> verificamos con cuatro lecciones distintas y las cuatro dan atribución
> exacta.
>
> Y el caso que V1 **no** resuelve es el del VIN duplicado: justo una de las
> dos lecciones que el sistema había diferido. **El loop no se quedó sin
> trabajo, se quedó con una tarea nombrada.**
>
> Codex no fue nuestro copiloto: fue el **órgano de construcción**. Nosotros
> escribimos el examen y el loop; **V1 lo escribió él.**

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
