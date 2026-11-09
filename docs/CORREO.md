# Correo y mensajes para compartir el proyecto

> **Principio:** lo que hace que un correo así pegue no son los adjetivos, son
> los números verificables. *"Entendemos de OPEX"* se lo escribe cualquiera;
> *"la carga de corrección humana pasó de 75 % a 5 % y aquí está el repo"* no.
>
> Por eso cada afirmación de abajo trae su número o su link, y cada número
> trae su límite.

---

## Versión larga · correo

**Asunto:** RSI Hackathon · Kavak Listing Autopilot — un loop que aprende de la operación

Hola [nombre]:

Les comparto lo que construimos en el RSI Hackathon, y sobre todo el
razonamiento detrás, que es la parte que nos interesa que vean.

**No construimos un agente. Construimos la maquinaria que permite que un
agente mejore solo.** Un sistema que observa sus propias ejecuciones, convierte
cada falla en una lección persistida con su prueba automática, y entrega esas
lecciones a Codex para que escriba la versión siguiente. Codex no fue nuestro
copiloto: fue el órgano de construcción del sistema.

**El objetivo del hackathon, entendido como un ciclo y no como un entregable.**
El reto pedía un sistema que aprenda de sus ejecuciones y construya un sucesor
funcional. Nos enfocamos en lo que hace que eso sea verificable: un banco fijo
de 60 casos con 20 apartados que el sistema nunca ve al aprender, calificación
determinista campo a campo sin ningún LLM opinando, y cada lección detrás de un
interruptor para poder apagarla y comprobar que la mejora vino de ahí. Sobre
los 20 casos apartados: **de 5/20 a 19/20, con los 9 tests de lección en
verde.**

**Uso eficiente de los recursos.** Diez horas, cero dependencias externas en el
camino crítico — el proyecto corre con Python de fábrica, sin instalar nada,
reproducible con un comando. No nos dieron datasets, así que fabricamos uno
donde conocemos la respuesta de cada caso **y el defecto que tiene**, lo cual
nos permite afirmar que una lección específica arregló exactamente ciertos
casos y ninguno más. Lo verificamos con cuatro lecciones distintas y las cuatro
dan atribución exacta.

**Y lo que más nos importa: el negocio.** Pedirle código a un agente reduce el
costo de construir algo una vez. Un loop que aprende de la operación reduce el
costo de operarlo todos los días. Esa es la diferencia entre CAPEX y OPEX, y es
donde creemos que está el valor real de esta tecnología.

Las fallas que el sistema aprendió a atrapar no son errores de tipeo. Son un
auto de 265 mil pesos publicado en 14 mil por una moneda mal leída. Un VIN que
no reconcilia con el registro. El mismo auto dado de alta dos veces. Un "listo"
al cliente por un alta que nunca se guardó. Hoy eso lo absorbe una persona
revisando, lo corrige y lo olvida, y la semana siguiente vuelve a ocurrir. **El
loop convierte cada incidente en un validador permanente con su prueba de
regresión: el costo de esa clase de falla baja y se queda abajo.** Sobre nuestro
banco, la carga de corrección humana pasó del 75 % de los anuncios al 5 %,
sobre los mismos casos y sin intervención manual entre versiones.

Lo decimos con su límite: nuestro banco es sintético y no afirmamos que ése sea
el ahorro de Kavak. Lo que sí está medido es que el mecanismo funciona, es
atribuible lección por lección y se acumula. Sustituir los casos sintéticos por
los últimos 2,000 anuncios reales con su desenlace no requiere tocar una línea
del loop.

Tres decisiones que explican mejor el proyecto que cualquier número:

1. **Tiramos una versión que sacó 20/20.** Había arreglado fallas cuya lección
   el sistema aún no tenía. Una mejora sin lección que la respalde no se puede
   apagar ni atribuir, y entonces no es evidencia.
2. **El sistema se negó a aprender dos fallas** mientras hubiera 38 casos de
   ruido, porque no podía atribuir la causa. Primero limpiar, después
   diagnosticar.
3. **Cerramos en la versión 1 a propósito.** El único caso que no resuelve es
   precisamente una de las lecciones que el propio sistema decidió diferir. Lo
   que falta no es un hueco: es la siguiente tarea, ya nombrada por el sistema.

Un sistema que pasa todo en verde a la primera no tiene nada que enseñarte. Las
fallas no son el accidente del proyecto: son la materia prima.

Todo es público y reproducible:

- Repositorio: https://github.com/waterboxdeveloper/kavak-rsi-hackathon
- El ciclo de evaluación, paso a paso: https://claude.ai/artifact/VdgCLRpAZNjrDVJQwUuKpW

Quedo con gusto para platicarlo.

[nombre]
[puesto] · opino.tech

---

## Versión corta · LinkedIn, DM o seguimiento

> En el RSI Hackathon de Kavak y OpenAI no construimos un agente: construimos
> la maquinaria que hace que un agente mejore solo. Observa sus propias
> ejecuciones, convierte cada falla en una lección con su prueba automática, y
> Codex escribe la versión siguiente.
>
> Sobre 20 casos que el sistema nunca vio al aprender: de 5/20 a 19/20. Y la
> parte que nos importa: tiramos una versión que sacó 20/20 porque había
> arreglado fallas cuya lección no existía todavía, y una mejora sin evidencia
> detrás no sirve.
>
> Pedirle código a un agente baja el costo de construir una vez. Un loop que
> aprende de la operación baja el OPEX para siempre. Ahí está el valor.
>
> Repo público: github.com/waterboxdeveloper/kavak-rsi-hackathon

---

## Cómo ajustarlo según a quién va

| Destinatario | Qué subir al frente | Qué recortar |
|---|---|---|
| **Organizadores / jurado** | el ciclo, el ablation, las tres decisiones | la parte de OPEX puede ir más corta: ya conocen el reto |
| **Alguien de Kavak (operación o producto)** | la tabla de qué cuesta cada falla, y el OPEX | el detalle técnico del loop |
| **Reclutador o inversionista** | las tres decisiones y el límite declarado | los nombres de archivos y comandos |
| **Alguien técnico** | el contrato del constructor y la frontera | la justificación de negocio |

**Dos reglas al adaptarlo:**

1. **Nunca quitar el límite que va junto al dato.** El "75 % → 5 %" sin la
   frase de que el banco es sintético deja de ser creíble en el momento en que
   alguien pregunta de dónde salió.
2. **No agregar cifras que no estén en `runs/*.score.json`.** Todo número de
   este correo es rastreable a un archivo del repo. Esa es la razón por la que
   funciona.
