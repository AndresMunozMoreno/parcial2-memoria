"""
Módulo que define la clase BloqueMemoria.

Representa un bloque contiguo de memoria dentro del simulador de
asignación (First Fit, Best Fit, Worst Fit). La memoria total del
sistema se modela como una lista de objetos BloqueMemoria.
"""

from __future__ import annotations
from typing import Optional


class BloqueMemoria:
    """
    Representa un bloque de memoria física, ya sea libre u ocupado.

    Atributos:
        direccion_inicio (int): posición inicial del bloque en la memoria total.
        tamano (int): tamaño del bloque en KB.
        libre (bool): indica si el bloque está disponible para asignación.
        proceso_asignado (Proceso | None): proceso que ocupa el bloque, si aplica.
    """

    def __init__(self, direccion_inicio: int, tamano: int):
        if tamano <= 0:
            raise ValueError("El tamaño del bloque debe ser mayor a 0")
        if direccion_inicio < 0:
            raise ValueError("La dirección de inicio no puede ser negativa")

        self.direccion_inicio: int = direccion_inicio
        self.tamano: int = tamano
        self.libre: bool = True
        self.proceso_asignado: Optional["Proceso"] = None  # noqa: F821 (forward ref)

    def esta_libre(self) -> bool:
        """Retorna True si el bloque no tiene un proceso asignado."""
        return self.libre

    def asignar(self, proceso: "Proceso") -> None:
        """
        Asigna un proceso a este bloque de memoria.

        Lanza un error si el bloque ya está ocupado o si el proceso
        no cabe en el tamaño disponible del bloque.
        """
        if not self.libre:
            raise RuntimeError(
                f"El bloque en dirección {self.direccion_inicio} ya está ocupado"
            )
        if proceso.tamano > self.tamano:
            raise ValueError(
                f"El proceso {proceso.id} (tamaño {proceso.tamano}KB) "
                f"no cabe en el bloque (tamaño {self.tamano}KB)"
            )

        self.libre = False
        self.proceso_asignado = proceso
        proceso.bloque_asignado = self

    def liberar(self) -> None:
        """Libera el bloque, desvinculando el proceso que lo ocupaba."""
        if self.proceso_asignado is not None:
            self.proceso_asignado.bloque_asignado = None
        self.proceso_asignado = None
        self.libre = True

    def fragmentacion_interna(self) -> int:
        """
        Calcula la fragmentación interna del bloque: el espacio que
        sobra dentro del bloque una vez asignado un proceso que no
        lo llena por completo. Si el bloque está libre, retorna 0.
        """
        if self.libre or self.proceso_asignado is None:
            return 0
        return self.tamano - self.proceso_asignado.tamano

    def __repr__(self) -> str:
        estado = "LIBRE" if self.libre else f"OCUPADO por {self.proceso_asignado.id}"
        return (
            f"BloqueMemoria(inicio={self.direccion_inicio}, "
            f"tamano={self.tamano}KB, estado={estado})"
        )