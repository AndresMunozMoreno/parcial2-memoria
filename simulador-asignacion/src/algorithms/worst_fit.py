"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: worst_fit.py

Descripción:
Implementa la estrategia de asignación de memoria Worst Fit.
Recorre todos los bloques libres y selecciona el bloque más
grande disponible, dejando el mayor espacio sobrante posible
tras la asignación.
==============================================================
"""

from __future__ import annotations
from typing import List, Optional

from models.bloque_memoria import BloqueMemoria
from models.proceso import Proceso


class WorstFit:
    """
    Estrategia de asignación Worst Fit.

    Recorre todos los bloques libres disponibles y elige el de
    mayor tamaño, sin importar qué tan ajustado quede respecto al
    proceso. La idea es dejar el mayor sobrante posible como un
    bloque libre grande y potencialmente reutilizable, en vez de
    fragmentos pequeños difíciles de aprovechar (como sí ocurre
    con Best Fit).
    """

    @staticmethod
    def elegir_bloque(
        bloques_libres: List[BloqueMemoria], proceso: Proceso
    ) -> Optional[BloqueMemoria]:
        """
        Recorre todos los bloques libres y retorna el de mayor
        tamaño entre los que alcanzan para el proceso. Retorna None
        si ningún bloque es suficientemente grande.
        """
        peor_bloque: Optional[BloqueMemoria] = None

        for bloque in bloques_libres:
            if bloque.tamano < proceso.tamano:
                continue  # este bloque no alcanza, se descarta

            if peor_bloque is None or bloque.tamano > peor_bloque.tamano:
                peor_bloque = bloque

        return peor_bloque

    def __repr__(self) -> str:
        return "WorstFit()"