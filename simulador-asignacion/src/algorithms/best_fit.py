"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: best_fit.py

Descripción:
Implementa la estrategia de asignación de memoria Best Fit.
Recorre todos los bloques libres y selecciona el bloque más
pequeño que aún sea suficiente para el proceso, minimizando
el espacio sobrante inmediato.
==============================================================
"""

from __future__ import annotations
from typing import List, Optional

from models.bloque_memoria import BloqueMemoria
from models.proceso import Proceso


class BestFit:
    """
    Estrategia de asignación Best Fit.

    Recorre todos los bloques libres disponibles y elige el que
    tenga el tamaño más ajustado (el más pequeño posible que aún
    alcance para el proceso). Busca minimizar el espacio sobrante
    en cada asignación individual, aunque con el tiempo tiende a
    generar muchos bloques libres muy pequeños y difíciles de
    reutilizar (fragmentación externa "fina").
    """

    @staticmethod
    def elegir_bloque(
        bloques_libres: List[BloqueMemoria], proceso: Proceso
    ) -> Optional[BloqueMemoria]:
        """
        Recorre todos los bloques libres y retorna el de menor
        tamaño entre los que alcanzan para el proceso. Retorna None
        si ningún bloque es suficientemente grande.
        """
        mejor_bloque: Optional[BloqueMemoria] = None

        for bloque in bloques_libres:
            if bloque.tamano < proceso.tamano:
                continue  # este bloque no alcanza, se descarta

            if mejor_bloque is None or bloque.tamano < mejor_bloque.tamano:
                mejor_bloque = bloque

        return mejor_bloque

    def __repr__(self) -> str:
        return "BestFit()"