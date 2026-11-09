# Kavak Listing Autopilot — sistema de agentes auto-mejorante

Un sistema que **aprende de sus propias corridas** y usa lo aprendido para que
**Codex construya su versión siguiente**. El dominio: convertir anuncios sucios
de autos usados en fichas de inventario confiables.

RSI Hackathon · Kavak × OpenAI × Primero AI · 9 nov 2026

---

## Esto no es «pedirle a Codex que programe»

La diferencia está en **dónde queda el conocimiento** y **qué costo ataca**:

| | Darle un objetivo a un agente de código | Este loop |
|---|---|---|
| Qué optimiza | el costo de **construir**, una vez | el costo de **operar**, todos los días |
| Dónde queda lo aprendido | en el prompt — muere con la sesión | en el repo: regla + función + test |
| La próxima vez que pasa | lo vuelves a explicar | ya está, y un test impide que se pierda |
| Quién detecta la falla | una persona revisando | **la operación misma** |
| Con qué escala | con tu capacidad de revisar | con los incidentes que el negocio **ya produce** |

Dicho en una línea: pedirle código a un agente baja el **CAPEX** de construir
algo una vez. Un loop como éste baja el **OPEX** de operarlo para siempre.

### Las tres propiedades que lo convierten en palanca de OPEX

1. **La señal ya existe y es gratis.** Los errores de captura ya ocurren hoy, y
   hoy se corrigen a mano y se olvidan. El loop sólo empieza a *guardarlos*.
2. **El arreglo no se degrada.** Cada lección nace con un test de regresión.
   El conocimiento de un proceso humano se va con la persona; una lección con
   test se queda. **El costo de esa clase de falla se va a cero y ahí se
   queda.**
3. **Cada incidente abarata el siguiente.** No es una mejora puntual: es una
   curva. Las 9 lecciones de hoy son el piso de las 11 de mañana.

### Qué significa en la operación de un marketplace de autos

Las fallas que el sistema aprendió a atrapar no son errores de tipeo, son
dinero y confianza:

| Falla que V0 cometía | Qué cuesta en la operación |
|---|---|
| `USD $14,324` guardado como $14,324 MXN | publicar en 14 mil un auto de **265 mil** |
| `30k kms` → 30 km | ficha sin credibilidad, devolución, revisión manual |
| VIN con checksum inválido aceptado | inventario que no reconcilia con el registro real |
| El mismo VIN dado de alta dos veces | dos autos fantasma en inventario |
| «Listo» al cliente por un alta que falló | promesa incumplida que nadie detecta |

**Sobre nuestro banco de 60 casos:** la carga de corrección humana pasó de
**75 % de los anuncios (15/20 mal) a 5 % (1/20)**. Sobre los mismos casos, sin
intervención manual entre versiones.

> ⚠️ **Lo que NO afirmamos:** que eso sea el ahorro real de Kavak. Nuestro
> banco es sintético y lo decimos de frente. Lo que sí afirmamos, y está
> medido, es que **el mecanismo que produciría ese ahorro funciona, es
> atribuible lección por lección y se acumula.** Cambiar el banco sintético
> por los últimos 2,000 anuncios reales con su desenlace no requiere tocar una
> línea del loop — sólo `bench/`. Ver
> [docs/NUESTRA-PROPUESTA.md](docs/NUESTRA-PROPUESTA.md).

### Y lo que demuestra que entendimos la lógica, no sólo el resultado

Tres decisiones donde el número bonito y la lógica correcta iban en direcciones
opuestas, y elegimos la lógica:

1. **Tiramos un V1 que sacó 20/20.** Había arreglado bugs cuya lección el
   sistema aún no tenía, y una mejora sin lección que la respalde no se puede
   apagar ni atribuir: es un número sin evidencia detrás.
   ([D16](docs/DECISIONES.md))
2. **El sistema se negó a aprender dos fallas** mientras hubiera 38 casos de
   ruido, porque no podía atribuir la causa. Primero limpiar, después
   diagnosticar. ([FASE-03](docs/fases/FASE-03-observe-learn.md))
3. **No construimos V2**, aunque el comando existe. El único caso que V1 falla
   es precisamente una de las lecciones diferidas: lo que falta no es un hueco,
   es **la siguiente tarea ya nombrada por el propio sistema**.
   ([D17](docs/DECISIONES.md))

Un sistema que pasa todo en verde a la primera no tiene nada que enseñarte.
**Las fallas no son el accidente del proyecto: son la materia prima.**

---

## Empieza aquí

