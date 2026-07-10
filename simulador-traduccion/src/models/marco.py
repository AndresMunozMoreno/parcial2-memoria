"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: marco.py

Descripción:
Define la clase Marco, que representa un marco de memoria física
dentro del esquema de paginación de un nivel. La memoria física
total se modela como una lista de objetos Marco, cada uno del
mismo tamaño fijo (tamaño de página).
==============================================================
"""

from __future__ import annotations
from typing import Optional


class Marco:
    """
    Representa un marco de memoria física.

    Atributos:
        numero_marco (int): identificador del marco (0, 1, 2...).
        tamano (int): tamaño del marco en KB (igual al tamaño de página).
        ocupado (bool): indica si el marco tiene una página cargada.
        pagina_asignada (Pagina | None): página actualmente cargada, si aplica.
    """

    def __init__(self, numero_marco: int, tamano: int):
        if numero_marco < 0:
            raise ValueError("El número de marco no puede ser negativo")
        if tamano <= 0:
            raise ValueError("El tamaño del marco debe ser mayor a 0")

        self.numero_marco: int = numero_marco
        self.tamano: int = tamano
        self.ocupado: bool = False
        self.pagina_asignada: Optional["Pagina"] = None  # noqa: F821

    def esta_libre(self) -> bool:
        """Retorna True si el marco no tiene ninguna página cargada."""
        return not self.ocupado

    def asignar(self, pagina: "Pagina") -> None:
        """Carga una página en este marco."""
        if self.ocupado:
            raise RuntimeError(f"El marco {self.numero_marco} ya está ocupado")

        self.ocupado = True
        self.pagina_asignada = pagina
        pagina.marco_asignado = self

    def liberar(self) -> None:
        """Libera el marco, desvinculando la página que tenía cargada."""
        if self.pagina_asignada is not None:
            self.pagina_asignada.marco_asignado = None
        self.pagina_asignada = None
        self.ocupado = False

    def __repr__(self) -> str:
        if self.ocupado and self.pagina_asignada is not None:
            estado = (
                f"OCUPADO por proceso {self.pagina_asignada.id_proceso} "
                f"(pagina {self.pagina_asignada.numero_pagina})"
            )
        else:
            estado = "LIBRE"
        return f"Marco(numero={self.numero_marco}, tamano={self.tamano}KB, estado={estado})"