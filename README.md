# Kavak Listing Autopilot — sistema de agentes auto-mejorante

Un sistema que **aprende de sus propias corridas** y usa lo aprendido para que
**Codex construya su versión siguiente**. El dominio: convertir anuncios sucios
de autos usados en fichas de inventario confiables.

RSI Hackathon · Kavak × OpenAI × Primero AI · 9 nov 2026

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
                     bench/score.py         5/20 → 16/20 → 19/20
                               │
                               └──► (otra vuelta) ──► agents/v2
```

## Estado

| Fase | | Estado |
|---|---|---|
| [00](docs/fases/FASE-00-setup.md) | Setup y línea de corte | ✅ |
| [01](docs/fases/FASE-01-benchmark.md) | Banco de 60 casos + scorer | ✅ |
| [02](docs/fases/FASE-02-v0-extractor.md) | V0 ingenuo · línea base **5/20** | ✅ |
| [03](docs/fases/FASE-03-observe-learn.md) | Observar y aprender · **9 lecciones** | ✅ |
| [04](docs/fases/FASE-04-build-v1.md) | Codex construye V1 | ⬜ |
| [05](docs/fases/FASE-05-build-v2.md) | Segunda iteración → V2 | ⬜ |
| [06](docs/fases/FASE-06-ablation-demo.md) | Ablation + demo | ⬜ |

## Requisitos

Python 3.10+ y nada más para el camino crítico. Opcionales: `codex` CLI (para
que el sistema construya solo) y el paquete `openai` (para el motor LLM).
