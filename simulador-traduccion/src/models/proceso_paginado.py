"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: proceso_paginado.py

Descripción:
Define la clase ProcesoPaginado, que representa un proceso dentro
del esquema de paginación de un nivel. A diferencia del Proceso
del simulador de asignación contigua, este proceso se divide en
un conjunto de páginas de tamaño fijo, calculadas a partir del
tamaño solicitado y el tamaño de página configurado.
==============================================================
"""

from __future__ import annotations
from typing import List
import math

from models.pagina import Pagina


class ProcesoPaginado:
    """
    Representa un proceso en el esquema de paginación de un nivel.

    Atributos:
        id (str): identificador único del proceso (ej: "P1").
        tamano (int): tamaño de memoria solicitado, en KB.
        tamano_pagina (int): tamaño de cada página, en KB.
        paginas (List[Pagina]): páginas en las que se divide el proceso.
    """

    def __init__(self, id_proceso: str, tamano: int, tamano_pagina: int):
        if not id_proceso:
            raise ValueError("El proceso debe tener un identificador válido")
        if tamano <= 0:
            raise ValueError("El tamaño solicitado por el proceso debe ser mayor a 0")
        if tamano_pagina <= 0:
            raise ValueError("El tamaño de página debe ser mayor a 0")

        self.id: str = id_proceso
        self.tamano: int = tamano
        self.tamano_pagina: int = tamano_pagina
        self.paginas: List[Pagina] = self._crear_paginas()

    def _crear_paginas(self) -> List[Pagina]:
        """
        Calcula cuántas páginas necesita el proceso, redondeando
        siempre hacia arriba: si el tamaño no es múltiplo exacto del
        tamaño de página, la última página igual se reserva completa
        (esto es lo que origina la fragmentación interna en paginación).
        """
        numero_de_paginas = math.ceil(self.tamano / self.tamano_pagina)
        return [
            Pagina(numero_pagina=i, id_proceso=self.id)
            for i in range(numero_de_paginas)
        ]

    def cantidad_paginas(self) -> int:
        """Retorna cuántas páginas necesita este proceso."""
        return len(self.paginas)

    def memoria_reservada(self) -> int:
        """
        Retorna el total de memoria realmente reservada para el
        proceso (cantidad de páginas * tamaño de página), que puede
        ser mayor al tamaño solicitado originalmente.
        """
        return self.cantidad_paginas() * self.tamano_pagina

    def fragmentacion_interna(self) -> int:
        """
        Calcula la fragmentación interna del proceso: la diferencia
        entre la memoria reservada (en páginas completas) y la
        memoria realmente solicitada.
        """
        return self.memoria_reservada() - self.tamano

    def todas_las_paginas_cargadas(self) -> bool:
        """Retorna True si todas las páginas del proceso tienen un marco asignado."""
        return all(pagina.esta_cargada() for pagina in self.paginas)

    def __repr__(self) -> str:
        return (
            f"ProcesoPaginado(id={self.id}, tamano={self.tamano}KB, "
            f"paginas={self.cantidad_paginas()}, "
            f"fragmentacion_interna={self.fragmentacion_interna()}KB)"
        )