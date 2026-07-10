"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: tabla_paginas.py

Descripción:
Define la clase TablaPaginas, que representa la tabla de páginas
de un proceso específico dentro del esquema de paginación de un
nivel. Mapea número de página -> número de marco físico, y ofrece
el método traducir() necesario para resolver una dirección virtual
a su marco correspondiente.
==============================================================
"""

from __future__ import annotations
from typing import Dict, Optional


class TablaPaginas:
    """
    Representa la tabla de páginas de un proceso.

    Atributos:
        id_proceso (str): identificador del proceso dueño de esta tabla.
        mapeo (Dict[int, int]): diccionario {numero_pagina: numero_marco}.
    """

    def __init__(self, id_proceso: str):
        if not id_proceso:
            raise ValueError("La tabla de páginas debe pertenecer a un proceso válido")

        self.id_proceso: str = id_proceso
        self.mapeo: Dict[int, int] = {}

    def mapear_pagina(self, numero_pagina: int, numero_marco: int) -> None:
        """
        Registra en la tabla que una página del proceso quedó cargada
        en un marco físico específico.
        """
        if numero_pagina < 0:
            raise ValueError("El número de página no puede ser negativo")
        if numero_marco < 0:
            raise ValueError("El número de marco no puede ser negativo")
        if numero_pagina in self.mapeo:
            raise RuntimeError(
                f"La página {numero_pagina} del proceso {self.id_proceso} "
                f"ya tiene un marco asignado (marco {self.mapeo[numero_pagina]})"
            )

        self.mapeo[numero_pagina] = numero_marco

    def traducir(self, numero_pagina: int) -> int:
        """
        Retorna el número de marco físico asociado a una página.
        Lanza un error claro si la página no está mapeada, para
        facilitar el diagnóstico durante las pruebas.
        """
        if numero_pagina not in self.mapeo:
            raise KeyError(
                f"La página {numero_pagina} del proceso {self.id_proceso} "
                f"no está mapeada en la tabla de páginas"
            )
        return self.mapeo[numero_pagina]

    def eliminar_mapeo(self, numero_pagina: int) -> None:
        """
        Elimina el mapeo de una página específica. Se usa típicamente
        al liberar el proceso completo, página por página.
        """
        if numero_pagina not in self.mapeo:
            raise KeyError(
                f"No se puede eliminar: la página {numero_pagina} del proceso "
                f"{self.id_proceso} no está mapeada"
            )
        del self.mapeo[numero_pagina]

    def esta_mapeada(self, numero_pagina: int) -> bool:
        """Retorna True si la página indicada ya tiene marco asignado."""
        return numero_pagina in self.mapeo

    def obtener_marco(self, numero_pagina: int) -> Optional[int]:
        """
        Retorna el número de marco de una página, o None si no está
        mapeada (a diferencia de traducir(), no lanza excepción).
        Útil para consultas desde el menú donde no se quiere interrumpir
        el flujo con una excepción.
        """
        return self.mapeo.get(numero_pagina)

    def __repr__(self) -> str:
        if not self.mapeo:
            return f"TablaPaginas(proceso={self.id_proceso}, vacia)"

        entradas = ", ".join(
            f"pag{pagina}->marco{marco}"
            for pagina, marco in sorted(self.mapeo.items())
        )
        return f"TablaPaginas(proceso={self.id_proceso}, [{entradas}])"