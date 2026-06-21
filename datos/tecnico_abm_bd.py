"""Clase con la importacion de mysqlconector y con las clases del Tecnico"""

import mysql.connector
from datos.conexion_base_bd import ConexionBaseBD
from models.tecnico import Tecnico

class TecnicoABMBD(ConexionBaseBD):

    """Clase con la persistencia y los metedos de consultas e inserción con la tabla 'tecnicos'"""

    def guardar_tecnico(self, tecnico):
        conexion = self._obtener_conexion()
        if conexion is None:
            return None
        try:

            ejecutar = conexion.cursor()

            query = """INSERT INTO tecnicos
                    (nombre, apellido, documento, telefono, turno)
                    VALUES (%s,%s,%s,%s,%s)"""

            valores = (tecnico.nombre, tecnico.apellido,
                       tecnico.documento, tecnico.telefono, tecnico.turno)

            ejecutar.execute(query, valores)
            conexion.commit()

            tecnico.id_tecnico = ejecutar.lastrowid

        except mysql.connector.Error:
            return None

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

    def obtener_tecnicos(self):
        # Establece una conexion con la BD.
        conexion = self._obtener_conexion()

        if conexion is None:
            return []

        try:
            ejecutar = conexion.cursor(dictionary=True)

            # Generamos la consulta SQL para obtener todos
            # los tecnicos registrados en la tabla "tecnicos".
            query = "SELECT * FROM tecnicos"
            ejecutar.execute(query)
            filas = ejecutar.fetchall()

        except mysql.connector.Error as error_mysql:
            print(f"Error al obtener tecnicos: {error_mysql}")
            return []

        finally:
            ejecutar.close()
            conexion.close()

        lista_tecnicos = []

        for fila in filas:
            # Recorremos cada fila obtenida de la consulta, creando un objeto Tecnico.
            tecnico_obj = Tecnico(
                id_tecnico=fila['id_tecnico'],
                nombre=fila['nombre'],
                apellido=fila['apellido'],
                documento=fila['documento'],
                telefono=fila['telefono'],
                turno=fila['turno']
            )

            lista_tecnicos.append(tecnico_obj)
        return lista_tecnicos