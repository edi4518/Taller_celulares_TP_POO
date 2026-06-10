"""Modulo que contiene la clase Tecnico."""
from models.persona import Persona


class Tecnico (Persona):
    """Clase que representa a un tecnico."""
    def __init__(self, id_tecnico, nombre, apellido, documento, telefono, turno):
        """Constructor de la clase tecnico que recibe
        los datos excenciales para crearlo,
        ademas de una lista vacia para almacenar
        las reparaciones asignadas al tecnico"""

        super().__init__(nombre, apellido, documento, telefono)
        self.id_tecnico = id_tecnico
        self.turno = turno

        # Lista para almacenar las reparaciones asignadas al técnico
        self._reparaciones_asignadas = []

    @property
    def turno(self):
        """Metodo para obtener el turno del tecnico"""
        return self._turno

    @turno.setter
    def turno(self, valor):
        """Metodo para establecer el turno del tecnico, validando que sea un turno valido"""
        turnos_validos = ['MAÑANA', 'TARDE', 'NOCHE']
        if valor.upper() in turnos_validos:
            self._turno = valor.upper()
        else:
            raise ValueError(
                f"Turno inválido. Los turnos válidos son: {', '.join(turnos_validos)}.")

    def agregar_reparacion(self, reparacion):
        """Metodo para agregar una reparacion a la lista de reparaciones asignadas al tecnico"""
        self._reparaciones_asignadas.append(reparacion)

    def ver_reparaciones_asignadas(self):
        """Metodo para ver las reparaciones asignadas al tecnico"""
        if not self._reparaciones_asignadas:
            return f"No hay reparaciones asignadas al técnico {self.nombre}."
        return self._reparaciones_asignadas
