"""Modulo encargado dela conexion con la base de datos"""

import mysql.connector


class ConexionBaseBD:
    """Constructor con la conexion a la BD"""

    def __init__(self):

        self.config_db = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': 'taller_celulares',
            'port': 3307,
            "use_pure": True
        }

    def _obtener_conexion(self):

        try:

            # Establece una conexión a la base de datos utilizando los parámetros configurados
            conexion = mysql.connector.connect(**self.config_db)
            return conexion

        except mysql.connector.Error as error_mysql:
            print(f"Error al conectar a la base de datos: {error_mysql}")
            # En caso de error, se devuelve None para indicar que no se pudo establecer la conexión
            return None
