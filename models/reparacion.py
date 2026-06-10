"""Modulo que contiene la clase Reparacion."""

class Reparacion:
    """ Clase que representa una orden de reparación. """

    def __init__(self, id_reparacion, dispositivo_obj,
                tecnico_obj, falla_reportada,notas_tecnico=""):
        """ Inicializa una nueva orden de reparación con su ID, 
        dispositivo, falla reportada, estado inicial e ingreso."""
        self.id = id_reparacion
        self.dispositivo = dispositivo_obj
        self.tecnico = tecnico_obj
        self.falla = falla_reportada
        self.estado = "INGRESADO"
        self.notas = notas_tecnico

        # Vinculacion con el historial de reparaciones del dispositivo
        self.dispositivo.actualizar_historial_reparaciones(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError(
                "El ID de la orden debe ser un número entero positivo.")
        self._id = valor

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado):
        """ Valida que el estado pertenezca a las opciones permitidas en el taller. """
        # Limpiamos y estandarizamos a mayúsculas como tenías en tu diseño
        estado_limpio = nuevo_estado.strip().upper()
        estados_validos = ["INGRESADO", "EN DIAGNOSTICO",
                           "EN REPARACION", "LISTO", "ENTREGADO", "CANCELADO"]

        if estado_limpio not in estados_validos:
            raise ValueError(
                f"Estado inválido. Los estados válidos son: {', '.join(estados_validos)}.")

        self._estado = estado_limpio

    def cambiar_estado(self, nuevo_estado):
        """Actualiza el estado de la reparación, asegurándose de que el nuevo estado sea válido."""
        self.estado = nuevo_estado
        print(
            f"Orden N°: {self.id} - Estado actualizado con exito a: {self.estado}")

    def agregar_nota_tecnico(self, nota):
        """Agrega una nota del técnico a la reparación."""
        nota_limpia = nota.strip()
        if not nota_limpia:
            raise ValueError("La nota del técnico no puede estar vacía.")
        if self.notas == "":
            # Si es la primera nota, la guardamos directo con un guion
            self.notas = f"- {nota_limpia}"
        else:

            self.notas += f"\n- {nota_limpia}"

        print(
            f"Nota agregada con exito al registro de reparacion N°: {self.id}")
