# ¿Esto es un estándar? ¿Y por qué Codex y no Claude?

> Las dos dudas que más ruido causan, respondidas con fuentes y con lo que
> verificamos en esta máquina el 9 nov 2026.

---

## La respuesta corta

1. **El reto NO es un estándar.** "Sistema de agentes que aprende de sus
   corridas y construye su sucesor" es una **línea de investigación activa**
   con nombres propios y papers, no una especificación con documentación
   oficial. Nadie publicó "el estándar RSI".
2. **Pero cada pieza suelta sí está estandarizada y documentada.** Benchmarks,
   evals, memoria del agente, instrucciones de repo, herramientas, CLIs no
   interactivos: todo eso tiene spec y docs.
3. **Codex no tiene nada especial para esto.** Es un agente de código que
   recibe texto y escribe archivos. Claude Code hace exactamente lo mismo. En
   este repo son **3 líneas** (`loop/build.py:BUILDERS`) y se cambia con un
   flag. Lo pide el hackathon porque lo organiza OpenAI y vale 25% de la
   calificación — no porque haga falta.

---

## 1. La parte que NO es estándar: la investigación

Lo que estamos construyendo tiene nombre en la literatura:

| Nombre | Qué propone | Relación con nuestro repo |
|---|---|---|
| **ADAS** (*Automated Design of Agentic Systems*, Hu et al.) | Trata el diseño de agentes como un problema de búsqueda: un **meta-agente** programa agentes nuevos en espacio de código abierto y mantiene un **archivo** de diseños encontrados | Nuestro `loop/build.py` **es** un meta-agente, muy chiquito y con repertorio acotado |
| **Darwin Gödel Machine** (Sakana AI + Jeff Clune, [arXiv:2505.22954](https://arxiv.org/pdf/2505.22954), ICLR 2026) | Un sistema que **modifica su propio código** y valida cada cambio contra benchmarks de código (SWE-bench, Polyglot); acumula un archivo de agentes generados | Es nuestro patrón llevado al extremo: ahí el sistema se reescribe a sí mismo, aquí escribe a su sucesor |
| **Reflexion** (Shinn et al., 2023) | El agente escribe en lenguaje natural una reflexión sobre su falla y la usa en el siguiente intento | Nuestro `loop/learn.py`, pero nosotros además la **materializamos en código y en un test** |
| **Voyager** (Wang et al., 2023) | Agente en Minecraft que acumula una **biblioteca de habilidades** (código reutilizable) que crece con la experiencia | `lessons/lessons.jsonl` + `agents/common/tools/` es exactamente una skill library |
| **Self-Refine / STaR** | Auto-crítica y auto-entrenamiento sobre las propias salidas correctas | La familia a la que pertenece todo esto |

> ⚠️ Honestidad sobre fuentes: ADAS y Darwin Gödel Machine los verifiqué con
> búsqueda hoy. Reflexion, Voyager, Self-Refine y STaR los cito de memoria —
> son papers conocidos de 2022-2023, pero si los vas a mencionar frente a
> alguien, busca la cita exacta.

**Una distinción que ese campo cuida y nosotros también:** en ADAS el diseñador
y el agente diseñado son piezas separadas. En la Darwin Gödel Machine es el
mismo sistema. Nosotros estamos en el primer grupo: `loop/` diseña, `agents/`
es diseñado. Si alguien te pregunta "¿tu sistema se modifica a sí mismo?", la
respuesta honesta es **no**: construye a su sucesor, que no es lo mismo.

---

## 2. La parte que SÍ es estándar y tiene documentación

Aquí está lo que puedes estudiar y reusar con confianza:

### AGENTS.md — instrucciones de repo para cualquier agente

Un archivo markdown en la raíz del repo que le dice al agente de código cómo
trabajar aquí (cómo correr tests, convenciones, qué no tocar). Nació como
convención de OpenAI para Codex y hoy es un proyecto multi-herramienta, bajo
gobernanza de la Linux Foundation según las fuentes que encontré. Lo leen
Codex, Cursor, Copilot, Gemini CLI, Windsurf, Zed y más.

> **Dato con asterisco:** sobre si **Claude Code** lee `AGENTS.md`, las fuentes
> se contradicen. Varias dicen que sí (como *fallback* cuando no hay
> `CLAUDE.md`), otras dicen que sólo lee `CLAUDE.md`. No lo pude confirmar
> contra la documentación oficial de Anthropic, así que **verifícalo antes de
> depender de ello**. Lo seguro: `CLAUDE.md` funciona en Claude Code y
> `AGENTS.md` en Codex; si quieres los dos, un symlink resuelve.

👉 **Para nuestro proyecto:** un `AGENTS.md` en la raíz sería *otra* forma de
persistir lecciones — las que aplican a cómo se escribe código aquí, en vez de
a cómo se parsean anuncios. Mismo patrón, otro nivel.

### MCP (Model Context Protocol)

El estándar para conectar herramientas y fuentes de datos a un agente. Si tus
lecciones se materializan en *herramientas* en lugar de reglas, MCP es el
formato en que se exponen. Lo soportan Claude, Codex y la mayoría.

### Skills (`SKILL.md`)

Carpetas con instrucciones + scripts que el agente carga cuando son relevantes.
Es memoria procedimental empaquetada. Documentado en
[code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills).

👉 **El paralelo exacto:** una lección nuestra (`regla` + `artifact` + `test`)
es conceptualmente un skill en miniatura.

### Evals

Medir con un banco fijo y casos apartados es práctica estándar, con producto
documentado de los dos lados (OpenAI tiene Evals API; Anthropic documenta
evaluación en sus docs). El vocabulario —*held-out*, *ground truth*,
*LLM-as-judge*, *ablation*— es el que ya usamos en
[ENTENDER.md §7](ENTENDER.md).

### CLIs no interactivos (lo que usa `loop/build.py`)

Esto es lo que hace posible que un script invoque un agente de código:

| | Codex | Claude Code |
|---|---|---|
| Comando | `codex exec "<prompt>"` | `claude -p "<prompt>"` |
| Docs | [developers.openai.com/codex/noninteractive](https://developers.openai.com/codex/noninteractive) | [code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless) |
| Permiso para escribir | `--sandbox workspace-write` | `--permission-mode acceptEdits` |
| Elegir modelo | `-m / --model` | `--model` |
| Salida estructurada | `--output-schema <FILE>` | `--output-format json` / `stream-json` |
| Reanudar sesión | `codex exec resume --last` | `--resume` (sesiones persistidas por default) |
| Directorio de trabajo | `-C / --cd <DIR>` | se corre desde el directorio |

---

## 3. Verificado en esta máquina (9 nov 2026)

No de memoria ni de blogs: corrido aquí.

```
codex-cli 0.150.0        ->  /Users/ee/.local/bin/codex
claude                   ->  /Users/ee/.local/bin/claude
```

| Hallazgo | Cómo lo verifiqué |
|---|---|
| ⚠️ **`codex exec --full-auto` NO existe** en 0.150.0 | `codex exec --help` — no aparece. Varios blogs de 2025 lo siguen citando. Nuestro `build.py` lo usaba y **habría tronado** |
| El flag correcto es `--sandbox workspace-write` | `codex exec --help` → `-s, --sandbox [read-only, workspace-write, danger-full-access]` |
| `codex exec` trae `resume`, `fork`, `review`, `--output-schema` | `codex exec --help` |
| Codex exige estar en un repo git (o `--skip-git-repo-check`) | documentado; por eso `git init` fue la FASE-00 |
| `claude -p --permission-mode` existe | `claude --help` |

**Lección práctica:** antes de confiar en un flag que viste en un blog, corre
`<cli> --help`. Las herramientas de agentes cambian de mes a mes y la mitad de
los tutoriales está desactualizada. Esto nos habría costado 20 minutos en
plena competencia.

---

## 4. Cómo cambiar de constructor, en la práctica

Todo el acoplamiento del sistema al agente de código vive aquí
(`loop/build.py`):

```python
BUILDERS = {
    "codex":  lambda prompt, model: ["codex", "exec", "--sandbox", "workspace-write", ...],
    "claude": lambda prompt, model: ["claude", "-p", "--permission-mode", "acceptEdits", ...],
}
```

Y se usa así:

```bash
python3 loop/build.py --from v0 --to v1                     # Codex (default)
python3 loop/build.py --from v0 --to v1 --builder claude     # Claude Code
```

**Pruébalo tú mismo:** construye V1 con Codex, bórralo, constrúyelo con Claude
Code, y corre `make test` las dos veces. Si los dos ponen los 9 tests en verde,
acabas de demostrar la tesis del proyecto: **el valor no está en el modelo,
está en el banco de casos, la evidencia y los tests.** El modelo es la pieza
intercambiable.

(Para el hackathon: usa Codex. Es 25% de la calificación y lo organiza OpenAI.
Pero ahora sabes *por qué* es intercambiable, que es lo que te sirve el martes.)

---

## 5. Qué leer, en orden

**Si quieres construir cosas (práctico):**
1. [Codex, modo no interactivo](https://developers.openai.com/codex/noninteractive) y su [referencia de CLI](https://developers.openai.com/codex/cli)
2. [Claude Code programático](https://code.claude.com/docs/en/headless) y [Skills](https://code.claude.com/docs/en/skills)
3. [agents.md](https://agents.md) — la convención de instrucciones de repo
4. Model Context Protocol — para exponer herramientas al agente

**Si quieres entender el campo (investigación):**
1. **Reflexion** — el ancestro simple: fallar, reflexionar, reintentar
2. **Voyager** — biblioteca de habilidades que se acumula (el papá de nuestro `lessons.jsonl`)
3. **ADAS** — el meta-agente que programa agentes
4. **[Darwin Gödel Machine](https://arxiv.org/pdf/2505.22954)** — el sistema que se reescribe a sí mismo y valida con benchmarks

**Lo que NO vas a encontrar:** una documentación oficial de "cómo construir un
sistema auto-mejorante". No existe. Lo que existe son los componentes, los
papers, y el criterio para pegarlos — y ese criterio es lo que está escrito en
[ENTENDER.md §6](ENTENDER.md) como receta de 6 preguntas.

---

## Fuentes

- [Darwin Gödel Machine — arXiv:2505.22954](https://arxiv.org/pdf/2505.22954) · [ResearchGate](https://www.researchgate.net/publication/392204438_Darwin_Godel_Machine_Open-Ended_Evolution_of_Self-Improving_Agents) · [anuncio de Jeff Clune](https://x.com/jeffclune/status/1928291576129933595)
- [ADAS — revisión en Preprints](https://www.preprints.org/frontend/manuscript/681d95e4c67e8f1c7370bbc8d39f887a/download_pub)
- [Codex — modo no interactivo](https://developers.openai.com/codex/noninteractive) · [Codex CLI](https://developers.openai.com/codex/cli)
- [Claude Code — ejecución programática](https://code.claude.com/docs/en/headless) · [Skills](https://code.claude.com/docs/en/skills) · [Glosario](https://code.claude.com/docs/en/glossary)
- AGENTS.md: [guía práctica](https://www.how2shout.com/ai/agents-md-file-guide.html) · [como estándar abierto](https://codex.danielvaughan.com/2026/04/07/agents-md-open-standard-cross-tool-portability) · [portabilidad con CLAUDE.md](https://codex.danielvaughan.com/2026/05/27/agent-instruction-files-agents-md-claude-md-cross-tool-portability-codex-cli/) · [soporte en Claude Code (no confirmado oficialmente)](https://runtimewire.com/article/claude-code-adds-agents-md-support)
- Flags de `codex exec`: verificados con `codex exec --help` en codex-cli 0.150.0. El reporte de que `--full-auto` ya no se acepta también aparece en [esta guía de 2026](https://codex.danielvaughan.com/2026/03/26/codex-cli-cicd-non-interactive/).
