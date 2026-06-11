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

        try:
            self.id_tecnico = id_tecnico
            self.turno = turno
        except ValueError as e:
            print(f"Error al crear el técnico: {e}")


        # Lista para almacenar las reparaciones asignadas al técnico
        self._reparaciones_asignadas = []

    @property
    def id_tecnico(self):
        """Metodo para obtener el id del tecnico"""
        return self._id_tecnico

    @id_tecnico.setter
    def id_tecnico(self, valor):
        """Metodo para establecer el id del tecnico, validando que sea un numero entero y positivo"""
        if valor is None:
            self._id_tecnico = None
            return

        try:
            valor = int(valor)
            if valor < 0:
                raise ValueError("El ID del técnico debe ser un número entero positivo.")
            self._id_tecnico = valor
        except (ValueError, TypeError) as e:
            raise ValueError("El ID del técnico debe ser un número entero positivo.") from e


    @property
    def turno(self):
        """Metodo para obtener el turno del tecnico"""
        return self._turno

    @turno.setter
    def turno(self, valor):
        """Metodo para establecer el turno del tecnico, validando que sea un turno valido"""
        turnos_validos = ['MAÑANA', 'TARDE', 'NOCHE']

        try:
            valor_upper = str(valor).strip().upper()

            if valor_upper not in turnos_validos:
                raise ValueError
            self._turno = valor_upper

        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError(f"""Turno inválido.
                             Los turnos válidos son: {', '.join(turnos_validos)}.""") from exc

    def agregar_reparacion(self, reparacion):
        """Metodo para agregar una reparacion a la lista de reparaciones asignadas al tecnico"""
        self._reparaciones_asignadas.append(reparacion)

    def ver_reparaciones_asignadas(self):
        """Metodo para ver las reparaciones asignadas al tecnico"""
        if not self._reparaciones_asignadas:
            return f"No hay reparaciones asignadas al técnico {self.nombre}."
        return self._reparaciones_asignadas
