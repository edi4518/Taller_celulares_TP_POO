"""Importamos conexion y clases del Dispositivo"""
import mysql.connector
from models.dispositivo import Dispositivo
from models.cliente import Cliente
from datos.conexion_base_bd import ConexionBaseBD


class DispositivoABMBD(ConexionBaseBD):

    """Clase especializada en la persistencia y consultas con la tablas 'dispositivos'"""
    def guardar_dispositivo(self, dispositivo):

        conexion = self._obtener_conexion()

        if conexion is None:
            return False

        try:

            ejecutar = conexion.cursor()

            query = """INSERT INTO dispositivos
            (imei, marca, modelo, cliente_id)
            VALUES
            (%s,%s,%s,%s)"""

            valores = (dispositivo.imei, dispositivo.marca,
                    dispositivo.modelo, dispositivo.cliente.id_cliente)

            ejecutar.execute(query, valores)
            conexion.commit()
            return True

        except mysql.connector.Error as error_mysql:
            print(f"Error al guardar dispositivo: {error_mysql}")
            return False

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

    def obtener_dispositivos(self):
        conexion = self._obtener_conexion()
        if conexion is None:
            return []

        lista_dispositivos = []

        try:
            ejecutar = conexion.cursor(dictionary=True)

            query = """SELECT
                    d.imei, d.marca, d.modelo,
                    c.id_cliente, c.nombre AS nombre_cliente,
                    c.apellido AS apellido_cliente, c.documento,
                    c.telefono, c.correo
                    FROM dispositivos d
                    INNER JOIN clientes c
                    ON d.cliente_id = c.id_cliente"""

            ejecutar.execute(query)
            filas = ejecutar.fetchall()

            for fila in filas:
                cliente_listado = Cliente(
                    id_cliente=fila['id_cliente'],
                    nombre=fila['nombre_cliente'],
                    apellido=fila['apellido_cliente'],
                    documento=fila['documento'],
                    telefono=fila['telefono'],
                    correo=fila['correo']

                )

                equipo_listado = Dispositivo(
                    imei=fila['imei'],
                    marca=fila['marca'],
                    modelo=fila['modelo'],
                    cliente_obj=cliente_listado
                )

                lista_dispositivos.append(equipo_listado)

        except mysql.connector.Error:
            return []

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

        return lista_dispositivos

    def eliminar_dispositivo_por_cliente(self, id_cliente):
        conexion = self._obtener_conexion()

        if conexion is None:
            return False
        try:
            ejecutar = conexion.cursor()

            query = "DELETE FROM dispositivos WHERE cliente_id = %s"
            ejecutar.execute(query, (id_cliente,))
            conexion.commit()
            return True
        except mysql.connector.Error as error_mysql:
            print(f"Error al eliminar dispositivo: {error_mysql}")
            return False

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

    def buscar_dispositivo_por_imei(self, imei):
        conexion = self._obtener_conexion()
        if conexion is None:
            return None

        try:

            ejecutar = conexion.cursor(dictionary=True)

            query = """SELECT d.imei, d.marca, d.modelo, d.cliente_id,
                    c.nombre AS nombre_cliente, c.apellido AS apellido_cliente,
                    c.documento, c.telefono, c.correo
                    FROM dispositivos d
                    INNER JOIN clientes c
                    ON d.cliente_id = c.id_cliente WHERE d.imei = %s"""

            ejecutar.execute(query, (imei,))
            resultado = ejecutar.fetchone()

            if resultado:
                dueño = Cliente(
                    id_cliente=resultado['cliente_id'],
                    nombre=resultado['nombre_cliente'],
                    apellido=resultado['apellido_cliente'],
                    documento=resultado['documento'],
                    telefono=resultado['telefono'],
                    correo=resultado['correo']
                )

                return Dispositivo(
                    imei=resultado['imei'],
                    marca=resultado['marca'],
                    modelo=resultado['modelo'],
                    cliente_obj=dueño
                )

        except mysql.connector.Error:
            return None

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()



