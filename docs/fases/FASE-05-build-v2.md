# FASE-05 — Segunda iteración: V2 y el conocimiento acumulado

| | |
|---|---|
| **Estado** | ⏸️ **no ejecutada, por decisión del equipo** — ver abajo |
| **Depende de** | FASE-04 terminada (V1 verde) ✅ |

> ## ⏸️ Por qué esta fase no se ejecutó
>
> **Decisión deliberada, no falta de tiempo.** Cerrar en V1 demuestra que
> entendimos la lógica del ciclo mejor que inflar un número:
>
> El único caso que V1 no resuelve es el del **VIN duplicado** — que es
> exactamente una de las dos lecciones que el sistema **decidió diferir**, con
> su razón escrita en el log. Lo que falta no es un hueco: es **la siguiente
> tarea ya nombrada por el propio sistema.**
>
> Eso enseña algo más difícil que un marcador alto: **el sistema sabe lo que no
> sabe, y sabe por qué todavía no lo aprendió.**
>
> Todo lo de abajo está construido y listo (`make observe-v1`, `make build-v2`
> existen y funcionan). Sólo no se corrió. Cualquiera puede ejecutarlo y ver
> la segunda vuelta. Registro: [DECISIONES.md](../DECISIONES.md) D17.
>
> **Importante para la demo:** no afirmar ningún número de V2. El pitch cierra
> en V1 y lo dice explícitamente.

## Objetivo
Correr el loop **otra vez**, ahora sobre V1, para que aparezcan las dos
lecciones de proceso que quedaron diferidas, y que Codex construya V2 con las
**11 lecciones acumuladas**.

## Por qué esta fase existe

La rúbrica dice: *"Si el sucesor vuelve a aprender y crea otra versión:
mostrar **qué se acumuló**."* Eso es esta fase, y es la diferencia entre
"mejoramos un agente una vez" y "tenemos un sistema que aprende".

Lo bonito es que no la forzamos. En la FASE-03 el sistema se negó a aprender
las fallas de proceso porque había 38 casos de ruido de extracción encima. Con
V1 ese ruido ya no está, así que las dos fallas quedan aisladas y atribuibles:

| Falla | Qué pasó | Lección esperada |
|---|---|---|
| `duplicate_vin` | el mismo VIN en dos anuncios creó **dos autos** en inventario | buscar el VIN antes de dar de alta; marcar `duplicate` y no crear fila |
| `write_interrupted` | se confirmó un alta cuya escritura **falló** | confirmar **sólo después** de persistir; reintentar; si falla, `failed` sin confirmar |

La segunda es la más interesante para contar: el sistema le dijo "listo" a un
cliente por algo que nunca se guardó. Es un bug clásico de sistemas
distribuidos (*confirmar antes de persistir*) y el sistema lo encontró en su
propia bitácora, no porque se lo señaláramos.

## Comandos exactos
```bash
make observe-v1    # corre V1 en train, observa, y aprende L10 y L11
make test          # L10 y L11 nuevos y ROJOS; L1-L9 siguen verdes
make build-v2      # Codex construye V2 con las 11 lecciones
make test AGENT=v2 # los 11 deben quedar VERDES
make v2            # medir en holdout
make report        # la tabla de las 3 versiones + lecciones acumuladas
```

## Resultado esperado
| | V0 | V1 | V2 |
|---|---|---|---|
| holdout | 5/20 | ~16/20 | ~19/20 |
| integridad | 0/2 | 0/2 | **2/2** |
| lecciones activas | 0 | 9 | **11** |

El salto de V1 a V2 en *casos* es chico (3) pero el de **integridad es 0/2 →
2/2**, y ése es el que vale la historia: V2 no lee mejor, **trabaja mejor**.
Pasó de un agente que extrae datos a un agente con integridad transaccional.

## Qué hace que esto sea "acumulación" y no "reemplazo"

Hay que poder enseñarlo, no sólo decirlo:

```bash
make test AGENT=v2    # los 11 tests verdes: V2 conserva L1-L9 Y añade L10-L11
```

Si V2 hubiera olvidado alguna lección vieja, su test estaría rojo. **Los tests
viejos son el candado contra la regresión**, que es justo lo que la gente
pierde cuando "le vuelve a pedir al modelo que lo haga mejor".

---

## ⬇️ A llenar al terminar

**Hora:** · **Commits:**

**Las dos lecciones nuevas, tal como las escribió el sistema:**
```json
```

**Salida de `make test AGENT=v2`:**
```
```

**Salida de `make v2`:**
```
```

**Intervención humana:**

**Qué salió mal / qué aprendimos:**

## Siguiente
[FASE-06 — ablation y demo](FASE-06-ablation-demo.md)
