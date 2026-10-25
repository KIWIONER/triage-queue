# 💻 Qué debes hacer

## Modelo de datos
- [x] Define una clase `Patient` (o dataclass) con al menos: `name`, `triage_level` (int, 1–3) y `arrived_at` (timestamp).
- [x] Define una clase `TriageQueue` que gestione internamente la lógica de cola de prioridad.

## Operaciones de cola
- [x] `enqueue(patient)` — añade un paciente; la posición en la cola debe respetar el nivel de triaje y el orden de llegada.
- [x] `dequeue()` — extrae y devuelve el siguiente paciente a ser atendido; debe lanzar un error descriptivo si la cola está vacía.
- [x] `peek()` — devuelve el siguiente paciente sin extraerlo.
- [x] `list_queue()` — devuelve todos los pacientes en espera en orden de atención como una lista.
- [x] `stats()` — devuelve un diccionario con el número de pacientes en espera por nivel de triaje.

## Interacción por CLI
- [x] Construye un menú de texto simple (en bucle) que permita a un usuario:
  - Añadir un nuevo paciente (solicitar nombre y nivel de triaje).
  - Llamar al siguiente paciente.
  - Ver la cola actual.
  - Ver estadísticas de la cola.
  - Salir.

## Correctitud y casos borde
- [x] Un paciente crítico (nivel 1) que llega mientras hay pacientes de nivel 2 y 3 esperando debe colocarse delante de ellos.
- [x] Dos pacientes con el mismo nivel de triaje deben atenderse en estricto orden de llegada.
- [x] Llamar a `dequeue()` o `peek()` sobre una cola vacía no debe romper el programa — gestiónalo con gracia.

## Notas de diseño (no se requiere código — incluye como comentarios o en un `DESIGN.md`)
- [x] Explica brevemente por qué elegiste tu estructura de datos interna frente a alternativas (p. ej., una sola `deque`, una lista ordenada, tres colas separadas).
- [x] Describe cómo gestionarías el caso en que un worker extrae un paciente de la cola en el mismo momento en que otro worker encola un nuevo paciente crítico. ¿En qué orden mutas el estado para evitar el doble procesamiento?

> ⚠️ **IMPORTANTE:** Usa únicamente la biblioteca estándar de Python (`collections.deque`, `heapq`, `datetime`). Sin paquetes externos.

---

## ✅ Qué vamos a evaluar
- [x] `TriageQueue` modela correctamente una cola de prioridad: nivel 1 siempre antes que nivel 2, nivel 2 siempre antes que nivel 3.
- [x] Dentro del mismo nivel de triaje, el orden FIFO se preserva estrictamente.
- [x] Las cinco operaciones (`enqueue`, `dequeue`, `peek`, `list_queue`, `stats`) están implementadas y funcionan correctamente.
- [x] Los casos borde están gestionados: desencolar/peek sobre cola vacía no rompe el programa; niveles de triaje duplicados se ordenan por llegada.
- [x] El código está organizado en clases con responsabilidades claras (sin lógica volcada en `main()`).
- [x] La nota de diseño explica la elección de la estructura de datos con una razón concreta.
- [x] La nota de diseño aborda el escenario de mutación concurrente, aunque sea de forma informal.
- [x] El bucle de CLI funciona y no rompe ante entradas inválidas.

> [!NOTE]
> La persistencia (guardar en archivo o base de datos) no es requerida y no será evaluada.
