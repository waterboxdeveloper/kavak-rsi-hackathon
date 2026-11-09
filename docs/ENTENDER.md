# ENTENDER — qué estamos haciendo, desde cero

> Este documento no asume que sabes nada. Si algo aquí no te queda claro,
> está mal escrito y hay que arreglarlo, no es que tú no entiendas.
>
> Objetivo: que al terminar puedas explicárselo a alguien más **y** que puedas
> imaginar dónde más aplicarlo.

---

## 1. La idea en una servilleta

Normalmente, cuando un programa de IA falla, pasa esto:

```
el programa falla → un humano lo nota → el humano lo arregla
```

Lo que estamos construyendo cambia quién hace los últimos dos pasos:

```
el programa falla → el SISTEMA lo nota → el SISTEMA escribe la lección
                 → el SISTEMA construye el programa siguiente
```

Eso es todo. Se llama **self-improving** (auto-mejorante) y suena a ciencia
ficción, pero son 4 scripts de Python y un archivo de texto. En serio.

La parte contraintuitiva: **no mejoramos el programa, lo reemplazamos.** El
programa viejo no se vuelve más listo. El programa viejo sirve para *generar
las lecciones* con las que se escribe el programa nuevo. Como un borrador que
no se corrige: se tira, pero te deja saber qué escribir en la versión buena.

---

## 2. El problema que elegimos (y por qué importa que sea aburrido)

Kavak compra y vende autos usados. Le llegan anuncios escritos por personas
normales, o sea: un desastre.

```
VENDO Volkswagen Jetta 2017 / 30k kms / $193,000 / credito disponible / vin: 3VWA11AA1AA000001
```

Alguien tiene que convertir ese texto en datos ordenados:

| campo | valor correcto |
|---|---|
| marca | Volkswagen |
| modelo | Jetta |
| año | 2017 |
| kilometraje | 30000 |
| precio (MXN) | 193000 |
| VIN | 3VWA11AA1AA000001 |
| banderas de riesgo | ninguna |

**Elegimos un problema aburrido a propósito.** No porque sea lo más
emocionante, sino porque tiene una propiedad valiosísima: **existe una
respuesta correcta y es verificable.** `30k kms` son 30,000 km y punto. No es
opinión.

👉 **Lección #1 que te llevas:** si quieres que un sistema aprenda solo,
necesitas un problema donde se pueda saber, sin discutir, si estuvo bien o
mal. Si la respuesta correcta es opinable ("¿este texto es bonito?"), el
sistema no tiene de dónde agarrarse y tú tampoco.

---

## 3. Las 4 piezas, con la analogía del becario

Imagina que contratas un becario para capturar esos anuncios.

### Pieza 0 · El examen (`bench/`)

Antes de que el becario toque nada, armamos **un examen de 60 anuncios de los
que ya sabemos la respuesta.** Como un examen con la hoja de respuestas
guardada.

Y algo importante: **40 anuncios son para practicar y 20 están guardados bajo
llave.** El becario (y el sistema) nunca ven esos 20 mientras aprenden. Sólo
se usan para calificar.

👉 **Lección #2:** eso se llama **held-out** (apartado). Si calificas con los
mismos ejemplos con los que entrenaste, estás midiendo memoria, no
aprendizaje. Es el error #1 en proyectos de IA y pasa todo el tiempo en la
vida real.

### Pieza 1 · El becario ingenuo (`agents/v0/agent.py`)

Escribimos a mano la versión más tonta que se nos ocurrió. Su regla de oro es
"agarra el primer número que veas":

```python
def naive_int(raw):
    m = re.search(r"\d+", raw)   # el primer número que aparezca
    return int(m.group(0))
```

Entonces lee `30k kms` y escribe **30 kilómetros**. Un Jetta con 30 km.

**No lo arreglamos.** Esto es lo que más confunde a la gente al principio: el
becario malo no es un accidente, es el **insumo**. Sus errores son la materia
prima de todo lo demás.

### Pieza 2 · El observador (`loop/observe.py`)

Corre al becario sobre el examen, compara contra la hoja de respuestas y anota
**exactamente** dónde se equivocó. No "le fue mal", sino:

```
[5 casos] odo_k_suffix   campos: odometer_km
   C002: VENDO Volkswagen Jetta 2017 / 30k kms / $193,000 / ...
   esperado {'odometer_km': 30000}  ->  obtenido {'odometer_km': 30}
```

👉 **Lección #3:** la diferencia entre un sistema que aprende y uno que no es
el **nivel de detalle de la evidencia.** "Falló" no sirve para nada. "Falló en
el campo `odometer_km`, en estos 5 casos, cuando el texto trae sufijo k, y
puso 30 donde iban 30000" ya es casi la solución escrita.

