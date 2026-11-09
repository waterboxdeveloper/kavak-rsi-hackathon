# Nuestra propuesta, explicada con la misma lupa

> Lee primero [CASOS-DE-USO.md](CASOS-DE-USO.md): este documento aplica esa
> misma lupa —*¿dónde está el juez gratis?*— a lo que estamos construyendo.

---

## El reencuadre

Si alguien te pregunta qué hicimos, la respuesta obvia es "un agente que lee
anuncios de autos". **Esa respuesta está mal**, y entenderlo es entender el
proyecto:

> No construimos un lector de anuncios.
> Construimos **un juez**, y al lado le pusimos un agente desechable.

El agente es lo barato. V0 son 40 líneas y es malo a propósito. V1 y V2 no los
escribimos nosotros. Lo que costó pensar —y lo único que no se puede
automatizar— es el juez: 60 casos con respuesta conocida, un scorer que no
opina, y 11 defectos etiquetados uno por uno.

**Todo lo demás del repo existe para servirle a ese juez.**

---

## ¿De dónde sacamos nuestro juez gratis?

De los 5 lugares posibles, elegimos el **#4: existe un registro canónico**.

| Lo que verificamos | El registro canónico | Dónde vive en el código |
|---|---|---|
| El VIN es real | **dígito verificador ISO 3779**: el carácter 9 es un checksum de los otros 16 | `agents/common/vin.py` |
| El año es posible | el rango de años en que existió esa generación del modelo | `constants.py:MODEL_YEARS` |
| El precio en pesos | tipo de cambio fijo del benchmark | `constants.py:USD_MXN` |
| El kilometraje | factor millas→km | `constants.py:MILES_TO_KM` |
| El auto no está duplicado | el VIN es único en el mundo | el chequeo de integridad del lote |

Y como no nos dieron datos, hicimos algo más: **fabricamos el juez
completo.** Generamos los 60 anuncios nosotros, así que no sólo sabemos la
respuesta correcta — sabemos **qué defecto tiene cada caso**.

Eso último es lo que nos da el superpoder del proyecto:

> Podemos decir *"la lección L5 arregló exactamente estos 8 casos, ni uno
> más"*. Con datos reales eso sería casi imposible de afirmar.

**Lo honesto:** fabricar el juez es nuestra mayor fortaleza *y* nuestra mayor
debilidad. Volvemos a eso en la sección de límites.

---

## Las 4 piezas, y qué pasa si quitas cada una

La mejor forma de ver que cada pieza carga peso es imaginar el sistema sin
ella. Es un ablation del diseño mismo:

| Si quitas… | Qué te queda |
|---|---|
| **el examen** (`bench/`) | un agente que nadie sabe si sirve. "Mejoró" vuelve a ser opinión |
| **el observador** (`loop/observe.py`) | sabes que falló pero no dónde. La lección se vuelve adivinanza |
| **el cuaderno** (`lessons/lessons.jsonl`) | arreglas lo mismo cada semana. Cero acumulación |
| **el candado** (`tests/`) | la lección se pierde en la siguiente versión y nadie se enteró |
| **el ablation** (`--ablate`) | "subimos de 5 a 19" sin poder probar por qué. Anécdota |
| **Codex** (`loop/build.py`) | lo escribes tú a mano. Funciona, pero ya no es un sistema que construye: es un humano con asistente |
| **los 20 casos apartados** | mides memoria, no aprendizaje. Y no te das cuenta |

Fíjate que **la única pieza sustituible es Codex** (`--builder claude` y
listo). Las otras seis no: son el sistema.

---

## Qué se acumula, exactamente

Esto es lo que el sistema "sabe" hoy, y está en un archivo de texto que puedes
abrir:

| | Lecciones | Estado | Qué aprendió |
|---|---|---|---|
| De V0 | **L1 – L9** | ✅ aprendidas y heredadas por V1, 9 tests en verde | leer kilometraje (sufijo k, millas, punto de miles), leer precio (USD, k, punto), validar checksum de VIN, detectar salvamento, detectar año imposible |
| De V1 | **L10 – L11** | ⏸️ **diferidas** — identificadas con su razón, no aprendidas | no dar de alta dos veces el mismo VIN · confirmar sólo después de persistir |

