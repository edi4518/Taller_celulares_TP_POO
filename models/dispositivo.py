"""Modulo que contiene la clase Dispositivo."""


class Dispositivo:
    """ Clase que representa un dispositivo. """

    def __init__(self, imei, marca, modelo, cliente_obj):
        """ Inicializa un nuevo dispositivo con su IMEI, marca, modelo y cliente asociado. """

        self.imei = imei
        self.marca = marca
        self.modelo = modelo

        # El cliente asociado al dispositivo se almacena como un objeto de la clase cliente.
        self.cliente = cliente_obj

        # Lista interna para almacenar el historial de sus reparaciones
        self._historial_reparaciones = []

    @property
    def imei(self):
        return self._imei

    @imei.setter
    def imei(self, valor):

        try:
            valor_str = str(valor).strip()
            if len(valor_str) != 15 or not valor_str.isdigit():
                raise ValueError("El IMEI debe ser un número de 15 dígitos.")
            self._imei = valor_str
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Error al establecer el IMEI: {exc}") from exc

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, valor):
        marcas_validas = ["Apple", "Samsung", "Huawei", "Xiaomi",
                          "Motorola", "Sony", "LG", "Nokia", "TCL", "Otras"]

        try:
            valor_cap = str(valor).strip()

            if valor_cap.upper() in ["LG", "TCL"]:
                valor_cap = valor_cap.upper()
            else:
                valor_cap = valor_cap.capitalize()

            if valor_cap not in marcas_validas:
                raise ValueError(
                    f"La marca debe ser una de las siguientes: {', '.join(marcas_validas)}.")
            self._marca = valor_cap
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError(f"Error al establecer la marca: {exc}") from exc

    def obtener_historial_reparaciones(self):
        """ Devuelve el historial de reparaciones del dispositivo.
        Si no hay reparaciones, devuelve una lista vacía.
        """
        return self._historial_reparaciones

    def actualizar_historial_reparaciones(self, reparacion):
        """ Agrega una nueva reparación al historial del dispositivo. """

        try:
            if reparacion is None:
                raise ValueError("La reparación no puede estar vacía.")
            self._historial_reparaciones.append(reparacion)
        except ValueError as exc:
            print(f"Error al actualizar el historial de reparaciones: {exc}")
            return False

        return True
