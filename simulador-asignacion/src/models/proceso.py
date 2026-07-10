"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: proceso.py

Descripción:
Define la clase Proceso, que representa un proceso que solicita
un bloque de memoria dentro del simulador de asignación (First Fit,
Best Fit, Worst Fit).
==============================================================
"""

from __future__ import annotations
from typing import Optional


class Proceso:
    """
    Representa un proceso que solicita un bloque de memoria.

    Atributos:
        id (str): identificador único del proceso (ej: "P1").
        tamano (int): tamaño de memoria solicitado, en KB.
        bloque_asignado (BloqueMemoria | None): bloque de memoria que
            tiene asignado. None si aún no se le ha asignado memoria
            o si fue rechazado por falta de espacio disponible.
    """

    def __init__(self, id_proceso: str, tamano: int):
        if tamano <= 0:
            raise ValueError("El tamaño solicitado por el proceso debe ser mayor a 0")
        if not id_proceso:
            raise ValueError("El proceso debe tener un identificador válido")

        self.id: str = id_proceso
        self.tamano: int = tamano
        self.bloque_asignado: Optional["BloqueMemoria"] = None  # noqa: F821

    def tiene_memoria_asignada(self) -> bool:
        """Retorna True si el proceso tiene un bloque de memoria asignado."""
        return self.bloque_asignado is not None

    def liberar_memoria(self) -> None:
        """
        Libera la memoria asignada a este proceso, si la tiene.
        Delega la liberación real al bloque de memoria para mantener
        la lógica de estado centralizada en BloqueMemoria.
        """
        if self.bloque_asignado is not None:
            self.bloque_asignado.liberar()

    def __repr__(self) -> str:
        estado = (
            f"asignado en dirección {self.bloque_asignado.direccion_inicio}"
            if self.tiene_memoria_asignada()
            else "sin memoria asignada"
        )
        return f"Proceso(id={self.id}, tamano={self.tamano}KB, {estado})"