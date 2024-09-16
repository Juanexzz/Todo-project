import csv
from datetime import datetime
from enum import Enum

class Priority(Enum):
    LOW = "baja"
    MEDIUM = "media"
    HIGH = "alta"

class Task:
    def __init__(self, description, due_date=None, priority=Priority.MEDIUM):
        self.description = description
        self.due_date = due_date
        self.completed = False
        self.priority = priority

    def mark_as_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completada" if self.completed else "Pendiente"
        due_date = f", Fecha límite: {self.due_date}" if self.due_date else ""
        return f"{self.description} - Estado: {status}{due_date}, Prioridad: {self.priority.value}"

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, due_date=None, priority=Priority.MEDIUM):
        task = Task(description, due_date, priority)
        self.tasks.append(task)
        print("Tarea añadida con éxito.")

    def list_tasks(self):
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")

    def complete_task(self, index):
        if 1 <= index <= len(self.tasks):
            self.tasks[index-1].mark_as_completed()
            print("Tarea marcada como completada.")
        else:
            print("Índice de tarea inválido.")

    def delete_task(self, index):
        if 1 <= index <= len(self.tasks):
            del self.tasks[index-1]
            print("Tarea eliminada con éxito.")
        else:
            print("Índice de tarea inválido.")

    def save_tasks(self):
        with open('tasks.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for task in self.tasks:
                writer.writerow([task.description, task.due_date, task.completed, task.priority.value])
        print("Tareas guardadas en el archivo.")

    def load_tasks(self):
        try:
            with open('tasks.csv', 'r') as file:
                reader = csv.reader(file)
                self.tasks = []
                for row in reader:
                    description, due_date, completed, priority = row
                    task = Task(description, due_date, Priority(priority))
                    task.completed = completed.lower() == 'true'
                    self.tasks.append(task)
            print("Tareas cargadas desde el archivo.")
        except FileNotFoundError:
            print("No se encontró el archivo de tareas. Se iniciará con una lista vacía.")

    def filter_tasks(self, status):
        filtered = [task for task in self.tasks if task.completed == (status.lower() == "completed")]
        for i, task in enumerate(filtered, 1):
            print(f"{i}. {task}")

    def edit_task(self, index, new_description, new_due_date=None):
        if 1 <= index <= len(self.tasks):
            task = self.tasks[index-1]
            task.description = new_description
            task.due_date = new_due_date
            print("Tarea actualizada con éxito.")
        else:
            print("Índice de tarea inválido.")

    def sort_by_date(self):
        # Separar tareas con y sin fecha de vencimiento
        tasks_with_date = [task for task in self.tasks if task.due_date]
        tasks_without_date = [task for task in self.tasks if not task.due_date]

        # Ordenar tareas con fecha de vencimiento
        tasks_with_date.sort(key=lambda x: datetime.strptime(x.due_date, "%Y-%m-%d"))

        # Mostrar tareas ordenadas
        print("Tareas ordenadas por fecha de vencimiento:")
        for i, task in enumerate(tasks_with_date, 1):
            print(f"{i}. {task}")

        # Mostrar tareas sin fecha de vencimiento al final
        if tasks_without_date:
            print("\nTareas sin fecha de vencimiento:")
            for i, task in enumerate(tasks_without_date, len(tasks_with_date) + 1):
                print(f"{i}. {task}")

        # Actualizar la lista de tareas con el nuevo orden
        self.tasks = tasks_with_date + tasks_without_date

    def set_priority(self, index, priority):
        if 1 <= index <= len(self.tasks):
            try:
                self.tasks[index-1].priority = Priority(priority.lower())
                print(f"Prioridad de la tarea establecida a {priority}.")
            except ValueError:
                print("Prioridad inválida. Use 'alta', 'media' o 'baja'.")
        else:
            print("Índice de tarea inválido.")

def main():
    manager = TaskManager()
    manager.load_tasks()

    while True:
        command = input("Ingrese un comando (add/list/complete/delete/filter/edit/sort/priority/save/exit): ").lower()

        if command == "add":
            desc = input("Descripción de la tarea: ")
            date = input("Fecha límite (YYYY-MM-DD) o presione Enter para omitir: ")
            date = date if date else None
            manager.add_task(desc, date)

        elif command == "list":
            manager.list_tasks()

        elif command == "complete":
            index = int(input("Índice de la tarea a completar: "))
            manager.complete_task(index)

        elif command == "delete":
            index = int(input("Índice de la tarea a eliminar: "))
            manager.delete_task(index)

        elif command == "filter":
            status = input("Estado a filtrar (completed/pending): ")
            manager.filter_tasks(status)

        elif command == "edit":
            index = int(input("Índice de la tarea a editar: "))
            new_desc = input("Nueva descripción: ")
            new_date = input("Nueva fecha límite (YYYY-MM-DD) o presione Enter para omitir: ")
            new_date = new_date if new_date else None
            manager.edit_task(index, new_desc, new_date)

        elif command == "sort":
            manager.sort_by_date()

        elif command == "priority":
            index = int(input("Índice de la tarea: "))
            priority = input("Nueva prioridad (alta/media/baja): ")
            manager.set_priority(index, priority)

        elif command == "save":
            manager.save_tasks()

        elif command == "exit":
            manager.save_tasks()
            print("¡Hasta luego!")
            break

        else:
            print("Comando no reconocido. Intente de nuevo.")

if __name__ == "__main__":
    main()