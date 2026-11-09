# Guion de la demo — 3:00 + 2:00 de preguntas

> Dos personas: **quien habla** y **quien teclea**. Nunca la misma.
> Los comandos van pre-escritos en un archivo para copiar y pegar: nadie
> teclea en vivo bajo presión.

---

## 0:00 – 0:40 · La versión inicial falla

**Decir** (una frase, nada más):

> *"Kavak recibe anuncios de autos escritos por personas. Alguien tiene que
> convertirlos en inventario confiable. Hicimos un agente que hace eso mal a
> propósito, y un sistema que aprende de sus errores y escribe al agente
> siguiente."*

**Teclear:**
```bash
make v0
```

**Señalar en pantalla:** `holdout 5/20` · `integridad 0/2`

**Decir, apuntando a un caso concreto:**

> *"Este anuncio dice `USD $14,324`. El agente guardó catorce mil trescientos
> veinticuatro **pesos** un auto de doscientos sesenta y cinco mil. Y aquí
> —`30k kms`— registró un Jetta con treinta kilómetros."*

🎯 Que se entienda el daño sin explicar nada técnico.

---

## 0:40 – 1:45 · Qué aprendió y qué construyó

**Teclear:**
```bash
make observe
```
> *"El sistema no dice 'falló'. Dice qué campo, en qué casos, qué esperaba y
> qué obtuvo."*

**Teclear:**
```bash
make learn
```
> *"Convierte cada grupo de fallas en una lección con cuatro partes: la
> evidencia que la provocó, la regla, la función donde debe vivir, y un test
> automático."*

**Abrir `lessons/lessons.jsonl`** (pestaña ya abierta) y leer una línea.

**Teclear:**
```bash
make test
```
> *"Nueve tests en rojo. El sistema sabe nueve cosas y ninguna está
> implementada todavía."*

⚡ **EL MOMENTO FUERTE — señalar las dos DIFERIDAS:**

> *"Miren esto: el sistema también detectó dos fallas de proceso —el mismo auto
> dado de alta dos veces, y una confirmación al cliente de algo que nunca se
> guardó— y **se negó a aprender de ellas**. Su razón, textual: 'no se puede
> atribuir causa aún, todavía hay 38 casos con ruido de extracción'. Primero
> limpia la señal, después diagnostica. Eso es lo que genera la segunda
> versión."*

**Teclear:**
```bash
make build          # Codex construye V1
make test           # los mismos 9, ahora VERDES
```
> *"Codex recibió el código del predecesor, las nueve lecciones y los nueve
> tests rojos. Escribió el sucesor completo."*

**Si hubo intervención humana, decirlo aquí. Exactamente aquí.**

---

## 1:45 – 3:00 · Comparar y probar causalidad

**Teclear:**
```bash
make report
```

| | V0 | V1 | V2 |
|---|---|---|---|
| holdout (20 casos) | 5/20 | 16/20 | 19/20 |
| integridad | 0/2 | 0/2 | 2/2 |
| lecciones activas | 0 | 9 | 11 |

> *"Mismos veinte casos, que el sistema nunca vio al aprender. V2 no lee
> mejor que V1: **trabaja** mejor. Ahí está el 0/2 → 2/2."*

⚡ **EL CIERRE — ablation en vivo:**
```bash
make ablate L=L5 V=v2
```
> *"Apago **una** lección, la de millas a kilómetros. Vuelven a fallar ocho
> casos. **Exactamente los ocho de millas, ni uno más.** Por eso podemos decir
> que la mejora vino de la lección y no de la suerte."*

**Cerrar con Codex (obligatorio, es 25% de la nota):**

> *"Codex no fue nuestro copiloto: fue el órgano de construcción del sistema.
> `loop/build.py` le entrega el predecesor y las lecciones, y Codex escribe el
> sucesor. V0 y el loop son nuestros. **V1 y V2 los escribió Codex.** Los
> prompts están guardados en `runs/`."*

---

## 2:00 de preguntas — tener abierto

| Pregunta | Respuesta | Archivo |
|---|---|---|
| ¿Cómo aislaron el efecto? | Banco fijo con semilla, 20 casos apartados, y cada lección detrás de un flag que apagamos en vivo | `bench/cases.jsonl` |
| ¿Qué haría fallar a V2? | Anuncio sin VIN, dos monedas en el mismo texto, modelo fuera de nuestro catálogo de 8. El reporte lo dice solo | última sección de `make report` |
| ¿Quién decidió la lección? | El repertorio de reglas es nuestro; el sistema elige cuál aplica, a qué casos y **cuándo hay evidencia suficiente** | `loop/learn.py:CATALOG` |
| ¿Qué trajeron vs. hoy? | El repo nació hoy. Sólo `intro.md` es previo | `docs/fases/FASE-00-setup.md` |

**Las 3 cosas a la mano:** una corrida (`runs/v0-holdout.json`), la lección que
salió de ella (`lessons/lessons.jsonl:1`), el cambio que heredó el sucesor
(`git show` del commit de V1).

---

## Reglas de la demo

1. **Nada se teclea en vivo.** Comandos en un archivo, copiar y pegar.
2. **Si algo truena, no se depura.** Se abre el score guardado en
   `runs/evidencia/` y se sigue hablando.
3. **A los 3:00 se corta.** Ensayar 3 veces con cronómetro. El ablation es el
   cierre: si se va el tiempo, se sacrifica cualquier otra cosa menos ése.
4. **Decir la intervención humana sin que la pregunten.** Un equipo que la
   declara se ve más sólido, no más débil.
