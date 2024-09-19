import csv
from datetime import datetime


class Tarea:
    def __init__(self, descripcion, fecha_vencimiento=None, completada=False, prioridad="baja"):
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.completada = completada
        self.prioridad = prioridad

    def marcar_como_completada(self):
        self.completada = True

    def mostrar_tarea(self):
        estado = "Completada" if self.completada else "Pendiente"
        fecha = f"Fecha límite: {self.fecha_vencimiento}" if self.fecha_vencimiento else "Sin fecha límite"
        return f"{self.descripcion} - {estado} - {fecha} - Prioridad: {self.prioridad}"


class SistemaGestionTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def listar_tareas(self, filtro=None):
        tareas_filtradas = self.tareas
        if filtro == "completadas":
            tareas_filtradas = [t for t in self.tareas if t.completada]
        elif filtro == "pendientes":
            tareas_filtradas = [t for t in self.tareas if not t.completada]

        for i, tarea in enumerate(tareas_filtradas):
            print(f"{i + 1}. {tarea.mostrar_tarea()}")

    def marcar_como_completada(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].marcar_como_completada()
        else:
            print("Índice de tarea inválido.")

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
        else:
            print("Índice de tarea inválido.")

    def guardar_en_archivo(self, nombre_archivo="tareas.csv"):
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            for tarea in self.tareas:
                escritor.writerow([tarea.descripcion, tarea.fecha_vencimiento, tarea.completada, tarea.prioridad])

    def cargar_desde_archivo(self, nombre_archivo="tareas.csv"):
        try:
            with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                self.tareas = []
                for fila in lector:
                    descripcion, fecha_vencimiento, completada, prioridad = fila
                    self.tareas.append(Tarea(descripcion, fecha_vencimiento, completada == 'True', prioridad))
        except FileNotFoundError:
            print("Archivo no encontrado. Se iniciará con una lista de tareas vacía.")

    def editar_tarea(self, indice, nueva_descripcion, nueva_fecha_vencimiento=None):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].descripcion = nueva_descripcion
            self.tareas[indice].fecha_vencimiento = nueva_fecha_vencimiento
        else:
            print("Índice de tarea inválido.")

    def ordenar_por_fecha(self):
        self.tareas.sort(
            key=lambda x: datetime.strptime(x.fecha_vencimiento, "%Y-%m-%d") if x.fecha_vencimiento else datetime.max)

    def asignar_prioridad(self, indice, prioridad):
        if 0 <= indice < len(self.tareas):
            if prioridad in ["alta", "media", "baja"]:
                self.tareas[indice].prioridad = prioridad
            else:
                print("Prioridad inválida. Use 'alta', 'media' o 'baja'.")
        else:
            print("Índice de tarea inválido.")


# Ejemplo de uso
if __name__ == "__main__":
    sistema = SistemaGestionTareas()
    sistema.cargar_desde_archivo()

    while True:
        print("\n--- Sistema de Gestión de Tareas ---")
        print("1. Añadir tarea")
        print("2. Listar tareas")
        print("3. Marcar tarea como completada")
        print("4. Eliminar tarea")
        print("5. Editar tarea")
        print("6. Ordenar tareas por fecha")
        print("7. Asignar prioridad a una tarea")
        print("8. Guardar y salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            descripcion = input("Ingrese la descripción de la tarea: ")
            fecha = input("Ingrese la fecha límite (YYYY-MM-DD) o deje en blanco: ")
            fecha = fecha if fecha else None
            sistema.agregar_tarea(Tarea(descripcion, fecha))
        elif opcion == "2":
            filtro = input("Filtrar por (todas/completadas/pendientes): ")
            sistema.listar_tareas(filtro if filtro in ["completadas", "pendientes"] else None)
        elif opcion == "3":
            indice = int(input("Ingrese el índice de la tarea a completar: ")) - 1
            sistema.marcar_como_completada(indice)
        elif opcion == "4":
            indice = int(input("Ingrese el índice de la tarea a eliminar: ")) - 1
            sistema.eliminar_tarea(indice)
        elif opcion == "5":
            indice = int(input("Ingrese el índice de la tarea a editar: ")) - 1
            nueva_descripcion = input("Ingrese la nueva descripción: ")
            nueva_fecha = input("Ingrese la nueva fecha límite (YYYY-MM-DD) o deje en blanco: ")
            sistema.editar_tarea(indice, nueva_descripcion, nueva_fecha if nueva_fecha else None)
        elif opcion == "6":
            sistema.ordenar_por_fecha()
            print("Tareas ordenadas por fecha.")
        elif opcion == "7":
            indice = int(input("Ingrese el índice de la tarea: ")) - 1
            prioridad = input("Ingrese la prioridad (alta/media/baja): ")
            sistema.asignar_prioridad(indice, prioridad)
        elif opcion == "8":
            sistema.guardar_en_archivo()
            print("Tareas guardadas. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")