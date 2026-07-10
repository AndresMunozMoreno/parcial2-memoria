"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: pagina.py

Descripción:
Define la clase Pagina, que representa una página de memoria
virtual perteneciente a un proceso, dentro del esquema de
paginación de un nivel.
==============================================================
"""

from __future__ import annotations
from typing import Optional


class Pagina:
    """
    Representa una página de memoria virtual de un proceso.

    Atributos:
        numero_pagina (int): posición de la página dentro del proceso (0, 1, 2...).
        id_proceso (str): identificador del proceso dueño de esta página.
        marco_asignado (Marco | None): marco físico donde está cargada, si aplica.
    """

    def __init__(self, numero_pagina: int, id_proceso: str):
        if numero_pagina < 0:
            raise ValueError("El número de página no puede ser negativo")
        if not id_proceso:
            raise ValueError("La página debe pertenecer a un proceso válido")

        self.numero_pagina: int = numero_pagina
        self.id_proceso: str = id_proceso
        self.marco_asignado: Optional["Marco"] = None  # noqa: F821

    def esta_cargada(self) -> bool:
        """Retorna True si la página tiene un marco físico asignado."""
        return self.marco_asignado is not None

    def __repr__(self) -> str:
        estado = (
            f"marco {self.marco_asignado.numero_marco}"
            if self.esta_cargada()
            else "sin marco asignado"
        )
        return (
            f"Pagina(numero={self.numero_pagina}, "
            f"proceso={self.id_proceso}, {estado})"
        )