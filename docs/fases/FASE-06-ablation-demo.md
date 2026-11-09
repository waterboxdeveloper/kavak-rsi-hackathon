# FASE-06 — Ablation y demo

| | |
|---|---|
| **Estado** | ⬜ pendiente |
| **Depende de** | V2 funcionando |

## Objetivo
Probar que la mejora vino **de las lecciones** y no de la suerte, y dejar la
demo ensayada con cronómetro.

## Parte A · Ablation: la prueba de causalidad

"Subimos de 5/20 a 19/20" es una anécdota. Esto es una afirmación causal:

```bash
make ablate L=L5 V=v2     # apaga la lección de millas → km
make ablate L=L10 V=v2    # apaga el dedupe por VIN
```

Resultado esperado al apagar **L5**: los 8 casos de `odo_miles` vuelven a
fallar. **Exactamente ésos, ni uno más.** Y al apagar **L10**:
`no_duplicate_inventory` vuelve a 0/1.

Funciona porque cada lección vive detrás de un interruptor en el código:

```python
if "L5" in lessons:
    km = convertir_millas(texto)
```

> **Verificar antes de la demo:** que el delta de casos coincida con el conteo
> de ese defecto en `bench/cases.jsonl`. Si al apagar una lección se caen
> *más* casos de los que esa lección arreglaba, hay acoplamiento entre
> lecciones y hay que decirlo (o arreglarlo). Un ablation que no cuadra es un
> hallazgo real, no un detalle cosmético.

Esto es la respuesta directa a la pregunta que el jurado tiene casi
garantizada: *"¿cómo aislaron el efecto del cambio?"*

## Parte B · La demo de 3 minutos

El guion detallado está en [`docs/demo/guion-3min.md`](../demo/guion-3min.md).
Lo esencial:

| Tiempo | Qué |
|---|---|
| 0:00–0:40 | El problema en una frase. Correr V0. Señalar `USD $14,324 → $14,324 MXN`. |
| 0:40–1:45 | Abrir `lessons/lessons.jsonl`. Enseñar el prompt que recibió Codex. Enseñar los tests pasando de rojo a verde. |
| 1:45–3:00 | La tabla de las 3 versiones. **Ablation en vivo.** Cerrar con cómo se usó Codex. |

### Checklist antes de presentar

- [ ] `make clean && make demo` corre de principio a fin sin error
- [ ] Todos los scores están regenerados (nada viejo en `runs/`)
- [ ] Copiar a `runs/evidencia/` las corridas que se van a citar (ese folder
      sí se versiona)
- [ ] Terminal con letra grande; una sola ventana; sin pestañas de más
- [ ] Los 3 archivos que se abren en vivo, ya abiertos en pestañas:
      `lessons/lessons.jsonl`, `tests/test_lesson_L5.py`,
      `runs/build-prompt-v0-to-v1.md`
- [ ] Ensayado **3 veces con cronómetro**. A los 3:00 cortan.
- [ ] Decidido quién habla y quién teclea (dos personas, no una)
- [ ] Las 4 respuestas de `PROYECTO.md §6` repartidas y memorizadas

### Para los 2 minutos de preguntas, a la mano

1. una corrida → `runs/v0-holdout.json`
2. la lección que salió de ella → `lessons/lessons.jsonl` línea 1
3. el cambio que heredó el sucesor → `git show` del commit de V1
4. qué sigue fallando → la última sección de `make report`

**Si algo truena en vivo:** hay scores guardados en `runs/evidencia/`. Se
muestra el archivo y se sigue. Nunca depurar en vivo.

---

## ⬇️ A llenar al terminar

**Salida de los ablations:**
```
```

**¿Cuadró el delta con el conteo de defectos?**

**Tiempos de los 3 ensayos:**

**Qué preguntó el jurado y qué contestamos:**
