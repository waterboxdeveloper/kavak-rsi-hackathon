# ¿Dónde sirve este patrón? Los 5 lugares donde vive un juez gratis

> La pregunta no es *"¿qué puede hacer la IA?"* — casi todo sí.
> La pregunta es: **¿qué me dice gratis si salió bien?**

Un caso de uso para un sistema que aprende **no** se define por lo interesante
de la tarea. Se define por si existe algo que ya te dice, sin discutir y sin
que un humano opine, si el resultado estuvo bien o mal.

A eso le llamamos **el juez gratis**. Si lo encuentras, tienes un loop. Si no,
tienes automatización normal: útil, pero en 6 meses va a ser igual de buena
que hoy.

Y resulta que el juez gratis vive en 5 lugares.

---

## 1️⃣ El futuro responde solo

Haces una predicción, el tiempo pasa, la realidad te contesta. **Nadie tuvo
que etiquetar nada**: el dataset se construye solo mientras el negocio opera.

| Caso | El juez |
|---|---|
| *"Este Jetta se vende en 23 días a $249k"* | a los 30 días: se vendió o no, y a cuánto |
| *"Este cliente se da de baja este mes"* | se fue o no |
| *"Esta tarea toma 3 días"* | tomó 8 |
| *"Estas 200 piezas se agotan en 2 semanas"* | el inventario real |
| *"Este lead va a cerrar"* | cerró o no |

Lo que se acumula son reglas del tipo *"en noviembre, los sedanes blancos
arriba de 120k km tardan 40% más de lo estimado"*.

**Costo:** hay que esperar. El loop gira a la velocidad de la realidad.

## 2️⃣ Un humano ya está corrigiendo

El más desperdiciado de todos. En cualquier empresa alguien corrige trabajo
todos los días, y esa corrección **se tira a la basura**.

| Caso | El juez |
|---|---|
| El agente de soporte **edita** la respuesta sugerida antes de enviarla | el diff entre lo sugerido y lo enviado |
| Contabilidad **reclasifica** facturas | la categoría final |
| El revisor **cambia** cosas en tu PR | lo que cambió = cómo se escribe código aquí |
| El jefe **corrige** la cotización | el documento final |
| El revisor **arregla** la traducción automática | el texto publicado |

El loop empieza por algo tonto: **guardar las correcciones.** Si tres veces
alguien movió "Pemex" de Insumos a Transporte, eso ya es una lección.

## 3️⃣ La máquina ya dice sí/no

El mejor juez que existe: binario, instantáneo, imposible de discutir.

| Caso | El juez |
|---|---|
| **Jobs, tests y deploys que se rompen** | el test pasa o no |
| **Scrapers** que se caen cuando el sitio cambia | el campo viene vacío o no |
| Integraciones con APIs ajenas | 200 o 400 |
| Extracción de datos de PDFs y facturas | el schema valida o no |
| Queries SQL generadas | corre o truena |
| Conciliación de pagos | cuadra o no cuadra |

> 🔑 **Los tests son ground truth gratis.** Un test que falla es una hoja de
> respuestas que ya existe y no tuviste que escribir.

El de los scrapers casi nadie lo hace bien: en vez de arreglar el selector
cada mes y olvidarlo, cada arreglo queda con un test que fija la página vieja
*y* la nueva. El conocimiento **se acumula** en lugar de reiniciarse.

## 4️⃣ Existe un registro canónico en otro lado

Hay una fuente de verdad contra la cual comparar. **Toda reconciliación es un
generador infinito de casos de prueba.**

| Caso | El juez |
|---|---|
| VIN, RFC, CURP, CLABE | tienen **dígito verificador** (ver `agents/common/vin.py`) |
| Inventario del sistema | el conteo físico |
| La contabilidad | el extracto bancario |
| La ficha del anuncio | el catálogo del fabricante |
| La dirección capturada | si existe en el mapa |
| Lo que dice el contrato | lo que está en el CRM |

**Éste es el que usamos en este proyecto.** Ver [NUESTRA-PROPUESTA.md](NUESTRA-PROPUESTA.md).

## 5️⃣ El usuario vota con sus acciones

No le preguntas si le gustó. Ves qué hizo.

| Caso | El juez |
|---|---|
| Respondiste un ticket | **lo reabrió** = estuvo mal |
| El bot atendió | pidió hablar con un humano = falló |
| Recomendaste un producto | lo devolvió |
| Mandaste el correo | no contestó |
| Publicaste el anuncio | nadie lo clickeó |

---

## ❌ Dónde NO funciona

Nada de esto es caso de uso para un loop:

> "que aprenda a escribir mejor copy" · "que mejore el diseño" · "que haga
> mejores resúmenes" · "que escriba código más elegante"

No porque sea difícil, sino porque **no hay juez**. Un LLM puede hacer esas
cosas hoy, pero no puede *aprender* a hacerlas mejor: no tiene cómo saber si
mejoró. Y si pones otro LLM a calificar, tienes dos modelos opinando y
alucinando en armonía.

### Pero el verificador a veces se puede fabricar

Esto es lo que separa a quien piensa bien de quien no:

| Suena inverificable | Hasta que lo conviertes en |
|---|---|
| "mejor copy" | **tasa de conversión en un A/B test** |
| "mejor diseño de formulario" | **% que lo completa** |
| "mejor resumen" | ¿la persona tuvo que abrir el documento original? |
| "código más elegante" | ¿cuántos comentarios recibió el PR? |

Convertir una opinión en un número medible **es** el trabajo. Es el 80% del
valor del proyecto, y es exactamente lo que hicimos con el banco de 60 casos.

---

## Tres casos aterrizados

**A · El agente que arregla sus propios jobs** — *una tarde*
| | |
|---|---|
| Tarea | un cron falla → lo diagnostica y lo arregla |
| Juez | el job vuelve a correr en verde |
| Se acumula | causa raíz + test de regresión. La misma falla no vuelve dos veces |

**B · Precio y días-en-piso de autos usados** — *un mes, pero es dinero real*
| | |
|---|---|
| Tarea | predecir precio de venta y días en inventario |
| Juez | a los 30 días, la venta real |
| Se acumula | reglas de estacionalidad, color, kilometraje, región |
| Ablation | apagas "la regla de noviembre" y el error vuelve a subir |

**C · Soporte que aprende de sus correcciones** — *dos semanas*
| | |
|---|---|
| Tarea | redactar la respuesta al ticket |
| Juez | doble: ¿el humano la editó? ¿el cliente reabrió? |
| Se acumula | política por tema |
| Métrica | % de respuestas enviadas sin editar |

---

## El filtro

> **¿Qué me dice gratis si salió bien?**
>
> Hay respuesta → hay loop. El sistema mejora solo con el tiempo.
> No hay respuesta → es un chatbot con `cron`. Útil, pero no aprende.
