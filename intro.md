# RSI Hackathon — Kavak × OpenAI × Primero AI
**Self-Improving AI Systems** · Lo que SÍ importa para competir

---

## Datos rápidos

| | |
|---|---|
| **Fecha** | Lunes 9 de noviembre de 2026 |
| **Horario** | 10:00 a.m. – 8:00 p.m. (10 horas, hora CDMX) |
| **Lugar** | Capital Reforma, Av. Paseo de la Reforma 250, Col. Juárez, Cuauhtémoc, CDMX |
| **Equipos** | 2 a 4 integrantes |
| **Formato de evaluación** | **3 min de demo + 2 min de preguntas** |
| **Jueces** | Panel que incluye a OpenAI |

---

## El reto

> Construir un **sistema de agentes que aprenda de sus propias ejecuciones** y use lo aprendido para **construir un sistema sucesor funcional**.

En la demo hay que mostrar:
1. **Qué cambió** entre versiones.
2. **Qué efecto tuvo** ese cambio.

---

## Rúbrica (4 criterios × 25 %)

### 1. Impacto — 25 %
- Explicar **quién se beneficia**, **qué problema resuelve** y **por qué importa**.
- Medir un resultado que tenga sentido para ese problema (ej. errores por lote, casos resueltos, tiempo de revisión).
- **Qué mostrar:** versión inicial vs. sucesora **sobre los mismos casos de evaluación**.
- Si pueden: **reservar casos que el sistema no vio al aprender** (held-out) y explicar **qué sigue fallando**.

### 2. Aplicación de Codex — 25 %
- Contar **cómo usaron Codex** en el proyecto.

### 3. Uso creativo de habilidades — 25 %
- Explicar cómo diseñaron el **ciclo de aprendizaje**:
  - Qué **señal** permitió detectar una falla.
  - Cómo se **guardó la lección**.
  - Cómo se **incorporó al construir el sucesor**.
- **Qué mostrar:** una **lección concreta** que cambie el comportamiento del sucesor. Puede vivir en una prueba, una herramienta, una regla o un cambio en el flujo.
- Si el sucesor vuelve a aprender y crea otra versión: mostrar **qué se acumuló**.

### 4. Demostración y presentación — 25 %
- Que sea fácil seguir la secuencia: **falla → decisión del sistema → resultado de la siguiente versión**.
- **Distinguir** acciones del sistema vs. intervenciones del equipo.
- **Qué mostrar:** correr un caso representativo, enseñar el cambio que produjo el sistema y hacer visible el **antes y después**.
- Si usaron una base previa: decir **qué trajeron** y **qué construyeron durante el hackathon**.

---

## Guion de la demo (3:00)

> Se puede usar cualquier problema que permita ver el ciclo completo. Una falla bien explicada + una comparación clara bastan.

| Tiempo | Qué hacer |
|---|---|
| **0:00 – 0:40** · Versión inicial | Presentar el problema en **una frase**. Correr el caso, **señalar dónde se rompe** y qué resultado esperaban. Enseñar el registro/salida/prueba que hace visible la falla. |
| **0:40 – 1:45** · Qué aprendió y qué construyó | Abrir la **lección guardada** y señalar **qué parte del sucesor cambió** por ella. Mostrar al sucesor haciendo su tarea. Si hubo intervención humana, decir **en qué punto**. |
| **1:45 – 3:00** · Comparar resultados | Correr las versiones **sobre los mismos casos de evaluación** y explicar qué se atribuye a la lección. **Cerrar contando cómo usaron Codex.** |

### Para los 2 min de preguntas
Tener a mano:
- Una **ejecución**.
- La **lección** que salió de ella.
- El **cambio que heredó** el sucesor.

Preguntas probables del jurado:
- ¿Cómo **aislaron el efecto** del cambio?
- ¿**Qué haría fallar** la última versión?

---

## Ejemplo de referencia (de la guía oficial): pedidos → reembolsos

1. **Versión inicial.** El agente de pedidos recibe dos veces el evento E-17 y crea dos registros. Detecta la repetición y guarda una **regla de deduplicación por ID**. Al re-correr el evento, la prueba muestra si el duplicado se resolvió.
2. **Primer sucesor.** El sistema usa esa regla para construir un **agente de devoluciones**. Evita duplicados, pero al interrumpirse una escritura descubre otra falla: **confirmó una devolución que nunca se guardó**.
3. **Segundo sucesor.** El agente de devoluciones usa esa evidencia para construir un **agente de reembolsos**: conserva la deduplicación y **confirma solo después de guardar**.
4. **Resultado:** en un banco común de **6 casos**, las tres versiones resuelven **2 → 4 → 6**. Si **desactivan una lección, vuelve la falla** correspondiente (ablation).

**Patrón a copiar:** falla observable → lección persistida → sucesor que la hereda → benchmark fijo con mejora medible → ablation que prueba causalidad.

---

## Recursos durante el evento
- **APIs de OpenAI** (acceso durante el evento).
- **Mentores de OpenAI y expertos de Kavak** en formato *stand-up*: sin cita, rotan por el espacio. Se les puede pedir preguntas técnicas, de arquitectura o estrategia, revisión rápida del enfoque y aclaraciones del reto/criterios. Tiempo limitado → llevar **preguntas concretas**.
- WiFi y electricidad.
- Comida completa (desayuno, comida, cena, snacks, café).

## Lo que NO dan
- **Datasets** → usar datos **públicos, sintéticos o propios**.
- Laptops / equipo.
- Transporte u hospedaje.

## Requisitos para entrar hoy
- INE o pasaporte vigente.
- Laptop y cargador.
- NDA y Aviso de Privacidad firmados (enviados antes o impresos el día del evento).

---

## Premios (efectivo + ChatGPT Pro 200 con Codex, por integrante)

| Lugar | Efectivo (se divide entre el equipo) | ChatGPT Pro 200 |
|---|---|---|
| 🥇 1.º | $50,000 MXN | 6 meses c/u |
| 🥈 2.º | $20,000 MXN | 3 meses c/u |
| 🥉 3.º | $10,000 MXN | 1 mes c/u |

## Propiedad intelectual (resumen)
- **El código es 100 % suyo.** Kavak y OpenAI no lo usan, reproducen, modifican ni comercializan.
- Solo pueden usar nombre, descripción, video y slides del proyecto para promoción (con atribución).

