# FASE-00 — Setup, reglas del juego y línea de corte

| | |
|---|---|
| **Estado** | ✅ hecha |
| **Fecha** | 9 nov 2026 |
| **Commits** | ver `git log --oneline` desde el primer commit |

## Objetivo
Repo con git, estructura de carpetas, Makefile y las reglas escritas antes de
teclear lógica. Y dejar por escrito **qué trajimos vs. qué construimos hoy**.

## Por qué
La rúbrica (criterio 4) pide explícitamente: *"Si usaron una base previa: decir
qué trajeron y qué construyeron durante el hackathon."* Si eso no está escrito
con hora y commit, en la demo se vuelve una respuesta dudosa. Con esto es un
hecho verificable en el `git log`.

## Línea de corte

**Lo que trajimos (base previa):** nada. El repo nació hoy, commit inicial
incluido. Lo único preexistente es `intro.md`, que es el material que entregó
la organización.

**Lo que construimos hoy:** todo lo demás — benchmark, V0, el loop de 3 pasos,
el scorer, el runner, el reporte y la documentación por fases.

> Si el equipo reutiliza algo de otro proyecto, **anotarlo aquí con el commit
> exacto en que entró.** No después.

## Comandos exactos
```bash
git init && git branch -M main
mkdir -p bench agents/{v0,common/tools} loop lessons runs tests docs/{fases,decisiones,demo}
make help          # lista todos los comandos del proyecto
```

## Decisiones tomadas en esta fase

1. **Dominio: ingesta de anuncios de autos usados.** Es el negocio de Kavak y
   los jueces incluyen gente de Kavak. Un dominio genérico (todo list, scraper)
   cuesta lo mismo de construir y puntúa menos en Impacto.
2. **Datos sintéticos con defectos inyectados.** La organización no da
   datasets. Generarlos nosotros nos da algo mejor que datos reales: sabemos
   la respuesta correcta de cada caso Y sabemos qué defecto tiene, así que
   podemos decir "la lección L5 arregló exactamente estos 8 casos".
3. **Python stdlib, sin dependencias.** En un hackathon de 10 horas, pelearse
   con `pip` en 4 laptops distintas es tiempo perdido. `openai` es opcional.
4. **Un `.md` por fase.** No es burocracia: es el guion de la demo
   escribiéndose solo. A las 7 p.m. el guion ya existe.

## Intervención humana
Toda. Esta fase es 100% nuestra; el sistema todavía no existe.

## Siguiente
[FASE-01 — el banco de casos](FASE-01-benchmark.md). Es la fase más importante:
sin vara de medir, el resto del proyecto no se puede demostrar.
