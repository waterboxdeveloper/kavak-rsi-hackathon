# Git — cómo trabajamos sin pisarnos

Reglas cortas, pensadas para 2-4 personas trabajando el mismo día sobre el
mismo repo. Si una regla te está costando más tiempo del que te ahorra,
sáltatela y anótalo.

---

## 1. Ramas

```
main                      siempre corre. Nunca se rompe.
  └── fase/04-build-v1    una rama por fase
  └── fase/05-build-v2
```

```bash
git switch -c fase/04-build-v1      # empezar
# ...trabajar, commitear...
git switch main && git merge --no-ff fase/04-build-v1
```

`--no-ff` deja un commit de merge visible, así el historial cuenta la historia
por fases en vez de ser una lista plana. En la demo eso se agradece.

**`main` siempre debe correr.** La regla práctica: antes de mergear,
`make clean && make demo` tiene que terminar sin error.

## 2. Mensajes de commit

Formato [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<ámbito>): <qué cambió, en imperativo, minúsculas>

<por qué. Esta parte es la que importa.>
```

Tipos que usamos: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.
Ámbitos: `bench`, `agents`, `loop`, `lessons`, `demo`.

**El cuerpo explica el POR QUÉ, no el qué.** El qué ya está en el diff. El por
qué se pierde para siempre si no lo escribes. Ejemplo real de este repo:

```
feat(bench): banco de 60 casos con defectos inyectados y scorer determinista

40 train / 20 holdout. El loop solo ve los train; los holdout son el número
que se presenta. Semilla fija: el banco de hoy es idéntico al de mañana.

Scoring campo a campo, cero juez-LLM: un LLM calificando vuelve el resultado
opinable justo cuando el jurado pide rigor.
```

Dentro de 3 meses, ese commit te va a ahorrar media hora de arqueología.

## 3. Qué se versiona y qué no

| Se versiona | Por qué |
|---|---|
| `bench/cases.jsonl` | es la vara de medir; tiene que ser idéntica para todos |
| `lessons/lessons.jsonl` | **es la memoria del sistema.** El `git log` de este archivo *es* la historia del aprendizaje |
| `tests/` | los candados de cada lección |
| `agents/v1`, `v2` | el producto del sistema; hay que poder auditar qué escribió Codex |
| `runs/evidencia/` | sólo las corridas que citamos en la demo |

| NO se versiona | Por qué |
|---|---|
| `runs/*` | se regenera con `make demo`; es ruido |
| `.env`, llaves | obvio, y está en `.gitignore` |
| `__pycache__/`, `.venv/` | basura de Python |

Dato bonito: `git log --oneline -- lessons/lessons.jsonl` es la línea de tiempo
del aprendizaje del sistema. Eso se puede enseñar en la demo.

## 4. Commits especiales del proyecto

Dos casos que conviene distinguir del resto del historial:

**Cuando el sistema genera lecciones:**
```
feat(lessons): L10 y L11 aprendidas de las fallas de proceso de V1

Generadas por `make observe-v1`. NO escritas a mano.
Evidencia: runs/v1-train.failures.json
```

**Cuando Codex escribe una versión:**
```
feat(agents): V1 construido por Codex desde V0 + 9 lecciones

Prompt: runs/build-prompt-v0-to-v1.md
Intervención humana: ninguna / <describir exactamente qué>
Resultado: holdout 5/20 -> 16/20. 9/9 tests de lección en verde.
```

Decir en el commit si hubo intervención humana no es trámite: la rúbrica
(criterio 4) pide distinguir acciones del sistema vs. del equipo, y con esto
la respuesta es verificable en el historial en vez de ser nuestra palabra.

## 5. Antes de cada merge a main

```bash
git status --short bench/ lessons/ tests/ agents/v0/   # ¿Codex tocó la vara de medir?
make clean && make demo                                 # ¿main sigue corriendo?
```

El primero importa de verdad: el prompt de construcción le prohíbe a Codex
tocar esas carpetas, pero un modelo atorado toma atajos. Si cambió algo ahí,
`git checkout` a esos paths y volver a construir.

## 6. GitHub (cuando se cree el remoto)

```bash
gh repo create kavak-rsi-hackathon --private --source=. --remote=origin --push
```

Privado por default. La propiedad intelectual es del equipo (ver `intro.md`),
así que publicarlo es una decisión a tomar después, no por accidente.

Si se usan PRs, el cuerpo lleva: qué fase, los números antes/después, y qué
hizo el sistema vs. el equipo.

## 7. Una sola cosa que no se negocia

> **El banco de casos y los tests no se editan para que algo pase.**

Si un test falla, se arregla el agente. El día que alguien ajuste el examen
para que la calificación suba, el proyecto entero deja de significar nada — y
lo peor es que no te vas a dar cuenta hasta que alguien te lo pregunte en
público.
