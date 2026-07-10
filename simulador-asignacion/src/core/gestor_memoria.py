"""
==============================================================
Proyecto: Simulador de Administración de Memoria
Autor: Andrés Felipe Muñoz Moreno
Asignatura: Sistemas Operativos - Universidad del Valle
Archivo: gestor_memoria.py
Descripción: Gestiona el estado global de la memoria del
sistema y coordina la creación/liberación de procesos.
==============================================================
"""

from __future__ import annotations
from typing import List, Optional

from models.bloque_memoria import BloqueMemoria
from models.proceso import Proceso


class GestorMemoria:
    """
    Administra el estado global de la memoria del sistema.

    Atributos:
        tamano_total (int): tamaño total de la memoria simulada, en KB.
        bloques (List[BloqueMemoria]): lista de bloques que componen la memoria.
        procesos (List[Proceso]): procesos actualmente creados en el sistema.
    """

    def __init__(self, tamano_total: int):
        if tamano_total <= 0:
            raise ValueError("El tamaño total de memoria debe ser mayor a 0")

        self.tamano_total: int = tamano_total
        # Al iniciar, toda la memoria es un único bloque libre
        self.bloques: List[BloqueMemoria] = [
            BloqueMemoria(direccion_inicio=0, tamano=tamano_total)
        ]
        self.procesos: List[Proceso] = []

    def obtener_bloques_libres(self) -> List[BloqueMemoria]:
        """Retorna solo los bloques actualmente disponibles."""
        return [bloque for bloque in self.bloques if bloque.esta_libre()]

    def obtener_bloques_ocupados(self) -> List[BloqueMemoria]:
        """Retorna solo los bloques actualmente ocupados."""
        return [bloque for bloque in self.bloques if not bloque.esta_libre()]

    def buscar_proceso(self, id_proceso: str) -> Optional[Proceso]:
        """Busca un proceso registrado por su id. Retorna None si no existe."""
        for proceso in self.procesos:
            if proceso.id == id_proceso:
                return proceso
        return None

    def crear_proceso(self, proceso: Proceso, bloque_elegido: BloqueMemoria) -> None:
        """
        Registra un nuevo proceso en el sistema y lo asigna al bloque
        indicado. El bloque_elegido debe ser determinado previamente
        por un algoritmo (First/Best/Worst Fit); GestorMemoria no
        decide la estrategia, solo ejecuta la asignación.

        Si el bloque es más grande que lo que el proceso necesita,
        el bloque se divide en dos: uno ocupado (del tamaño exacto
        del proceso) y uno libre restante (con el espacio sobrante).
        """
        if self.buscar_proceso(proceso.id) is not None:
            raise ValueError(f"Ya existe un proceso registrado con id {proceso.id}")
        if bloque_elegido not in self.bloques:
            raise ValueError("El bloque indicado no pertenece a esta memoria")
        if not bloque_elegido.esta_libre():
            raise RuntimeError("El bloque elegido no está libre")
        if proceso.tamano > bloque_elegido.tamano:
            raise ValueError(
                f"El proceso {proceso.id} no cabe en el bloque seleccionado"
            )

        self._dividir_bloque_si_sobra_espacio(bloque_elegido, proceso)
        self.procesos.append(proceso)

    def _dividir_bloque_si_sobra_espacio(
        self, bloque: BloqueMemoria, proceso: Proceso
    ) -> None:
        """
        Divide un bloque libre en dos partes cuando el proceso no
        ocupa el bloque completo: una parte queda ocupada exactamente
        con el tamaño del proceso, y la otra queda libre con el
        espacio restante. Si el proceso ocupa el bloque exacto, no
        hay división y solo se asigna directamente.
        """
        espacio_sobrante = bloque.tamano - proceso.tamano

        if espacio_sobrante == 0:
            bloque.asignar(proceso)
            return

        # Reducimos el bloque original al tamaño exacto del proceso
        # y lo asignamos.
        indice = self.bloques.index(bloque)
        bloque.tamano = proceso.tamano
        bloque.asignar(proceso)

        # Creamos un nuevo bloque libre con el espacio restante,
        # ubicado justo después del bloque asignado.
        nuevo_bloque_libre = BloqueMemoria(
            direccion_inicio=bloque.direccion_inicio + proceso.tamano,
            tamano=espacio_sobrante,
        )
        self.bloques.insert(indice + 1, nuevo_bloque_libre)

    def liberar_proceso(self, id_proceso: str) -> None:
        """Libera la memoria asignada a un proceso, dado su id."""
        proceso = self.buscar_proceso(id_proceso)
        if proceso is None:
            raise ValueError(f"No existe un proceso con id {id_proceso}")
        if not proceso.tiene_memoria_asignada():
            raise RuntimeError(f"El proceso {id_proceso} no tiene memoria asignada")

        proceso.liberar_memoria()
        self.procesos.remove(proceso)

    def fragmentacion_externa_total(self) -> int:
        """
        Suma el tamaño de todos los bloques libres. Representa la
        memoria total disponible mostrada de forma fragmentada,
        aunque ningún bloque individual sea suficientemente grande
        para un proceso futuro.
        """
        return sum(bloque.tamano for bloque in self.obtener_bloques_libres())

    def fragmentacion_interna_total(self) -> int:
        """Suma la fragmentación interna de todos los bloques ocupados."""
        return sum(bloque.fragmentacion_interna() for bloque in self.bloques)

    def mostrar_estado(self) -> None:
        """Imprime en consola el estado actual de todos los bloques de memoria."""
        print(f"\n{'='*60}")
        print(f"Estado de la memoria (total: {self.tamano_total}KB)")
        print(f"{'='*60}")
        for bloque in self.bloques:
            print(f"  {bloque}")
        print(f"{'-'*60}")
        print(f"Fragmentación externa total: {self.fragmentacion_externa_total()}KB")
        print(f"Fragmentación interna total: {self.fragmentacion_interna_total()}KB")
        print(f"{'='*60}\n")

    def __repr__(self) -> str:
        return (
            f"GestorMemoria(total={self.tamano_total}KB, "
            f"bloques={len(self.bloques)}, procesos={len(self.procesos)})"
        )