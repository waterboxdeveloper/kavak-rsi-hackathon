# FASE-04 — Codex construye V1

| | |
|---|---|
| **Estado** | ✅ hecha, en dos intentos |
| **Archivos** | `agents/v1/agent.py` + `agents/common/tools/{odometer,money,validators}.py` |
| **Commits** | `68b99b3` primer intento (se pasó de listo) · `82ad0e0` reconstrucción |
| **Resultado** | holdout **5/20 → 19/20** · tests de lección **0/9 → 9/9 verdes** |

## Objetivo
Que **Codex**, no nosotros, escriba el agente sucesor a partir del código de
V0 más las 9 lecciones, y que los 9 tests rojos se pongan verdes.

## Por qué esta fase es el criterio "Aplicación de Codex" (25%)

La respuesta que vamos a dar al jurado es ésta, y el código la respalda:

> *Codex no es nuestro copiloto, es el órgano de construcción del sistema.
> `loop/build.py` le entrega el código del predecesor y las lecciones que el
> sistema aprendió de sus propias corridas, y Codex escribe el sucesor
> completo. V0 y el loop son nuestros; V1 y V2 son de Codex.*

Casi todos los equipos van a decir "usamos Codex para programar más rápido".
Esa respuesta vale la mitad.

## Qué recibe Codex

`build.py` arma un prompt con cuatro bloques (se guarda en
`runs/build-prompt-v0-to-v1.md`, **enseñarlo en la demo**):

1. **El contrato** — firma, formato del record, y la regla no negociable:
   cada comportamiento aprendido va envuelto en `if "Lx" in lessons:`.
2. **El código completo de V0.**
3. **Las utilidades que ya existen** y debe reutilizar (`vin.py`,
   `constants.py`, los métodos del store).
4. **Las 9 lecciones**, cada una con su disparador, evidencia, regla,
   artefacto y el id con el que debe envolverse.

Y el criterio de éxito explícito:

```
RSI_AGENT=v1 python3 run_tests.py
python3 agents/run.py --version v1 --split holdout && python3 bench/score.py runs/v1-holdout.json
```

## Lo que NO debe tocar

El prompt lo prohíbe explícitamente: `bench/`, `lessons/`, `tests/` y
`agents/v0/`. Son la vara de medir. Si el constructor pudiera editar el examen
o los tests, el resultado no significaría nada — y es exactamente el atajo que
un modelo toma cuando se atora.

> ⚠️ **Verificar esto siempre después de un build:**
> ```bash
> git status --short bench/ lessons/ tests/ agents/v0/   # debe salir vacío
> ```
> Si Codex tocó algo de ahí, `git checkout` a esos paths y volver a construir.
> Y si pasó, **decirlo en la demo**: es un hallazgo interesante, no una
> vergüenza.

## Comandos exactos
```bash
make build                                   # invoca `codex exec`
# alternativas:
python3 loop/build.py --from v0 --to v1 --print-prompt   # sólo ver el prompt
make test                                    # los 9 deben quedar VERDES
make v1                                      # medir en holdout
make report                                  # la tabla comparativa
```

## Plan B (si Codex se atora)

1. **Segundo intento** con el prompt tal cual. Los modelos varían entre
   corridas; a veces basta.
2. **Pegar el prompt a mano** en Codex web / ChatGPT:
   `cat runs/build-prompt-v0-to-v1.md`.
3. **Construir sólo las herramientas** (`odometer.py`, `money.py`,
   `validators.py`) con Codex y escribir a mano el ensamblado en
   `agents/v1/agent.py`.

> En los casos 2 y 3 hay intervención humana. **Hay que decirlo en la demo**
> y anotarlo abajo. La rúbrica pide distinguir acciones del sistema vs. del
> equipo; un equipo que lo declara se ve más sólido, no más débil.

## Resultado esperado
| | V0 | V1 esperado |
|---|---|---|
| holdout | 5/20 | ~16/20 |
| tests de lección | 0/9 verdes | 9/9 verdes |
| integridad | 0/2 | 0/2 (todavía) |