> **Cerramos en V1 a propósito.** El único caso que V1 no resuelve es el del
> VIN duplicado, que es precisamente una de esas dos lecciones diferidas. Lo
> que falta no es un hueco: es la siguiente tarea **ya nombrada por el propio
> sistema**. Ver [DECISIONES.md](DECISIONES.md) D17.

Y cada una existe en **tres lugares al mismo tiempo**, lo que es justo lo que
impide que se pierda:

1. como **regla** en `lessons/lessons.jsonl` (legible por humanos),
2. como **función** en `agents/common/tools/` (ejecutable),
3. como **test** en `tests/` (que grita si alguien la rompe).

> **Eso es la diferencia entre "le volví a pedir al modelo que lo haga mejor"
> y un sistema que aprende.** Lo primero se olvida en el siguiente prompt. Lo
> segundo queda escrito, ejecutándose y vigilado.

---

## Los 3 momentos en que esto se siente vivo

No son adornos de demo: son los tres puntos donde el sistema hace algo que
nadie le dijo.

### 1. Cuando se negó a aprender

El sistema detectó las dos fallas de proceso y **las diferió**:

```
DIFERIDA [write_interrupted] -> es una falla de proceso y todavía hay
         38 casos con ruido de extracción. No se puede atribuir causa aún.
```

Decidió que con 38 casos fallando por mala extracción, una falla de integridad
podría ser *consecuencia* y no *causa*. Primero limpia, luego diagnostica.

**Y eso, de pasada, es lo que genera la cadena de versiones.** V1 limpia el
ruido → las fallas de proceso quedan aisladas → nacen L10 y L11 → eso
justifica V2. La escalera no es un guion: es consecuencia de la disciplina.

### 2. Cuando 9 rojos se vuelven 9 verdes

```
0 verdes / 9 rojos      ← el sistema sabe 9 cosas, ninguna implementada
      ↓  (Codex construye V1)
9 verdes / 0 rojos      ← el sucesor las heredó todas
```

Nadie tocó esos tests. Los escribió el propio sistema **antes** de que
existiera el código que los pasa.

### 3. Cuando apagas una lección y la falla regresa

```bash
make ablate L=L5 V=v2
```

Vuelven a fallar los 8 casos de millas. **Exactamente ésos.** Ahí deja de ser
"mejoró" y se vuelve "mejoró por esto".

---

## Dónde se rompe nuestra propuesta

La parte que hay que decir sin que nos pregunten:

| Límite | Qué tan grave |
|---|---|
| **El juez es sintético.** Los 60 anuncios los generamos nosotros | La crítica más justa. Un anuncio real es más sucio y más raro |
| Sólo 8 modelos de auto en el catálogo | Un Tsuru rompe el chequeo de año |
| El repertorio de lecciones es humano (`learn.py:CATALOG`) | El sistema elige *cuál* y *cuándo*; el menú lo escribimos nosotros |
| No hay fotos, ni texto sin VIN, ni dos monedas en el mismo anuncio | El reporte lo confiesa solo en "Qué sigue fallando" |
| El sistema construye a su sucesor, **no se modifica a sí mismo** | Es ADAS, no Darwin Gödel Machine. Hay que decirlo así |

---

## El upgrade: cómo se vuelve real

Y aquí está lo bonito de haber aprendido la lupa de los 5 jueces. Nuestra
debilidad —el juez sintético— se arregla **cambiando de juez, no de sistema**:

| | Hoy (hackathon) | En Kavak de verdad |
|---|---|---|
| Juez | #4 registro canónico + casos fabricados | **#1 el futuro responde**: el auto se vendió en X días a $Y |
| Banco de casos | 60 sintéticos | los últimos 2,000 anuncios reales con su desenlace |
| Métrica | campos correctos | error de precio, días en piso, devoluciones |
| Lecciones | parseo y validación | estacionalidad, región, color, kilometraje |

**El loop, el cuaderno, los tests, el ablation y el constructor no cambian ni
una línea.** Sólo se reemplaza `bench/`. Eso es la prueba de que lo que
construimos hoy no fue un demo de hackathon: fue la maquinaria.

---

## El filtro, aplicado a nosotros mismos

> **¿Qué nos dice gratis si salió bien?**
>
> Hoy: 20 casos apartados, respuesta conocida, scorer que no opina.
> Mañana en producción: la venta real a 30 días.
>
> Las dos respuestas son números. Por eso esto es un loop y no un chatbot.
