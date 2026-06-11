"""Modulo que contiene la clase Reparacion."""


class Reparacion:
    """ Clase que representa una orden de reparación. """

    def __init__(self, id_reparacion, dispositivo_obj,
                 tecnico_obj, falla_reportada, notas_tecnico=""):
        """ Inicializa una nueva orden de reparación con su ID,
        dispositivo, falla reportada, estado inicial e ingreso."""

        self.dispositivo = dispositivo_obj
        self.tecnico = tecnico_obj
        self.falla = falla_reportada

        try:

            self.id = id_reparacion
            self.estado = "INGRESADO"
            self.notas = notas_tecnico
        except ValueError as e:
            print(f"Error al crear la reparación: {e}")

        if self.dispositivo is not None:

            # Vinculacion con el historial de reparaciones del dispositivo
            self.dispositivo.actualizar_historial_reparaciones(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):

        if valor is None:
            self._id = None
            return

        try:
            valor_int = int(valor)
            if valor < 0:
                raise ValueError(
                    "El ID de la orden debe ser un número entero positivo.")
            self._id = valor_int
        except (ValueError, TypeError) as exc:
            raise ValueError(
                "El ID de la orden debe ser un número entero positivo.") from exc

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado):
        """ Valida que el estado pertenezca a las opciones permitidas en el taller. """
        try:

            # Limpiamos y estandarizamos a mayúsculas como tenías en tu diseño
            estado_limpio = nuevo_estado.strip().upper()
            estados_validos = ["INGRESADO", "EN DIAGNOSTICO",
                               "EN REPARACION", "LISTO", "ENTREGADO", "CANCELADO"]

            if estado_limpio not in estados_validos:
                raise ValueError

            self._estado = estado_limpio
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError(
                f"Estado inválido. Los estados válidos son: {', '.join(estados_validos)}.") from exc

    def cambiar_estado(self, nuevo_estado):
        """Actualiza el estado de la reparación, asegurándose de que el nuevo estado sea válido."""
        try:

            self.estado = nuevo_estado
            return True
        except ValueError as e:
            print(f"Error al cambiar el estado: {e}")
            return False

    def agregar_nota_tecnico(self, nota):
        """Agrega una nota del técnico a la reparación."""
        try:

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

            return True
        except ValueError as exc:
            print(f"Error al agregar la nota: {exc}")
            return False
