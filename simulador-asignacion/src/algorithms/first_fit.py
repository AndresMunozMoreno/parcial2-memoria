"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: first_fit.py

Descripción:
Implementa la estrategia de asignación de memoria First Fit.
Recorre la lista de bloques libres en orden y selecciona el
primer bloque cuyo tamaño sea suficiente para el proceso.
==============================================================
"""

from __future__ import annotations
from typing import List, Optional

from models.bloque_memoria import BloqueMemoria
from models.proceso import Proceso


class FirstFit:
    """
    Estrategia de asignación First Fit.

    Elige el primer bloque libre, en orden de aparición en la lista,
    cuyo tamaño sea mayor o igual al tamaño solicitado por el proceso.
    Es la estrategia más simple y rápida de las tres, aunque tiende
    a generar más fragmentación externa al frente de la memoria con
    el paso del tiempo.
    """

    @staticmethod
    def elegir_bloque(
        bloques_libres: List[BloqueMemoria], proceso: Proceso
    ) -> Optional[BloqueMemoria]:
        """
        Recorre los bloques libres en orden y retorna el primero que
        pueda alojar al proceso. Retorna None si ningún bloque es
        suficientemente grande (no hay memoria disponible para el
        proceso en este momento).
        """
        for bloque in bloques_libres:
            if bloque.tamano >= proceso.tamano:
                return bloque
        return None

    def __repr__(self) -> str:
        return "FirstFit()"