"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: main.py

Descripción:
Punto de entrada del Simulador de Asignación de Memoria. Presenta
un menú interactivo por consola que permite configurar la memoria,
elegir la estrategia de asignación (First Fit, Best Fit, Worst Fit),
cargar procesos desde un archivo de entrada, crear/liberar procesos
manualmente y visualizar el estado de la memoria en todo momento.
==============================================================
"""

from __future__ import annotations
from typing import Optional

from core.gestor_memoria import GestorMemoria
from core.lector_archivo import LectorArchivo
from algorithms.first_fit import FirstFit
from algorithms.best_fit import BestFit
from algorithms.worst_fit import WorstFit
from models.proceso import Proceso


# Tamaño de memoria por defecto (en KB), usado si el usuario no
# configura uno distinto al iniciar el programa.
TAMANO_MEMORIA_POR_DEFECTO = 1000

# Mapeo de nombres visibles a las clases de estrategia disponibles.
# Todas comparten la misma interfaz elegir_bloque(bloques_libres, proceso),
# por lo que intercambiarlas aquí es trivial.
ESTRATEGIAS = {
    "1": ("First Fit", FirstFit),
    "2": ("Best Fit", BestFit),
    "3": ("Worst Fit", WorstFit),
}


def mostrar_menu_principal() -> None:
    print("\n" + "=" * 50)
    print("  SIMULADOR DE ASIGNACIÓN DE MEMORIA")
    print("=" * 50)
    print("1. Configurar memoria (tamaño total)")
    print("2. Seleccionar estrategia de asignación")
    print("3. Cargar procesos desde archivo")
    print("4. Crear proceso manualmente")
    print("5. Liberar proceso")
    print("6. Ver estado de la memoria")
    print("7. Salir")
    print("=" * 50)


def configurar_memoria() -> GestorMemoria:
    """Solicita al usuario el tamaño total de memoria a simular."""
    entrada = input(
        f"Tamaño total de memoria en KB "
        f"(Enter para usar {TAMANO_MEMORIA_POR_DEFECTO}KB por defecto): "
    ).strip()

    tamano = TAMANO_MEMORIA_POR_DEFECTO if entrada == "" else int(entrada)
    gestor = GestorMemoria(tamano_total=tamano)
    print(f"Memoria configurada con {tamano}KB.")
    return gestor


def seleccionar_estrategia():
    """Solicita al usuario elegir una de las tres estrategias disponibles."""
    print("\nEstrategias disponibles:")
    for clave, (nombre, _) in ESTRATEGIAS.items():
        print(f"  {clave}. {nombre}")

    opcion = input("Elija una estrategia: ").strip()

    if opcion not in ESTRATEGIAS:
        print("Opción inválida. Se mantiene la estrategia actual.")
        return None

    nombre, clase_estrategia = ESTRATEGIAS[opcion]
    print(f"Estrategia seleccionada: {nombre}")
    return clase_estrategia


def cargar_procesos_desde_archivo(gestor: GestorMemoria, estrategia) -> None:
    """Lee procesos desde un archivo de texto y los asigna en orden."""
    ruta = input("Ruta del archivo de entrada: ").strip()

    try:
        procesos = LectorArchivo.leer_procesos(ruta)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error al leer el archivo: {error}")
        return

    for proceso in procesos:
        asignar_proceso(gestor, estrategia, proceso)


def crear_proceso_manual(gestor: GestorMemoria, estrategia) -> None:
    """Solicita al usuario los datos de un proceso nuevo y lo asigna."""
    id_proceso = input("Id del proceso (ej: P1): ").strip()
    tamano_texto = input("Tamaño solicitado en KB: ").strip()

    try:
        tamano = int(tamano_texto)
        proceso = Proceso(id_proceso=id_proceso, tamano=tamano)
    except ValueError as error:
        print(f"Datos inválidos: {error}")
        return

    asignar_proceso(gestor, estrategia, proceso)


def asignar_proceso(gestor: GestorMemoria, estrategia, proceso: Proceso) -> None:
    """
    Aplica la estrategia seleccionada para elegir un bloque y asigna
    el proceso a la memoria. Informa al usuario si no hay memoria
    suficiente disponible en este momento.
    """
    bloques_libres = gestor.obtener_bloques_libres()
    bloque_elegido = estrategia.elegir_bloque(bloques_libres, proceso)

    if bloque_elegido is None:
        print(
            f"No hay memoria disponible para el proceso {proceso.id} "
            f"({proceso.tamano}KB). Asignación rechazada."
        )
        return

    try:
        gestor.crear_proceso(proceso, bloque_elegido)
        print(f"Proceso {proceso.id} asignado correctamente.")
    except (ValueError, RuntimeError) as error:
        print(f"Error al asignar el proceso: {error}")


def liberar_proceso(gestor: GestorMemoria) -> None:
    """Solicita el id de un proceso y libera su memoria si existe."""
    id_proceso = input("Id del proceso a liberar: ").strip()

    try:
        gestor.liberar_proceso(id_proceso)
        print(f"Proceso {id_proceso} liberado correctamente.")
    except (ValueError, RuntimeError) as error:
        print(f"Error al liberar el proceso: {error}")


def main() -> None:
    """Bucle principal del programa: muestra el menú hasta que el usuario salga."""
    print("Bienvenido al Simulador de Asignación de Memoria.")
    gestor: Optional[GestorMemoria] = None
    estrategia = FirstFit  # estrategia por defecto al iniciar

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            gestor = configurar_memoria()

        elif opcion == "2":
            nueva_estrategia = seleccionar_estrategia()
            if nueva_estrategia is not None:
                estrategia = nueva_estrategia

        elif opcion == "3":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                cargar_procesos_desde_archivo(gestor, estrategia)

        elif opcion == "4":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                crear_proceso_manual(gestor, estrategia)

        elif opcion == "5":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                liberar_proceso(gestor)

        elif opcion == "6":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                gestor.mostrar_estado()

        elif opcion == "7":
            print("Saliendo del simulador. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()