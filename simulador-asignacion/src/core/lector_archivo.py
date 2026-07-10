"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: lector_archivo.py

Descripción:
Define la clase LectorArchivo, encargada de leer un archivo de
texto plano con la lista de procesos a simular y convertir cada
línea en un objeto Proceso. Formato esperado por línea:

    id_proceso,tamano_en_KB

Ejemplo de archivo válido:
    P1,50
    P2,30
    P3,100
==============================================================
"""

from __future__ import annotations
from typing import List
import os

from models.proceso import Proceso


class LectorArchivo:
    """
    Lee un archivo de texto plano con procesos y los convierte en
    una lista de objetos Proceso. Cada línea del archivo debe tener
    el formato: id_proceso,tamano_en_KB
    """

    @staticmethod
    def leer_procesos(ruta_archivo: str) -> List[Proceso]:
        """
        Lee el archivo indicado y retorna una lista de objetos
        Proceso construidos a partir de cada línea válida.

        Lanza FileNotFoundError si el archivo no existe, y ValueError
        si alguna línea no cumple el formato esperado.
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(
                f"No se encontró el archivo de entrada: {ruta_archivo}"
            )

        procesos: List[Proceso] = []

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
    def _parsear_linea(linea: str, numero_linea: int) -> Proceso:
        """
        Convierte una línea individual del archivo en un objeto
        Proceso. Lanza ValueError con un mensaje claro indicando el
        número de línea si el formato es inválido.
        """
        partes = linea.split(",")

        if len(partes) != 2:
            raise ValueError(
                f"Línea {numero_linea} inválida: '{linea}'. "
                f"Formato esperado: id_proceso,tamano_en_KB"
            )

        id_proceso, tamano_texto = partes[0].strip(), partes[1].strip()

        try:
            tamano = int(tamano_texto)
        except ValueError:
            raise ValueError(
                f"Línea {numero_linea} inválida: el tamaño '{tamano_texto}' "
                f"no es un número entero"
            )

        # La validación de tamano > 0 y id no vacío ya la hace el
        # propio constructor de Proceso, así que confiamos en él en
        # vez de duplicar la lógica aquí.
        return Proceso(id_proceso=id_proceso, tamano=tamano)

    def __repr__(self) -> str:
        return "LectorArchivo()"