from dataclasses import dataclass, field
from datetime import datetime
from collections import deque

@dataclass
class Patient:
    name: str
    triage_level: int
    arrived_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.triage_level not in (1, 2, 3):
            raise ValueError("El nivel de triaje debe ser 1, 2 o 3.")

class TriageQueue:
    def __init__(self):
        self._queues = {
            1: deque(),
            2: deque(),
            3: deque()
        }

    def is_empty(self) -> bool:
        return all(len(q) == 0 for q in self._queues.values())

    def __len__(self) -> int:
        return sum(len(q) for q in self._queues.values())

    def enqueue(self, patient: Patient) -> None:
        if not isinstance (patient, Patient):
            raise TypeError("Se esperaba una instancia de Patient. ")
        self._queues[patient.triage_level].append(patient)

    def dequeue(self) -> Patient:
        for level in (1, 2, 3):
            if self._queues[level]:
                return self._queues[level].popleft()
        raise IndexError("la cola de triaje está vacía. No hay pacientes por atender.")

    def peek(self) -> Patient:
        for level in (1, 2, 3):
            if self._queues[level]:
                return self._queues[level][0]
        raise IndexError("La cola de triaje está vacía. No hay pacientes en espera.")

    def list_queue(self) -> list[Patient]:
        result = []
        for level in (1, 2, 3):
            result.extend(self._queues[level])
        return result

    def stats(self) -> dict[int, int]:
        return {level: len(self._queues[level]) for level in (1, 2, 3)}


class TriageCLI:
    def __init__(self, queue: TriageQueue | None = None):
        self.queue = queue if queue is not None else TriageQueue()
    def display_menu(self) -> None:
        print("\n=== SISTEMA DE TRIAJE HOSPITALARIO ===")
        print("1. Añadir nuevo paciente")
        print("2. Llamar al siguiente paciente")
        print("3. Ver la cola actual")
        print("4. Ver estadísticas de la cola")
        print("5. Salir")
    def handle_add_patient(self) -> None:
        name = input("Nombre del paciente: ").strip()
        if not name:
            print("⚠️ El nombre no puede estar vacío.")
            return
        level_input = input("Nivel de triaje (1: Crítico, 2: Urgente, 3: Estándar): ").strip()
        try:
            level = int(level_input)
            patient = Patient(name=name, triage_level=level)
            self.queue.enqueue(patient)
            print(f"✅ Paciente '{patient.name}' añadido con prioridad {patient.triage_level}.")
        except ValueError:
            print("⚠️ Nivel inválido. Debe ser un número entero entre 1 y 3.")
    def handle_call_patient(self) -> None:
        try:
            patient = self.queue.dequeue()
            print(f"📢 Llamando a: {patient.name} | Triaje: {patient.triage_level} | Llegada: {patient.arrived_at.strftime('%H:%M:%S')}")
        except IndexError as err:
            print(f"ℹ️ {err}")
    def handle_view_queue(self) -> None:
        patients = self.queue.list_queue()
        if not patients:
            print("ℹ️ La cola está vacía.")
            return
        print("\n--- Pacientes en espera (orden de atención) ---")
        for i, p in enumerate(patients, start=1):
            print(f"{i}. {p.name} (Nivel {p.triage_level}) - Llegada: {p.arrived_at.strftime('%H:%M:%S')}")
    def handle_view_stats(self) -> None:
        stats = self.queue.stats()
        total = len(self.queue)
        print("\n--- Estadísticas de la cola ---")
        print(f"Total en espera: {total}")
        print(f" - Nivel 1 (Crítico): {stats[1]}")
        print(f" - Nivel 2 (Urgente): {stats[2]}")
        print(f" - Nivel 3 (Estándar): {stats[3]}")
    def run(self) -> None:
        while True:
            self.display_menu()
            choice = input("Selecciona una opción (1-5): ").strip()
            if choice == "1":
                self.handle_add_patient()
            elif choice == "2":
                self.handle_call_patient()
            elif choice == "3":
                self.handle_view_queue()
            elif choice == "4":
                self.handle_view_stats()
            elif choice == "5":
                print("👋 Saliendo del sistema de triaje. ¡Hasta luego!")
                break
            else:
                print("⚠️ Opción no válida. Por favor, selecciona un número del 1 al 5.")
def main():
    cli = TriageCLI()
    cli.run()
if __name__ == "__main__":
    main()
