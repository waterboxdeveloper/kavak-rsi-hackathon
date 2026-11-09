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