| Si quieres… | Lee |
|---|---|
| **entender qué pedo es todo esto, desde cero** | **[docs/ENTENDER.md](docs/ENTENDER.md)** ← empieza aquí |
| **nuestra propuesta, con la misma lupa** | [docs/NUESTRA-PROPUESTA.md](docs/NUESTRA-PROPUESTA.md) |
| dónde sirve este patrón y dónde no (los 5 jueces gratis) | [docs/CASOS-DE-USO.md](docs/CASOS-DE-USO.md) |
| saber si esto es un estándar, qué docs hay, y Codex vs Claude | [docs/ESTANDARES-Y-HERRAMIENTAS.md](docs/ESTANDARES-Y-HERRAMIENTAS.md) |
| el mapa del repo y las reglas del proyecto | [PROYECTO.md](PROYECTO.md) |
| **cada decisión grande y qué impacta** | [docs/DECISIONES.md](docs/DECISIONES.md) |
| la rúbrica oficial y cómo le respondemos | [docs/reto/RUBRICA.md](docs/reto/RUBRICA.md) |
| la guía oficial de la demo, aterrizada | [docs/reto/GUIA-DEMO-OFICIAL.md](docs/reto/GUIA-DEMO-OFICIAL.md) |
| la bitácora de cada paso con números reales | [docs/fases/](docs/fases/) |
| cómo trabajamos en git sin pisarnos | [docs/git-workflow.md](docs/git-workflow.md) |
| las reglas del hackathon | [intro.md](intro.md) |

## Correrlo (30 segundos, sin API key)

```bash
make bench      # genera 60 casos con respuesta conocida (semilla fija)
make v0         # corre el agente ingenuo  -> 5/20 en holdout
make observe    # ¿dónde falló exactamente?
make learn      # esas fallas -> 9 lecciones + 9 tests ROJOS
make test       # 0 verdes / 9 rojos  (nadie las heredó todavía)
make build      # Codex escribe V1 desde V0 + las lecciones
make test       # los mismos 9 tests, ahora VERDES
make v1         # medir V1 en holdout
make report     # la tabla comparativa
```

`make help` lista todos los comandos.

El motor de extracción por default es `stub`: regex deterministas, sin red ni
API key. Para usar un LLM de verdad: `--engine openai` con `OPENAI_API_KEY`.

## El ciclo, en un diagrama

```
   bench/cases.jsonl ──────────┐  (60 casos: 40 train / 20 holdout)
                               │
   agents/v0/agent.py ─────────┤
   (ingenuo, escrito a mano)   │
                               ▼
                     loop/observe.py        ¿qué falló, en qué campo, en qué caso?
                               │
                               ▼
                     loop/learn.py          lección + artefacto + TEST ROJO
                               │                    │
                               │                    └──► lessons/lessons.jsonl
                               ▼
                     loop/build.py ──► CODEX ──► agents/v1/agent.py
                                                 agents/common/tools/*.py
                               │
                               ▼
                     bench/score.py         5/20 ──► 19/20   (holdout, medido)
                               │
                               └──► (otra vuelta disponible: make build-v2)
```

**Resultado medido** sobre los 20 casos que el loop nunca vio:

| | V0 | V1 |
|---|---|---|
| Casos resueltos | **5/20** | **19/20** |
| Tests de lección verdes | 0/9 | **9/9** |
| Integridad | 0/2 | 0/2 |
| Único caso sin resolver | — | C056, VIN duplicado |

Y el ablation, verificado con 4 lecciones: apagar una sola tira el marcador a
16/20 y caen **exactamente** los casos que esa lección arreglaba, ni uno más.

> **Cerramos en V1 a propósito.** El caso que no resuelve es precisamente una
> de las dos lecciones que el sistema decidió diferir: lo que falta no es un
> hueco, es la siguiente tarea ya nombrada por el propio sistema. Detalle en
> [docs/DECISIONES.md](docs/DECISIONES.md) D17.

## Estado

| Fase | | Estado |
|---|---|---|
| [00](docs/fases/FASE-00-setup.md) | Setup y línea de corte | ✅ |
| [01](docs/fases/FASE-01-benchmark.md) | Banco de 60 casos + scorer | ✅ |
| [02](docs/fases/FASE-02-v0-extractor.md) | V0 ingenuo · línea base **5/20** | ✅ |
| [03](docs/fases/FASE-03-observe-learn.md) | Observar y aprender · **9 lecciones** | ✅ |
| [04](docs/fases/FASE-04-build-v1.md) | Codex construye V1 · **19/20** | ✅ |
| [06](docs/fases/FASE-06-ablation-demo.md) | Ablation verificado con 4 lecciones | ✅ |
| [05](docs/fases/FASE-05-build-v2.md) | Segunda iteración → V2 | ⏸️ no ejecutada, por decisión |

## Requisitos

Python 3.10+ y nada más para el camino crítico. Opcionales: `codex` CLI (para
que el sistema construya solo) y el paquete `openai` (para el motor LLM).