### Pieza 3 · El cuaderno (`loop/learn.py` → `lessons/lessons.jsonl`)

Toma ese grupo de fallas y escribe una **lección**. Una lección no es un
párrafo bonito, son cuatro cosas concretas:

```json
{
  "id": "L1",
  "evidence_cases": ["C002", "C012", "C017"],
  "rule": "El kilometraje puede venir con sufijo 'k' (56k = 56000). Normalizar antes de guardar.",
  "artifact": "agents/common/tools/odometer.py::normalize_odometer",
  "test": "tests/test_lesson_L1.py"
}
```

| parte | para qué sirve |
|---|---|
| `evidence_cases` | **de dónde salió.** Sin esto, la lección es una opinión. |
| `rule` | qué hacer, en imperativo y verificable. |
| `artifact` | **dónde debe vivir en el código.** No basta "acuérdate de esto": tiene que convertirse en una función que exista. |
| `test` | una prueba automática que **hoy falla**. |

Ese último es el más astuto y vale la pena detenerse.

Junto con la lección, el sistema escribe este archivo:

```python
from agents.common.tools.odometer import normalize_odometer

def test_l1_1():
    assert normalize_odometer('56k kms') == 56000
```

Ese archivo **truena hoy**, porque `normalize_odometer` todavía no existe. Y
eso es exactamente lo que queremos:

- 🔴 **test rojo** = la lección es real, hay algo que de verdad no funciona.
- 🟢 **test verde** = el programa nuevo **sí** heredó la lección.

👉 **Lección #4:** convertir cada aprendizaje en un test automático es el
truco más poderoso de todo esto. Un test es una lección que **se defiende
sola para siempre.** Si alguien, dentro de 6 meses, borra sin querer la
conversión de millas, el test se pone rojo y grita. La lección no depende de
que alguien se acuerde.

### Pieza 4 · El constructor (`loop/build.py` → **Codex**)

Aquí entra Codex (el modelo de OpenAI que escribe código). El script arma un
mensaje con tres cosas y se lo manda:

1. el código completo del becario viejo,
2. las 9 lecciones del cuaderno,
3. los tests rojos que tiene que lograr poner verdes.

Y Codex **escribe al becario nuevo** (`agents/v1/agent.py`) desde cero.

👉 **Lección #5:** el modelo de IA no es "el sistema". El modelo es **una
pieza intercambiable** dentro de una maquinaria que tú diseñaste. La
maquinaria (examen + observador + cuaderno + tests) es lo que hace que
funcione. Si mañana sale un modelo mejor, lo cambias y todo lo demás sigue
igual. Esto es lo que separa un proyecto de IA serio de un chatbot con
esteroides.

---

## 4. El recorrido real, con los números que de verdad salieron

Esto ya lo corrimos. No es teoría.

### Paso 1 — calificamos al becario ingenuo

```bash
$ make v0
```
```
casos resueltos : 15/60
  train         : 10/40
  holdout       : 5/20     <- el número que presentamos
integridad      : 0/2
```

Resolvió **5 de 20**. Los 5 que resolvió son los anuncios limpios, sin trampa.
Falló en todos los que traían algo raro.

Nota el detalle: los 15 limpios **sí** los pasó. Eso fue a propósito.

👉 **Lección #6:** tu punto de partida debe ser **malo, no inútil.** Si V0
hubiera sacado 0/20, no habría contraste: no sabrías si la mejora vino de tus
lecciones o de que antes todo estaba roto. De hecho eso nos pasó: el primer
`naive_int` que escribí fallaba hasta en los casos limpios y lo tuve que
ajustar.

### Paso 2 — ¿dónde falló, exactamente?

```bash
$ make observe
```
```
[5 casos] odo_k_suffix    esperado 30000  ->  obtenido 30
[5 casos] price_usd       esperado 264994 ->  obtenido 14324
[5 casos] vin_invalid...  esperado ['vin_invalid'] -> obtenido []
[5 casos] salvage_wording esperado ['salvage']     -> obtenido []
[5 casos] odo_miles       esperado 115000 ->  obtenido 71458
...
```

Fíjate en `price_usd`: el anuncio decía `USD $14,324` y el becario escribió
14,324 pesos. Un auto de ~265 mil pesos publicado en 14 mil. Ése es el tipo de
error que en la vida real le cuesta dinero a alguien.

### Paso 3 — el sistema escribe sus lecciones

```bash
$ make learn
```
```
== lecciones nuevas: 9 ==
  L1  [odo_k_suffix]   <- 5 casos fallaron en odometer_km
      regla    : El kilometraje puede venir con sufijo 'k'...
      artefacto: agents/common/tools/odometer.py::normalize_odometer
      test ROJO: tests/test_lesson_L1.py
  ... L2 a L9 ...

  DIFERIDA  [write_interrupted] -> es una falla de proceso y todavía hay
            38 casos con ruido de extracción. No se puede atribuir causa aún.
  DIFERIDA  [duplicate_vin]     -> idem
```

