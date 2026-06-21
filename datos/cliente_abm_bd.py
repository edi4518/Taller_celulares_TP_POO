
import mysql.connector
from models.cliente import Cliente
from datos.conexion_base_bd import ConexionBaseBD


class ClienteADMBD(ConexionBaseBD):

    """Clase especializada en el ABM y consultas de la tabla 'clientes'"""

    def guardar_cliente(self, cliente):
        # Establece una conexion con la BD.
        conexion = self._obtener_conexion()

        if conexion is None:
            return None

        try:
            ejecutar = conexion.cursor()

            # Generamos la consulta SQL para insertar un nuevo cliente en la tabla "clientes".
            query = """INSERT INTO clientes(
                    nombre, apellido, documento, telefono, correo)
                    VALUES
                    (%s,%s,%s,%s,%s)"""

            valores = (cliente.nombre, cliente.apellido,
                       cliente.documento, cliente.telefono, cliente.correo)

            ejecutar.execute(query, valores)
            conexion.commit()

            cliente.id_cliente = ejecutar.lastrowid
            return cliente.id_cliente

        except mysql.connector.Error as error_mysql:
            print(f"Error al guardar cliente: {error_mysql}")
            return None

        finally:
            ejecutar.close()
            conexion.close()

    def obtener_clientes(self):
        conexion = self._obtener_conexion()

        if conexion is None:
            return []

        # Lista vacia donde vamos a ir guardando los objetos Cliente ya fabricados
        lista_clientes = []

        try:
            ejecutar = conexion.cursor(dictionary=True)

            query = "SELECT * FROM clientes"
            ejecutar.execute(query)

            # Obtener todas las filas resultantes de la consulta
            filas = ejecutar.fetchall()

            # Iteramos sobre cada fila obtenida de la consulta,
            # creando un objeto Cliente con los datos de cada fila.

            for fila in filas:
                cliente_obj = Cliente(
                    id_cliente=fila['id_cliente'],
                    nombre=fila['nombre'],
                    apellido=fila['apellido'],
                    documento=fila['documento'],
                    telefono=fila['telefono'],
                    correo=fila['correo']
                )
                lista_clientes.append(cliente_obj)

        except mysql.connector.Error:
            return []

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

        return lista_clientes

    def actualizar_cliente(self, cliente):
        # Modifica los datos del correo o tel de un cliente existente en BD

        conexion = self._obtener_conexion()

        if conexion is None:
            return False

        try:

            ejecutar = conexion.cursor()

            query = """UPDATE clientes SET
                    nombre = %s, apellido = %s,
                    documento = %s,telefono = %s,
                    correo = %s
                    WHERE id_cliente = %s"""

            valores = (cliente.nombre, cliente.apellido, cliente.documento,
                       cliente.telefono, cliente.correo, cliente.id_cliente)

            ejecutar.execute(query, valores)
            conexion.commit()
            return True

        except mysql.connector.Error:
            return False

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente de la base de datos dado su ID
        """

        conexion = self._obtener_conexion()

        if conexion is None:
            return False

        try:

            ejecutar = conexion.cursor()

            query = "DELETE FROM clientes WHERE id_cliente = %s"

            ejecutar.execute(query, (id_cliente,))
            conexion.commit()

            if ejecutar.rowcount > 0:
                return True
            return False

        except mysql.connector.Error as error_mysql:
            print(f"Error al eliminar cliente: {error_mysql}")
            return False

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

