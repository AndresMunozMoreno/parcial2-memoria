"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: gestor_memoria_virtual.py

Descripción:
Define la clase GestorMemoriaVirtual, componente central del
Simulador 2. Administra la memoria física como una lista de
marcos, crea y libera procesos paginados asignando marcos libres
a sus páginas, y traduce direcciones virtuales a direcciones
físicas usando la tabla de páginas de cada proceso.
==============================================================
"""

from __future__ import annotations
from typing import Dict, List

from models.marco import Marco
from models.pagina import Pagina
from models.proceso_paginado import ProcesoPaginado
from core.tabla_paginas import TablaPaginas


class GestorMemoriaVirtual:
    """
    Administra la memoria física (marcos) y la relación entre
    procesos paginados y sus tablas de páginas.

    Atributos:
        tamano_memoria_fisica (int): tamaño total de la memoria física, en KB.
        tamano_pagina (int): tamaño de cada página/marco, en KB.
        marcos (List[Marco]): lista completa de marcos físicos.
        procesos (Dict[str, ProcesoPaginado]): procesos activos por id.
        tablas_paginas (Dict[str, TablaPaginas]): tabla de páginas por id de proceso.
    """

    def __init__(self, tamano_memoria_fisica: int, tamano_pagina: int):
        if tamano_memoria_fisica <= 0:
            raise ValueError("El tamaño de la memoria física debe ser mayor a 0")
        if tamano_pagina <= 0:
            raise ValueError("El tamaño de página debe ser mayor a 0")
        if tamano_pagina > tamano_memoria_fisica:
            raise ValueError(
                "El tamaño de página no puede ser mayor que la memoria física total"
            )

        self.tamano_memoria_fisica: int = tamano_memoria_fisica
        self.tamano_pagina: int = tamano_pagina

        numero_de_marcos = tamano_memoria_fisica // tamano_pagina
        self.marcos: List[Marco] = [
            Marco(numero_marco=i, tamano=tamano_pagina)
            for i in range(numero_de_marcos)
        ]

        self.procesos: Dict[str, ProcesoPaginado] = {}
        self.tablas_paginas: Dict[str, TablaPaginas] = {}

    def _marcos_libres(self) -> List[Marco]:
        """Retorna la lista de marcos actualmente libres."""
        return [marco for marco in self.marcos if marco.esta_libre()]

    def crear_proceso(self, id_proceso: str, tamano: int) -> ProcesoPaginado:
        """
        Crea un ProcesoPaginado, le asigna marcos libres a cada una de
        sus páginas y construye su tabla de páginas correspondiente.

        Lanza RuntimeError si no hay marcos libres suficientes, o si
        ya existe un proceso con el mismo id_proceso.
        """
        if id_proceso in self.procesos:
            raise RuntimeError(f"Ya existe un proceso activo con id '{id_proceso}'")

        proceso = ProcesoPaginado(
            id_proceso=id_proceso, tamano=tamano, tamano_pagina=self.tamano_pagina
        )

        libres = self._marcos_libres()
        if len(libres) < proceso.cantidad_paginas():
            raise RuntimeError(
                f"No hay marcos suficientes para el proceso '{id_proceso}': "
                f"se necesitan {proceso.cantidad_paginas()} marcos, "
                f"hay {len(libres)} libres"
            )

        tabla = TablaPaginas(id_proceso=id_proceso)

        for pagina in proceso.paginas:
            marco = libres.pop(0)
            marco.asignar(pagina)
            tabla.mapear_pagina(pagina.numero_pagina, marco.numero_marco)

        self.procesos[id_proceso] = proceso
        self.tablas_paginas[id_proceso] = tabla
        return proceso

    def liberar_proceso(self, id_proceso: str) -> None:
        """
        Libera todos los marcos ocupados por un proceso y elimina su
        registro (proceso y tabla de páginas) del gestor.
        """
        if id_proceso not in self.procesos:
            raise RuntimeError(f"No existe un proceso activo con id '{id_proceso}'")

        proceso = self.procesos[id_proceso]
        for pagina in proceso.paginas:
            if pagina.marco_asignado is not None:
                pagina.marco_asignado.liberar()

        del self.procesos[id_proceso]
        del self.tablas_paginas[id_proceso]

    def traducir_direccion(self, id_proceso: str, direccion_virtual: int) -> int:
        """
        Traduce una dirección virtual de un proceso a su dirección
        física correspondiente.

        Calcula:
            numero_pagina    = direccion_virtual // tamano_pagina
            desplazamiento   = direccion_virtual % tamano_pagina
            numero_marco     = tabla_paginas.traducir(numero_pagina)
            direccion_fisica = (numero_marco * tamano_pagina) + desplazamiento

        Lanza RuntimeError si el proceso no existe, o ValueError si la
        dirección virtual está fuera del espacio de memoria reservado
        para ese proceso.
        """
        if id_proceso not in self.procesos:
            raise RuntimeError(f"No existe un proceso activo con id '{id_proceso}'")

        proceso = self.procesos[id_proceso]

        if direccion_virtual < 0 or direccion_virtual >= proceso.memoria_reservada():
            raise ValueError(
                f"La dirección virtual {direccion_virtual} está fuera del espacio "
                f"del proceso '{id_proceso}' (memoria reservada: "
                f"{proceso.memoria_reservada()}KB)"
            )

        numero_pagina = direccion_virtual // self.tamano_pagina
        desplazamiento = direccion_virtual % self.tamano_pagina

        tabla = self.tablas_paginas[id_proceso]
        numero_marco = tabla.traducir(numero_pagina)

        direccion_fisica = (numero_marco * self.tamano_pagina) + desplazamiento
        return direccion_fisica

    def marcos_libres_disponibles(self) -> int:
        """Retorna la cantidad de marcos libres actualmente."""
        return len(self._marcos_libres())

    def __repr__(self) -> str:
        return (
            f"GestorMemoriaVirtual(memoria_fisica={self.tamano_memoria_fisica}KB, "
            f"tamano_pagina={self.tamano_pagina}KB, "
            f"marcos_totales={len(self.marcos)}, "
            f"marcos_libres={self.marcos_libres_disponibles()}, "
            f"procesos_activos={list(self.procesos.keys())})"
        )