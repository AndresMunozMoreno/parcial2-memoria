"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: lector_archivo.py

Descripción:
Define la clase LectorArchivo, encargada de leer un archivo de
texto plano con la lista de procesos a simular. A diferencia del
lector usado en el Simulador 1 (que retorna objetos Proceso), este
lector retorna tuplas simples (id_proceso, tamano), para no
depender de ninguna clase de dominio y mantener a ambos
simuladores completamente desacoplados entre sí. Formato esperado
por línea:

    id_proceso,tamano_en_KB

Ejemplo de archivo válido:
    P1,45
    P2,10
    P3,60
==============================================================
"""

from __future__ import annotations
from typing import List, Tuple
import os


class LectorArchivo:
    """
    Lee un archivo de texto plano con procesos y los convierte en
    una lista de tuplas (id_proceso, tamano). Cada línea del archivo
    debe tener el formato: id_proceso,tamano_en_KB
    """

    @staticmethod
    def leer_procesos(ruta_archivo: str) -> List[Tuple[str, int]]:
        """
        Lee el archivo indicado y retorna una lista de tuplas
        (id_proceso, tamano) construidas a partir de cada línea válida.

        Lanza FileNotFoundError si el archivo no existe, y ValueError
        si alguna línea no cumple el formato esperado.
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(
                f"No se encontró el archivo de entrada: {ruta_archivo}"
            )

        procesos: List[Tuple[str, int]] = []

        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea = linea.strip()

                # Ignoramos líneas vacías y comentarios (líneas que
                # empiezan con #), útiles para documentar el archivo
                # de entrada sin romper el formato.
                if not linea or linea.startswith("#"):
                    continue

                proceso = LectorArchivo._parsear_linea(linea, numero_linea)
                procesos.append(proceso)

        if not procesos:
            raise ValueError(
                f"El archivo {ruta_archivo} no contiene procesos válidos"
            )

        return procesos

    @staticmethod
    def _parsear_linea(linea: str, numero_linea: int) -> Tuple[str, int]:
        """
        Convierte una línea individual del archivo en una tupla
        (id_proceso, tamano). Lanza ValueError con un mensaje claro
        indicando el número de línea si el formato es inválido.
        """
        partes = linea.split(",")

        if len(partes) != 2:
            raise ValueError(
                f"Línea {numero_linea} inválida: '{linea}'. "
                f"Formato esperado: id_proceso,tamano_en_KB"
            )

        id_proceso, tamano_texto = partes[0].strip(), partes[1].strip()

        if not id_proceso:
            raise ValueError(
                f"Línea {numero_linea} inválida: el id de proceso está vacío"
            )

        try:
            tamano = int(tamano_texto)
        except ValueError:
            raise ValueError(
                f"Línea {numero_linea} inválida: el tamaño '{tamano_texto}' "
                f"no es un número entero"
            )

        if tamano <= 0:
            raise ValueError(
                f"Línea {numero_linea} inválida: el tamaño debe ser mayor a 0 "
                f"(se recibió {tamano})"
            )

        return (id_proceso, tamano)

    def __repr__(self) -> str:
        return "LectorArchivo()"