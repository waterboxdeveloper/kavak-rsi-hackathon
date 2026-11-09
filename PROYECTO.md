# PROYECTO — Kavak Listing Autopilot

> Sistema de agentes que aprende de sus propias corridas y usa lo aprendido
> para construir su siguiente versión.
> RSI Hackathon · Kavak × OpenAI × Primero AI · 9 nov 2026

> 🧠 **¿Primera vez aquí, o se siente confuso todo este pedo?**
> Lee [**docs/ENTENDER.md**](docs/ENTENDER.md) antes que nada: explica el
> sistema desde cero, sin jerga, con los números reales que ya obtuvimos, y
> cierra con la receta de 6 preguntas para aplicar este patrón a cualquier
> otro problema. Este archivo (PROYECTO.md) es el mapa; ése es el porqué.

---

## 1. Explicado como si tuvieras 5 minutos

Imagina un becario que da de alta autos usados en el inventario de Kavak.
Le llegan anuncios escritos por humanos, sucios:

```
VENDO Volkswagen Jetta 2017 / 30k kms / $193,000 / credito disponible / vin: 3VWA11AA1AA000001
```

El becario tiene que sacar de ahí: marca, modelo, año, kilometraje, precio,
VIN, y levantar banderas si algo huele mal.

**El becario del día 1 (le llamamos V0)** hace lo que haría cualquiera: agarra
el primer número que ve. Entonces lee `30k kms` y escribe **30 kilómetros**.
Un auto con 30 km. Nadie lo revisa y se publica.

Aquí viene la idea del proyecto. En vez de que *nosotros* arreglemos al
becario, montamos tres piezas alrededor de él:

| Pieza | Qué hace | En el repo |
|---|---|---|
| 👀 **El observador** | Corre al becario sobre 60 anuncios de los que sí sabemos la respuesta, y anota exactamente dónde se equivocó | `loop/observe.py` |
| 📓 **El cuaderno** | Convierte cada error en una **lección escrita**: la regla, dónde debe vivir en el código, y un **test que hoy falla** | `loop/learn.py` |
| 🏗️ **El constructor** | Le pasa a **Codex** el código del becario viejo + el cuaderno, y Codex escribe al **becario nuevo** | `loop/build.py` |

Y eso es todo el truco: **el sistema no se arregla, se reemplaza.** V0 no
mejora: V0 genera las lecciones con las que se construye V1. Y V1, al correr
limpio, deja ver fallas más profundas que estaban escondidas, que son las que
producen V2.

### La cadena de versiones

```
V0  Extractor ingenuo
    └─ falla: "30k kms" → 30 km. No valida VIN. No marca salvamento.
       │
       │  9 lecciones persistidas (L1..L9)
       ▼
V1  Extractor + Validador   ← CONSTRUIDO POR CODEX desde V0 + lecciones
    └─ ya normaliza y valida. Al limpiarse el ruido aparecen 2 fallas
       de PROCESO que antes no se podían atribuir:
         · el mismo VIN publicado 2 veces crea 2 autos en inventario
         · confirmó un alta cuya escritura se interrumpió (mentira al cliente)
       │
       │  + 2 lecciones nuevas (L10, L11) = 11 acumuladas
       ▼
V2  Agente de ingesta con integridad transaccional   ← CONSTRUIDO POR CODEX
    └─ hereda las 9 anteriores + dedupe por VIN + confirmar sólo después
       de persistir
```

### Por qué esto gana puntos

La rúbrica no premia al agente más listo. Premia que se vea el ciclo:
**falla observable → lección guardada → sucesor que la hereda → mismo
benchmark con número que sube → ablation que prueba la causa.**

Lo que proyectamos en pantalla. **Todo medido, nada proyectado:**

| | V0 | V1 |
|---|---|---|
| Casos resueltos (holdout, 20 casos) | **5/20** | **19/20** |
| Chequeos de integridad | 0/2 | 0/2 |
| Lecciones activas | 0 | 9 |
| Tests de lección verdes | 0/9 | **9/9** |
| Único caso sin resolver | — | **C056**, VIN duplicado |

Y el cierre: `make ablate L=L5 V=v1` apaga **una** lección y los casos de
millas vuelven a romperse. **Exactamente ésos, ni uno más** — verificado con
4 lecciones distintas. Eso es la prueba de causalidad; sin eso la mejora es
anécdota.

> ### Por qué cerramos en V1 y no construimos V2
>
> **Decisión del equipo, a propósito.** El único caso que V1 no resuelve es el
> del VIN duplicado — que es exactamente una de las dos lecciones que el
> sistema **decidió diferir** con su razón escrita.
>
> O sea: lo que falta no es un hueco, es **la siguiente tarea ya nombrada por
> el propio sistema**. Cerrar ahí demuestra que entendimos la lógica del
> ciclo, en vez de correr a inflar un número. El sistema **sabe lo que no
> sabe**, y eso es más difícil de lograr que un marcador alto.
>
> El loop sigue siendo replayable: `make reset && make demo` lo corre desde
> cero y cualquiera ve nacer las 9 lecciones. Y `make build-v2` existe: la
> segunda vuelta está construida, sólo no la ejecutamos. Ver
> [docs/DECISIONES.md](docs/DECISIONES.md) D17.

---

## 2. Las 5 reglas que no se negocian