**Pon mucha atención a esas dos DIFERIDAS, porque es mi parte favorita.**

El examen tiene dos trampas distintas a las demás. No son errores de *leer* un
dato, son errores de *cómo trabaja*:

- el mismo auto publicado dos veces → lo da de alta dos veces en el inventario;
- la escritura a la base se interrumpe → **ya le había dicho al cliente "listo"**
  cuando en realidad nada se guardó.

El sistema los detectó, y aun así **se negó a aprender de ellos todavía**. Su
razonamiento, literal, está en el código:

> *"No se puede atribuir causa aún: con 38 casos fallando por mala extracción,
> una falla de integridad podría ser consecuencia de un campo mal parseado."*

👉 **Lección #7 (la más transferible de todas):** no diagnostiques causas
mientras tengas ruido. Primero limpia lo evidente, vuelve a medir, y *entonces*
mira qué sigue fallando. Esto aplica a depurar código, a investigar una caída
en producción, a analizar por qué bajaron las ventas y a tu vida en general.
La mitad de las "causas" que la gente encuentra son ruido mal interpretado.

Y como efecto secundario hermoso: eso es lo que genera la cadena de versiones
de forma natural. V1 limpia el ruido → las fallas de proceso quedan a la
vista → nacen 2 lecciones nuevas → eso justifica V2.

### Paso 4 — los 9 tests están rojos

```bash
$ make test
```
```
ROJO  L1  El kilometraje puede venir con sufijo 'k'...
      ModuleNotFoundError: No module named 'agents.common.tools.odometer'
...
0 verdes / 9 rojos
```

Perfecto. El sistema sabe 9 cosas y **ninguna está implementada**. Ese es el
"antes" de la demo.

### Paso 5 — Codex construye al sucesor

```bash
$ make build
```

Codex recibe V0 + las 9 lecciones + los 9 tests rojos, y escribe
`agents/v1/agent.py` más las herramientas nuevas. Los mismos 9 tests deben
ponerse **verdes**, y el examen debe subir de `5/20` a ~`16/20`.

*(Este paso es el único que falta correr.)*

### Paso 6 — la prueba de que no fue casualidad

Éste es el paso que casi nadie hace y es el que convierte "mejoró" en
"mejoró **por esto**".

```bash
$ make ablate L=L5 V=v2
```

Apaga **una sola lección** (la de millas → km) y vuelve a correr el examen.
Resultado esperado: los 8 casos de millas vuelven a fallar. **Exactamente
ésos, ni uno más.**

Funciona porque en el código cada lección vive detrás de un interruptor:

```python
if "L5" in lessons:
    km = convertir_millas_a_km(texto)
```

👉 **Lección #8:** esto se llama **ablation** (ablación) y es cómo se prueba
causalidad en ciencia: quitas *una* variable y ves qué se cae. Sin esto,
"subimos de 5 a 19" es una anécdota. Con esto, es una afirmación causal que
puedes defender frente a cualquiera.

---

## 5. Entonces, ¿esto es "IA que se mejora sola"?

Sí, pero quiero ser honesto contigo sobre qué tan "sola", porque la gente
exagera esto en LinkedIn y acabas confundido.

**Lo que el sistema hace solo:**
- detecta sus fallas y las agrupa,
- decide de qué sí y de qué no se puede aprender todavía,
- redacta la lección y escribe el test que la fija,
- escribe el código de su sucesor (vía Codex),
- se vuelve a medir.

**Lo que pusimos los humanos:**
- el examen y la forma de calificar (**eso es el 80% del valor**),
- el becario inicial malo,
- el catálogo de lecciones posibles en `loop/learn.py` — o sea: el sistema
  elige *cuál* lección aplica y *cuándo*, con base en la evidencia, pero el
  repertorio lo escribimos nosotros.

👉 **Lección #9, la más importante de todas:** la inteligencia del sistema no
está en el modelo, está en **el bucle de retroalimentación que construyes
alrededor**. Un modelo mediocre con un buen examen, buena evidencia y buenos
tests mejora. Un modelo excelente sin forma de saber si falló, no mejora
nunca — ni sabrás si empeoró.

---

## 6. 🔑 Cómo aplicar esto a lo que tú quieras

Aquí está el valor real del día. El patrón completo son **6 preguntas**. Si
puedes responderlas, puedes montar esto sobre cualquier cosa:

