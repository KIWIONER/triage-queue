# 📐 Documento de Diseño: Sistema de Triaje Hospitalario

Este documento justifica las decisiones técnicas tomadas en la implementación de la cola de prioridad de triaje ([triage_queue.py](file:///c:/Users/balsa/triage-queue/triage_queue.py)) y describe la estrategia recomendada para entornos concurrentes.

---

## 1. Elección de la Estructura de Datos Interna

Para gestionar la cola de triaje con tres niveles de prioridad (1: Crítico, 2: Urgente, 3: Estándar) respetando estrictamente el orden de llegada (FIFO) dentro de cada nivel, se eligió una arquitectura basada en **tres colas independientes implementadas con `collections.deque`** dentro de un diccionario `{1: deque(), 2: deque(), 3: deque()}`.

### Comparativa frente a alternativas

| Estructura | Enqueue | Dequeue | Preservación FIFO | Complejidad / Overhead |
| :--- | :---: | :---: | :---: | :--- |
| **Tres colas (`collections.deque`) [Elegida]** | **$O(1)$** | **$O(1)$** | **Nativa y garantizada** | **Mínima:** Código simple, sin overhead de ordenación ni contadores. |
| **Montículo binario (`heapq`)** | $O(\log n)$ | $O(\log n)$ | Requiere contador auxiliar | **Media:** Requiere empaquetar tuplas `(prioridad, contador_llegada, paciente)` para evitar comparaciones directas entre instancias. |
| **Lista única ordenada (`list`)** | $O(n)$ | $O(1)$ o $O(n)$ | Requiere búsqueda lineal/binaria | **Alta:** Insertar en orden desplaza elementos en memoria en tiempo lineal $O(n)$. |
| **Una sola `collections.deque`** | $O(n)$ | $O(1)$ | Requiere recorrerla | **Alta:** Una `deque` solo es rápida en sus extremos ($O(1)$ en extremos, pero $O(n)$ para insertar en medio ante prioridades mixtas). |

### Razones concretas de la elección:
1. **Rendimiento óptimo ($O(1)$ amortizado):** `enqueue` es una operación directa `append()` sobre la cola correspondiente ($O(1)$). `dequeue` solo itera sobre las 3 claves fijas y ejecuta un `popleft()` ($O(1)$).
2. **Garantía natural de FIFO:** Al ser una cola de doble extremo basada en listas doblemente enlazadas por bloques, los pacientes dentro de un mismo nivel se atienden exactamente en el orden en que llegaron sin necesidad de comparar marcas de tiempo ni mantener secuencias numéricas.
3. **Claridad y mantenibilidad:** La separación semántica por niveles hace que las operaciones de consulta (`stats`, `peek`, `list_queue`) sean directas e intuitivas.

---

## 2. Gestión de Concurrencia y Mutación de Estado

### Escenario planteado
Un worker extrae un paciente (`dequeue`) simultáneamente mientras otro worker encola a un nuevo paciente crítico de nivel 1 (`enqueue`).

### Problemas potenciales
- **Doble procesamiento:** Dos workers obtienen el mismo paciente si leen la cola antes de que el otro la actualice.
- **Inversión de prioridad / Condición de carrera:** El paciente crítico entrante podría perder su turno si el estado no se sincroniza atómicamente.

### Estrategia de sincronización y orden de mutación

Para garantizar la consistencia en un entorno multihilo o distribuido:

1. **Sección crítica atómica mediante cerrojos (Locks):**
   - Utilizar un cerrojo exclusivo (`threading.Lock` en Python, o un cerrojo distribuido como Redis Redlock si los workers están en nodos distintos).

2. **Orden estricto de mutación en la extracción (`dequeue`):**
   1. **Adquirir el cerrojo:** El worker solicita acceso exclusivo a la estructura de colas.
   2. **Inspeccionar y extraer inmediatamente de la cola:** 
      - Se localiza al paciente con mayor prioridad actual.
      - Se remueve atómicamente de la cola (`deque.popleft()`).
      - *(Opcional en sistemas distribuidos)*: Se registra al paciente en una tabla/colección con estado `EN_ATENCION` junto al ID del worker.
   3. **Liberar el cerrojo:** En cuanto el paciente ha sido removido de la cola visible, se libera el cerrojo inmediatamente para que otros workers (y quienes encolan) puedan continuar sin bloqueo prolongado.
   4. **Procesar la atención médica:** La atención del paciente ocurre **fuera del cerrojo**. De este modo, ningún otro worker podrá volver a ver o extraer a ese paciente (evitando 100% el doble procesamiento).

3. **Orden de mutación en la inserción (`enqueue`):**
   1. **Adquirir el cerrojo.**
   2. **Añadir el paciente a la cola correspondiente (`deque.append()`).**
   3. **Liberar el cerrojo.**

### Tolerancia a fallos
Si el worker falla o se desconecta mientras atiende al paciente (tras haberlo extraído de la cola), un monitor de *heartbeat* o un mecanismo de *timeout* devuelve al paciente al inicio de su cola correspondiente (`deque.appendleft()`) o a una cola de reintentos (*Dead-Letter Queue*), garantizando que no se pierda la atención.
