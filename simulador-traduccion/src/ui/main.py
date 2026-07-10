"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: main.py

Descripción:
Punto de entrada del Simulador de Traducción de Direcciones
Virtuales a Físicas (paginación de un nivel). Presenta un menú
interactivo por consola que permite configurar la memoria física
y el tamaño de página, cargar procesos desde un archivo de
entrada, crear/liberar procesos manualmente, traducir direcciones
virtuales y visualizar el estado de los marcos y de las tablas
de páginas.
==============================================================
"""

from __future__ import annotations
from typing import Optional

from core.gestor_memoria_virtual import GestorMemoriaVirtual
from core.lector_archivo import LectorArchivo


# Valores por defecto (en KB), usados si el usuario no configura otros
# al iniciar el programa.
TAMANO_MEMORIA_FISICA_POR_DEFECTO = 64
TAMANO_PAGINA_POR_DEFECTO = 16


def mostrar_menu_principal() -> None:
    print("\n" + "=" * 55)
    print("  SIMULADOR DE TRADUCCIÓN DE DIRECCIONES (PAGINACIÓN)")
    print("=" * 55)
    print("1. Configurar memoria física y tamaño de página")
    print("2. Cargar procesos desde archivo")
    print("3. Crear proceso manualmente")
    print("4. Liberar proceso")
    print("5. Traducir una dirección virtual")
    print("6. Ver estado de los marcos")
    print("7. Ver tabla de páginas de un proceso")
    print("8. Salir")
    print("=" * 55)


def configurar_memoria() -> GestorMemoriaVirtual:
    """Solicita al usuario el tamaño de memoria física y el tamaño de página."""
    entrada_memoria = input(
        f"Tamaño de memoria física en KB "
        f"(Enter para usar {TAMANO_MEMORIA_FISICA_POR_DEFECTO}KB por defecto): "
    ).strip()
    entrada_pagina = input(
        f"Tamaño de página en KB "
        f"(Enter para usar {TAMANO_PAGINA_POR_DEFECTO}KB por defecto): "
    ).strip()

    tamano_memoria = (
        TAMANO_MEMORIA_FISICA_POR_DEFECTO if entrada_memoria == "" else int(entrada_memoria)
    )
    tamano_pagina = (
        TAMANO_PAGINA_POR_DEFECTO if entrada_pagina == "" else int(entrada_pagina)
    )

    gestor = GestorMemoriaVirtual(
        tamano_memoria_fisica=tamano_memoria, tamano_pagina=tamano_pagina
    )
    print(
        f"Memoria física configurada: {tamano_memoria}KB, "
        f"tamaño de página: {tamano_pagina}KB "
        f"({len(gestor.marcos)} marcos en total)."
    )
    return gestor


def cargar_procesos_desde_archivo(gestor: GestorMemoriaVirtual) -> None:
    """Lee procesos desde un archivo de texto y los crea en orden."""
    ruta = input("Ruta del archivo de entrada: ").strip()

    try:
        procesos = LectorArchivo.leer_procesos(ruta)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error al leer el archivo: {error}")
        return

    for id_proceso, tamano in procesos:
        crear_proceso(gestor, id_proceso, tamano)


def crear_proceso_manual(gestor: GestorMemoriaVirtual) -> None:
    """Solicita al usuario los datos de un proceso nuevo y lo crea."""
    id_proceso = input("Id del proceso (ej: P1): ").strip()
    tamano_texto = input("Tamaño solicitado en KB: ").strip()

    try:
        tamano = int(tamano_texto)
    except ValueError:
        print(f"Tamaño inválido: '{tamano_texto}' no es un número entero.")
        return

    crear_proceso(gestor, id_proceso, tamano)


def crear_proceso(gestor: GestorMemoriaVirtual, id_proceso: str, tamano: int) -> None:
    """
    Crea el proceso paginado en el gestor. Informa al usuario si no hay
    marcos suficientes o si el id ya existe, sin detener el programa.
    """
    try:
        proceso = gestor.crear_proceso(id_proceso, tamano)
        print(
            f"Proceso {proceso.id} creado: {proceso.cantidad_paginas()} página(s), "
            f"fragmentación interna de {proceso.fragmentacion_interna()}KB."
        )
    except (ValueError, RuntimeError) as error:
        print(f"Error al crear el proceso: {error}")


def liberar_proceso(gestor: GestorMemoriaVirtual) -> None:
    """Solicita el id de un proceso y libera sus marcos si existe."""
    id_proceso = input("Id del proceso a liberar: ").strip()

    try:
        gestor.liberar_proceso(id_proceso)
        print(f"Proceso {id_proceso} liberado correctamente.")
    except RuntimeError as error:
        print(f"Error al liberar el proceso: {error}")


def traducir_direccion(gestor: GestorMemoriaVirtual) -> None:
    """
    Solicita id de proceso y dirección virtual, y muestra el detalle
    completo de la traducción: página, desplazamiento, marco y
    dirección física resultante.
    """
    id_proceso = input("Id del proceso: ").strip()
    direccion_texto = input("Dirección virtual a traducir: ").strip()

    try:
        direccion_virtual = int(direccion_texto)
    except ValueError:
        print(f"Dirección inválida: '{direccion_texto}' no es un número entero.")
        return

    try:
        direccion_fisica = gestor.traducir_direccion(id_proceso, direccion_virtual)
        numero_pagina = direccion_virtual // gestor.tamano_pagina
        desplazamiento = direccion_virtual % gestor.tamano_pagina
        print(
            f"Dirección virtual {direccion_virtual} -> "
            f"página {numero_pagina}, desplazamiento {desplazamiento} -> "
            f"dirección física {direccion_fisica}"
        )
    except (ValueError, RuntimeError, KeyError) as error:
        print(f"Error al traducir la dirección: {error}")


def mostrar_estado_marcos(gestor: GestorMemoriaVirtual) -> None:
    """Muestra el estado de todos los marcos físicos."""
    print(f"\nEstado de los marcos ({gestor.marcos_libres_disponibles()} libres de {len(gestor.marcos)}):")
    for marco in gestor.marcos:
        print(f"  {marco}")


def mostrar_tabla_paginas(gestor: GestorMemoriaVirtual) -> None:
    """Muestra la tabla de páginas de un proceso específico."""
    id_proceso = input("Id del proceso: ").strip()

    if id_proceso not in gestor.tablas_paginas:
        print(f"No existe un proceso activo con id '{id_proceso}'.")
        return

    print(gestor.tablas_paginas[id_proceso])


def main() -> None:
    """Bucle principal del programa: muestra el menú hasta que el usuario salga."""
    print("Bienvenido al Simulador de Traducción de Direcciones (Paginación).")
    gestor: Optional[GestorMemoriaVirtual] = None

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            gestor = configurar_memoria()

        elif opcion == "2":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                cargar_procesos_desde_archivo(gestor)

        elif opcion == "3":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                crear_proceso_manual(gestor)

        elif opcion == "4":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                liberar_proceso(gestor)

        elif opcion == "5":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                traducir_direccion(gestor)

        elif opcion == "6":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                mostrar_estado_marcos(gestor)

        elif opcion == "7":
            if gestor is None:
                print("Primero debe configurar la memoria (opción 1).")
            else:
                mostrar_tabla_paginas(gestor)

        elif opcion == "8":
            print("Saliendo del simulador. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()