| # | Pregunta | En nuestro caso |
|---|---|---|
| 1 | ¿Cuál es la tarea y **cómo sé sin discutir** si salió bien? | texto → 7 campos; comparación exacta contra la hoja de respuestas |
| 2 | ¿Dónde está mi **examen fijo**, y cuál parte **aparto** para calificar? | 60 casos, 40 practican / 20 apartados |
| 3 | ¿Cuál es mi **versión mala** de arranque? | V0, "el primer número que veas" |
| 4 | ¿Qué **señal** me dice *exactamente* qué se rompió? | campo + caso + esperado vs obtenido |
| 5 | ¿Dónde **vive** la lección para que no se olvide? | una función + un test automático |
| 6 | ¿Cómo **pruebo** que la mejora vino de la lección? | apago la lección y veo reaparecer esos casos |

Si la pregunta 1 no tiene respuesta clara, **no empieces**: busca la parte del
problema que sí se pueda verificar y empieza por ahí.

### Cuatro ejemplos para que veas que se transfiere

**A. Tu agente de soporte responde mal ciertos tickets**
- Examen: 50 tickets históricos con la respuesta que un humano aprobó.
- Señal: ¿citó la política correcta? ¿prometió algo que no podemos dar?
- Lección: "si el ticket menciona reembolso después de 30 días, cita la
  política X y escala" → una función `detectar_fuera_de_plazo()` + su test.
- Ablation: apágala y mira volver esos tickets a fallar.

**B. Clasificar facturas / gastos**
- Examen: 200 facturas ya categorizadas por contabilidad.
- Señal: matriz de confusión — ¿qué categoría se confunde con cuál?
- Lección: "proveedores que terminan en 'Combustibles' van a Transporte, no a
  Insumos" → regla + test.
- Esto es, literalmente, el mismo proyecto con otro vestido.

**C. Un scraper que se rompe cuando los sitios cambian**
- Examen: páginas guardadas en HTML con los datos que debió sacar.
- Señal: qué campo empezó a venir vacío.
- Lección: un selector nuevo de respaldo + test que fija la página vieja **y**
  la nueva. Aquí el valor es brutal: el conocimiento se **acumula** en vez de
  arreglarse y olvidarse cada mes.

**D. Generación de código / migraciones**
- Examen: 30 funciones con sus tests ya escritos.
- Señal: qué test falla y por qué.
- Lección: "en este repo, las fechas siempre en UTC" → regla al prompt +
  test. Esto es básicamente cómo funciona un `CLAUDE.md` o un `AGENTS.md`
  bien hecho: memoria de proyecto que se acumula.

### La trampa en la que todos caen

**Querer que el sistema aprenda de cosas no verificables.** "Aprende a
escribir mejor copy", "aprende a tener mejor criterio". No hay examen, no hay
señal, no hay lección: sólo un LLM calificando a otro LLM y los dos
alucinando en armonía. Si no tienes cómo verificar, no tienes loop — tienes un
generador de texto que se siente productivo.

---

## 7. Glosario (los nombres "de verdad")

Para que los reconozcas cuando los leas en un paper o en una junta:

| palabra que oirás | lo que significa aquí |
|---|---|
| **benchmark** | el examen de 60 casos |
| **held-out / test set** | los 20 casos apartados |
| **ground truth** | la hoja de respuestas |
| **deterministic eval** | calificar con comparación exacta, sin LLM de juez |
| **LLM-as-judge** | un LLM calificando. Cómodo, pero el número se vuelve opinable |
| **regression test** | el test que impide que una falla ya resuelta regrese |
| **ablation** | apagar una pieza para probar que era la causa |
| **feature flag** | el interruptor `if "L5" in lessons:` |
| **RSI** (*recursive self-improvement*) | el nombre pomposo de todo esto |
| **trace** | la bitácora de lo que hizo el agente (`runs/*.json`) |
| **signal** | la evidencia concreta de que algo se rompió |
| **idempotencia** | hacer algo dos veces no causa daño. Es la lección del VIN duplicado |

---

## 8. Si te quedaste con una sola cosa

> Un sistema no aprende porque el modelo sea listo.
> Aprende porque alguien construyó un lugar donde la verdad se puede medir,
> un lugar donde las lecciones se guardan, y una prueba que no deja que se
> pierdan.
>
> El modelo es el músculo. El bucle es el cerebro. **El bucle lo escribes tú.**

---

**Siguiente lectura:**
- [ESTANDARES-Y-HERRAMIENTAS.md](ESTANDARES-Y-HERRAMIENTAS.md) — ¿esto es un
  estándar? ¿qué documentación oficial existe? ¿por qué Codex y no Claude?
- [PROYECTO.md](../PROYECTO.md) — el mapa del repo y las reglas.
- [fases/](fases/) — la bitácora de cada paso con sus números reales.
