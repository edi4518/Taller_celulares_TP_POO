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
        if not isinstance(valor, str) or len(valor) != 15 or not valor.isdigit():
            raise ValueError("El IMEI debe tener 15 dígitos.")
        self._imei = valor

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, valor):
        marcas_validas = ["Apple", "Samsung", "Huawei", "Xiaomi",
                        "Motorola", "Sony", "LG", "Nokia", "TCL", "Otras"]

        if valor.capitalize() not in marcas_validas:
            raise ValueError(
                f"La marca debe ser una de las siguientes: {', '.join(marcas_validas)}.")
        self._marca = valor.capitalize()

    def obtener_historial_reparaciones(self):
        """ Devuelve el historial de reparaciones del dispositivo.
        Si no hay reparaciones, devuelve un mensaje indicando
        que no hay reparaciones registradas. """

        if not self._historial_reparaciones:
            return f"No hay reparaciones registradas para el IMEI {self.imei}"
        return self._historial_reparaciones

    def actualizar_historial_reparaciones(self, reparacion):
        """ Agrega una nueva reparación al historial del dispositivo. """

        self._historial_reparaciones.append(reparacion)
