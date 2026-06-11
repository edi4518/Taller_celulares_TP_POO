"""Modulo que contiene la clase Persona."""


class Persona:
    """ Clase que representa a una persona. """

    def __init__(self, nombre, apellido, documento, telefono):


        try:
            self.nombre = nombre
            self.apellido = apellido
            self.documento = documento
            self.telefono = telefono
        except ValueError as e:
            print(f"Error al crear la persona: {e}")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        try:

            nombre_limpio = nombre.strip()
            if not nombre_limpio:
                raise ValueError("El nombre no puede estar vacío.")
            self._nombre = nombre_limpio
        except (ValueError, TypeError, AttributeError) as e:
            raise ValueError("El nombre no puede estar vacío.") from e

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, apellido):
        try:

            apellido_limpio = apellido.strip()
            if not apellido_limpio:
                raise ValueError("El apellido no puede estar vacío.")
            self._apellido = apellido_limpio
        except (ValueError, TypeError, AttributeError) as e:
            raise ValueError("El apellido no puede estar vacío.") from e

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, documento):
        try:
            documento_limpio = str(documento).strip()
            if not documento_limpio or documento_limpio == 'None':
                raise ValueError(
                    "El documento no puede estar vacío.")
            self._documento = documento_limpio
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError("El documento debe ser una cadena de texto no vacía.") from exc

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        try:
            telefono_limpio = telefono.strip()
            if not telefono_limpio or telefono_limpio == 'None':
                raise ValueError("El teléfono no puede estar vacío.")
            self._telefono = telefono_limpio
        except (ValueError, TypeError, AttributeError) as exc:
                raise ValueError("El teléfono debe ser una cadena de texto válida (ej: '1123456789')") from exc