Si una decisión choca con una de éstas, gana la regla.

1. **El benchmark no se toca.** `bench/` es la vara de medir. Modificarlo a
   media competencia invalida toda comparación. Si hay que cambiarlo, se
   regenera todo desde V0.
2. **El holdout nunca entra al loop.** El sistema aprende sólo de los 40 casos
   `train`. Los 20 `holdout` son el número que presentamos. Si el loop los ve,
   estamos midiendo memoria, no aprendizaje.
3. **Scoring determinista, cero juez-LLM.** El scorer compara campo a campo.
   Un LLM calificando hace que el número sea discutible frente al jurado.
4. **Cada lección va envuelta en `if "Lx" in lessons:`.** Es lo que permite el
   ablation sin reconstruir el agente. Es el momento más fuerte de la demo.
5. **Lo que hizo el sistema vs. lo que hicimos nosotros queda escrito.** La
   rúbrica lo pide explícitamente. Cada fase tiene una sección
   "intervención humana" en su `.md`.

---

## 3. Mapa del repo

```
PROYECTO.md            <- este archivo
intro.md               <- las reglas del hackathon (dado por la organización)
Makefile               <- todos los comandos. `make help` los lista

bench/
  generate_cases.py    60 casos, semilla fija, defectos inyectados
  cases.jsonl          el banco (versionado: es la vara de medir)
  score.py             scorer determinista + 2 chequeos de integridad

agents/
  run.py               corre cualquier versión y guarda la traza
  common/
    constants.py       tipo de cambio, catálogo de modelos
    vin.py             checksum ISO 3779
    store.py           inventario simulado, con fallas de escritura a propósito
    engine.py          texto → campos crudos (stub determinista | OpenAI)
    tools/             herramientas que NACEN de las lecciones (vacío al inicio)
  v0/agent.py          escrito a mano por nosotros
  v1/, v2/             ESCRITOS POR CODEX

loop/
  observe.py           1. corrida → fallas agrupadas con evidencia
  learn.py             2. fallas → lecciones + tests rojos
  build.py             3. lecciones + predecesor → Codex → sucesor

lessons/lessons.jsonl  la memoria del sistema. Esto es el "cuaderno".
tests/                 un test por lección. Rojo = no heredada. Verde = heredada.
runs/                  trazas y scores (ignoradas por git; evidencia/ sí se versiona)
report.py              la tabla comparativa de la demo

docs/
  ENTENDER.md          el sistema explicado desde cero + cómo reusar el patrón
  fases/FASE-*.md      bitácora: una por fase, con resultados y commits
  demo/guion-3min.md   el guion cronometrado
  git-workflow.md      cómo trabajamos en equipo sin pisarnos
```

---

## 4. Cómo correrlo (sin API key, en 30 segundos)

```bash
make bench      # genera los 60 casos
make v0         # corre el becario ingenuo → 5/20 holdout
make observe    # ¿dónde falló exactamente?
make learn      # convierte esas fallas en 9 lecciones + 9 tests rojos
make test       # los 9 tests en ROJO (nadie los hereda todavía)
make build      # Codex escribe V1
make test       # los mismos 9 tests en VERDE
make v1         # mide V1 en holdout
make report     # la tabla
```

El motor por default es `stub` (regex determinista, sin red). Para usar el LLM
de verdad: `--engine openai` con `OPENAI_API_KEY` en el entorno.

---

## 5. Estado y bitácora

| Fase | Qué | Estado |
|---|---|---|
| [00](docs/fases/FASE-00-setup.md) | Setup, reglas, repo | ✅ |
| [01](docs/fases/FASE-01-benchmark.md) | Banco de 60 casos | ✅ |
| [02](docs/fases/FASE-02-v0-extractor.md) | V0 ingenuo + línea base | ✅ |
| [03](docs/fases/FASE-03-observe-learn.md) | Observar y aprender | ✅ |
| [04](docs/fases/FASE-04-build-v1.md) | Codex construye V1 | ⬜ |
| [05](docs/fases/FASE-05-build-v2.md) | Segunda iteración → V2 | ⬜ |
| [06](docs/fases/FASE-06-ablation-demo.md) | Ablation + demo | ⬜ |

---

## 6. Las 4 respuestas que el jurado va a pedir

Tenerlas memorizadas, no leídas:

**¿Cómo aislaron el efecto del cambio?**
> Mismo banco de 60 casos con semilla fija, mismo scorer, y los 20 holdout
> nunca entraron al loop. Además cada lección está detrás de un flag: la
> apagamos en vivo y reaparecen exactamente los casos que arreglaba.

**¿Qué haría fallar a la última versión?**
> Un anuncio sin VIN, dos monedas en el mismo texto, o un modelo fuera de
> nuestro catálogo de 8. El reporte lo dice solo en "Qué sigue fallando".

**¿Cómo usaron Codex?**
> Codex es el órgano de construcción del sistema, no nuestro copiloto.
> `loop/build.py` le entrega el código del predecesor y las lecciones, y
> Codex escribe el sucesor completo. V0 y el loop son nuestros; V1 y V2 son
> de Codex. Los prompts quedaron guardados en `runs/`.

**¿Qué trajeron y qué construyeron hoy?**
> Lo que diga `docs/fases/FASE-00-setup.md` — ahí está la línea de corte con
> hora y commit.