Que la integridad siga en 0/2 **es correcto**: V1 no sabe nada de las fallas
de proceso, porque esas lecciones quedaron diferidas en la FASE-03. Ésa es la
puerta a la FASE-05.

---

## ✅ Resultado real

**Intentos de Codex: 2.** El primero se pasó de listo.

### Intento 1 — `68b99b3` · descartado aunque sacó 20/20

Codex escribió los 4 archivos con las 9 guardas de ablation correctas y **no
tocó la vara de medir**. Pero implementó además el dedupe por VIN y el
confirm-after-save, o sea las lecciones **L10 y L11 que estaban diferidas y no
venían en el prompt**. Resultado: holdout 20/20, integridad 2/2.

Lo descartamos, y hay que poder explicar por qué un número mejor fue peor:

| Problema | Consecuencia |
|---|---|
| No queda nada que V2 pueda aprender | se cae la cadena y el criterio de acumulación |
| Esos 2 comportamientos no tienen interruptor | no se pueden apagar ni atribuir → mejora sin evidencia |
| Salto de 5/20 a 20/20 de un golpe | frente a un jurado técnico eso genera sospecha, no aplauso |

**Causa raíz, y fue nuestra:** el prompt protegía la vara de medir
(`bench/`, `lessons/`, `tests/`) pero **no protegía la evidencia**. Nunca dijo
"no implementes nada que no tenga lección".

### El arreglo — sección FRONTERA en `loop/build.py`

> *"Si detectas otros bugs en el predecesor, DÉJALOS INTACTOS. No son
> descuidos: son fallas que el sistema todavía no ha aprendido, y arreglarlas
> antes de que exista su lección destruye la evidencia."*

### Intento 2 — `82ad0e0` · el bueno

Verificado en el código, no de palabra:

- `grep find_by_vin agents/v1/agent.py` → **0 resultados** (no deduplica)
- `store.confirm()` en la línea 83, `store.save()` en la 85 → **conservó el bug
  de proceso de V0 aunque lo tenía enfrente**
- 9 guardas `if "Lx" in lessons:` → una por lección
- `git status --short bench/ lessons/ tests/ agents/v0/` → **vacío**

**Salida de `make test`:**
```
== tests de leccion (agente bajo prueba: v1) ==
  VERDE L1 ... VERDE L9
  9 verdes / 0 rojos
```

**Salida de `make v1`:**
```
== v1  (split=holdout) ==
  casos resueltos : 19/20
    holdout       : 19/20  <- el numero que presentamos
  integridad      : 0/2
    [FALLA] no_duplicate_inventory {'7JJHHPGG2VFBFF9JC': ['C043', 'C056']}
    [FALLA] no_phantom_confirmation ['C051']
```

### El detalle que hace a esta fase

**El único caso que V1 no resuelve es `C056`: VIN duplicado.** Y las dos
fallas de integridad que quedan son exactamente las dos lecciones diferidas.

Lo que falta es precisamente lo que el sistema ya identificó como su siguiente
lección. **La frontera funcionó.**

## Intervención humana

Dos, y en puntos exactos:

1. **Escribimos la sección FRONTERA** del contrato, después de ver el primer
   intento. Ningún sistema nos lo pidió.
2. **Borramos el V1 del primer intento** y relanzamos el build.

El código de V1 lo escribió Codex en los dos casos. Nosotros no editamos una
línea de `agents/v1/agent.py` ni de las herramientas.

## Qué salió mal / qué aprendimos

**Un constructor obediente no es lo mismo que un constructor acotado.** Codex
incluso *avisó* que no iba a tocar las fallas de proceso — y las tocó. La
lección no es "el modelo miente": es que **un contrato tiene que prohibir
explícitamente lo que no quieres**, porque lo que no está prohibido se vuelve
una optimización razonable desde el punto de vista del constructor.

Eso aplica a cualquier agente con permiso de escribir código.

## Siguiente
[FASE-05 — segunda iteración → V2](FASE-05-build-v2.md)
