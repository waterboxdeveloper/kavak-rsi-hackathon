# FASE-04 — Codex construye V1

| | |
|---|---|
| **Estado** | ⬜ pendiente (es el siguiente paso) |
| **Archivos** | `loop/build.py` → genera `agents/v1/agent.py` y `agents/common/tools/*` |

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

## ⬇️ A llenar al terminar

**Hora:** · **Commit:** · **Intentos de Codex:**

**Salida real de `make test`:**
```
```

**Salida real de `make v1`:**
```
```

**¿Qué escribió Codex exactamente?** (`git show --stat`)

**¿Tocó algo prohibido?**

**Intervención humana:**

**Qué salió mal / qué aprendimos:**

## Siguiente
[FASE-05 — segunda iteración → V2](FASE-05-build-v2.md)
