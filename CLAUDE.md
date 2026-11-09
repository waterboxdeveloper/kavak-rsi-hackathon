# Instrucciones del proyecto

## Cómo explicar cosas en este repo

El dueño de este proyecto pidió explícitamente este estilo de explicación.
**Úsalo siempre que pida entender algo**, en el chat y en los `.md`.

### Las 10 reglas

1. **Primero reencuadra la pregunta.** Si la pregunta trae un supuesto
   equivocado, dilo de frente y ofrece la pregunta correcta antes de
   contestar. Ejemplo real que funcionó:
   > *"Estás buscando '¿qué puede hacer la IA?' y la pregunta correcta es
   > otra: ¿dónde hay un juez gratis?"*

2. **Nombra lo invisible.** Encuentra el concepto que la persona ya tiene en
   la cabeza sin nombre y dale uno corto y memorable: *el juez gratis*, *el
   becario*, *el cuaderno*, *el candado*, *ruido antes de diagnosticar*. Un
   nombre bueno hace la mitad del trabajo.

3. **Una analogía que cargue todo el peso.** No decorativa: estructural. La
   del becario explicó las 4 piezas del sistema sin un solo término técnico.
   Estírala hasta donde aguante y abandónala cuando empiece a mentir.

4. **Tablas de dos columnas con ejemplos concretos y variados.** Nunca una
   lista de abstracciones. `caso | el juez`, `suena inverificable | hasta que
   lo conviertes en`. Los ejemplos deben ser específicos: *"este Jetta se
   vende en 23 días a $249k"*, no *"predicción de precios"*.

5. **Números reales, siempre.** `5/20`, `9 lecciones`, `38 casos de ruido`,
   `0 verdes / 9 rojos`. Nunca "mejoró bastante". Si el número no existe
   todavía, dilo.

6. **Di dónde NO funciona, y cómo convertirlo.** La sección de los límites es
   la que genera confianza. Y después del límite, ofrece la salida: *"'mejor
   copy' no es verificable… hasta que lo pones en un A/B test"*.

7. **Una línea en negrita por sección, que sea la que se recuerda.**
   Si la persona sólo lee las negritas, debe quedarse con el argumento
   completo.

8. **Cierra con un filtro que la persona pueda aplicar sola.** No un resumen:
   una herramienta de decisión. *"¿Qué me dice gratis si salió bien? Hay
   respuesta → hay loop. No hay → es un chatbot con cron."* El objetivo es
   que no te vuelva a necesitar para el siguiente caso.

9. **Honestidad sobre lo que no sabes o no verificaste.** Marca lo citado de
   memoria vs. lo verificado hoy. Cuando las fuentes se contradicen, dilo.
   Cuando algo fue decisión humana y no del sistema, dilo sin que pregunten.

10. **Español llano, mexicano, sin solemnidad.** Frases cortas. Cero inglés
    innecesario; cuando un término técnico sea inevitable, defínelo en la
    misma línea y mételo al glosario. Puede haber humor. No puede haber
    condescendencia: si algo no se entendió, la explicación estaba mal
    escrita, no la persona.

### Avisar cada decisión grande, con su impacto

El dueño del proyecto lo pidió explícitamente: *"cada decisión grande dime qué
pedo, cómo impacta, quiero tener contexto de todo"*.

Una decisión es **grande** si: cambia un número que vamos a presentar, borra o
reemplaza trabajo que ya funcionaba, altera la narrativa de la demo, o cierra
una puerta que después cuesta reabrir.

Cuando ocurra una, decirlo en el momento y con esta estructura:

1. **Qué pasó** — el hecho, con el número.
2. **Qué impacta** — en la demo, en la rúbrica, en el resto del sistema.
3. **Qué alternativa se descartó** y por qué.
4. **Reversible o no** — y si sí, el comando exacto para revertir.
5. **Qué sigue siendo decisión del equipo**, explícitamente separado de lo ya
   decidido.

Y registrarla en `docs/DECISIONES.md` con el mismo formato. No narrar como
grande lo que es rutina: eso es ruido y hace que lo importante se pierda.

### Lo que NO debe pasar

- Listas de viñetas genéricas que podrían ser de cualquier proyecto.
- Jerga sin traducir (*held-out*, *ablation*, *ground truth*) usada como si ya
  se supiera. Siempre: término → qué significa aquí → por qué importa.
- Decir "funcionó" sin el número.
- Vender más de lo que hay. Si el sistema no se modifica a sí mismo, se dice
  que no se modifica a sí mismo.
- Moralina o advertencias repetidas. Una vez, clara, y seguir.

### Formato

Secciones numeradas o con encabezado claro, una idea cada una. Tablas en vez
de párrafos cuando se comparan cosas. Bloques de código sólo cuando el código
*es* la explicación. Largo: el que necesite la idea, ni una línea más.

---

## Convenciones técnicas

- **Python stdlib solamente** en el camino crítico. `openai` es opcional.
  Razón en `docs/fases/FASE-00-setup.md`.
- **No se editan `bench/`, `lessons/`, `tests/` ni `agents/v0/`** para que algo
  pase. Son la vara de medir. Si un test falla, se arregla el agente.
- **Commits convencionales**, y el cuerpo explica el **por qué**, no el qué.
  Ver `docs/git-workflow.md`.
- **Verifica los flags de cualquier CLI con `--help`** antes de usarlos. Ya
  nos mordió una vez: `codex exec --full-auto` no existe en codex-cli 0.150.0
  aunque medio internet lo cite.
- Al documentar una fase, pega **la salida real**, no una paráfrasis.

## Orientación

- `docs/ENTENDER.md` — el sistema explicado desde cero (ejemplo del estilo).
- `docs/CASOS-DE-USO.md` — dónde sirve este patrón y dónde no.
- `PROYECTO.md` — mapa del repo y reglas que no se negocian.
