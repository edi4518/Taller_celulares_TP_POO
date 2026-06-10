"""Modulo que contiene la clase Persona."""


class Persona:
    """ Clase que representa a una persona. """

    def __init__(self, nombre, apellido, documento, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = nombre_limpio

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, apellido):
        apellido_limpio = apellido.strip()
        if not apellido_limpio:
            raise ValueError("El apellido no puede estar vacío.")
        self._apellido = apellido_limpio

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, documento):
        if not isinstance(documento, str):
            raise ValueError(
                "El documento debe ser una cadena de texto (ej: '23456789')")
        documento_limpio = documento.strip()
        if not documento_limpio:
            raise ValueError("El documento no puede estar vacío.")
        self._documento = documento_limpio

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        if not isinstance(telefono, str):
            raise ValueError(
                "El teléfono debe ser una cadena de texto (ej: '1123456789')")
        telefono_limpio = telefono.strip()
        if not telefono_limpio:
            raise ValueError("El teléfono no puede estar vacío.")
        self._telefono = telefono_limpio
