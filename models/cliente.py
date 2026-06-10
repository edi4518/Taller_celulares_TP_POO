"""Modulo que contiene la clase Cliente."""
from models.persona import Persona


class Cliente(Persona):
    """Clase que representa a un cliente."""
    def __init__(self, id_cliente, nombre, apellido, documento, telefono, correo):
        """Constructor de la clase Cliente, que inicializa los atributos del cliente"""
        super().__init__(nombre, apellido, documento, telefono)
        self.id_cliente = id_cliente
        self.correo = correo

    # Getters y Setters para el id del cliente,
    # con validacion para asegurar que sea un numero entero y mayor a 0
    @property
    def id_cliente(self):
        return self._id

    @id_cliente.setter
    def id_cliente(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError(
                "El id del cliente debe ser un numero entero y mayor a 0")
        self._id = valor

    @property
    def correo(self):
        return self._email

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise ValueError(
                "El correo debe ser del estilo ejemplo@dominio.com")
        self._email = valor

    def actualizar_datos(self, nuevo_telefono=None, nuevo_correo=None):
        """Metodo para actualizar los datos del cliente 
        ya sea el telefono de contacto como el correo electronico,
        si no se ingresa alguno de los dos datos,
        se mantiene el valor anterior"""
        if nuevo_telefono:
            self.telefono = nuevo_telefono
        if nuevo_correo:
            self.correo = nuevo_correo

        return f"""Los datos del cliente {self.nombre}
                fueron actualizados con exito"""
