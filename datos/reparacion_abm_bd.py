"""Importamos mysqlconector y las clases que se utilizan para los abm en esta clase"""

import mysql.connector
from models.cliente import Cliente
from models.dispositivo import Dispositivo
from models.tecnico import Tecnico
from models.reparacion import Reparacion
from datos.conexion_base_bd import ConexionBaseBD

class ReparacionABMBD (ConexionBaseBD):
    """Clase con la persistencia y las consultas avanzadas con la tabla 'reparaciones' """

    def guardar_reparacion(self, reparacion):

        conexion = self._obtener_conexion()
        if conexion is None:
            return None

        try:

            ejecutar = conexion.cursor()

            query = """INSERT INTO reparaciones
                    (falla, estado, notas, dispositivo_imei, tecnico_id)
                    VALUES (%s,%s,%s,%s,%s)"""

            valores = (reparacion.falla, reparacion.estado, reparacion.notas,
                       reparacion.dispositivo.imei, reparacion.tecnico.id_tecnico)

            ejecutar.execute(query, valores)
            conexion.commit()

            reparacion.id_reparacion = ejecutar.lastrowid
            print(" Orden de reparacion creada con exito")

        except mysql.connector.Error:
            return None

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

    def obtener_reparaciones(self):
        conexion = self._obtener_conexion()
        if conexion is None:
            return []
        lista_reparaciones = []

        try:
            ejecutar = conexion.cursor(dictionary=True)

            query = """SELECT r.id_reparacion, r.falla, r.estado,
                    r.fecha_ingreso, r.notas, d.imei, d.marca,
                    d.modelo, c.documento, c.telefono, c.correo,
                    c.nombre AS nombre_cliente, c.apellido AS apellido_cliente
                    FROM reparaciones r
                    INNER JOIN dispositivos d
                    ON r.dispositivo_imei = d.imei
                    INNER JOIN clientes c
                    ON d.cliente_id = c.id_cliente"""

            ejecutar.execute(query)
            filas = ejecutar.fetchall()

            for fila in filas:
                cliente_listado = Cliente(
                    None,
                    fila['nombre_cliente'],
                    fila['apellido_cliente'],
                    fila['documento'],
                    fila['telefono'],
                    fila['correo']
                )

                equipo_listado = Dispositivo(
                    fila['imei'],
                    fila['marca'],
                    fila['modelo'],
                    cliente_listado
                )

                reparacion_listado = Reparacion(
                    fila['id_reparacion'],
                    equipo_listado,
                    None,
                    fila['falla'],
                    fila['notas'] if fila['notas'] else ""
                )

                reparacion_listado.estado = fila['estado']
                lista_reparaciones.append(reparacion_listado)

        except mysql.connector.Error:
            return []

        finally:
            ejecutar.close()
            conexion.close()

        return lista_reparaciones

    def actualizar_reparacion(self, reparacion):

        conexion = self._obtener_conexion()
        if conexion is None:
            print("No se pudo establecer la conexión a la base de datos.")
            return False

        try:

            ejecutar = conexion.cursor()

            # Mandamos el UPDATE apuntando especificamente al ID de la orden

            query = """
                UPDATE reparaciones
                SET estado = %s, notas = %s
                WHERE id_reparacion = %s
            """

            valores = (reparacion.estado, reparacion.notas, reparacion.id)

            ejecutar.execute(query, valores)
            conexion.commit()
            if ejecutar.rowcount > 0:
                return True
            else:
                print("No se encontró la orden con el ID proporcionado.")
                return False

        except mysql.connector.Error as error_mysql:
            print(f"Error al actualizar la reparacion: {error_mysql}")
            return False

        finally:
            ejecutar.close()
            conexion.close()

    def buscar_reparacion_por_id(self, id_reparacion):
        """Busca una reparacion por si ID y devuelve un objeto Rep"""
        conexion = self._obtener_conexion()
        if conexion is None:
            return None

        ejecutar = None

        try:

            ejecutar = conexion.cursor(dictionary=True)

            query = """SELECT r.id_reparacion, r.falla, r.estado,
                    r.notas, r.fecha_ingreso, d.imei, d.marca,
                    d.modelo, t.id_tecnico, t.nombre AS nombre_tecnico,
                    t.apellido AS apellido_tecnico,
                    t.documento AS documento_tecnico, t.telefono, t.turno
                    FROM reparaciones r
                    INNER JOIN dispositivos d
                    ON r.dispositivo_imei = d.imei
                    INNER JOIN tecnicos t
                    ON r.tecnico_id = t.id_tecnico
                    WHERE r.id_reparacion = %s"""

            ejecutar.execute(query, (id_reparacion,))
            resultado = ejecutar.fetchone()

            if resultado:
                equipo = Dispositivo(
                    resultado['imei'],
                    resultado['marca'],
                    resultado['modelo'],
                    None
                )
                tecnico = Tecnico(
                    resultado['id_tecnico'],
                    resultado['nombre_tecnico'],
                    resultado['apellido_tecnico'],
                    resultado['documento_tecnico'],
                    resultado['telefono'],
                    resultado['turno']
                )
                orden_reparacion = Reparacion(
                    resultado['id_reparacion'],
                    equipo,
                    tecnico,
                    resultado['falla'],
                    resultado['notas'] if resultado['notas'] else ""
                )

                orden_reparacion.estado = resultado['estado']
                orden_reparacion.fecha_ingreso = resultado['fecha_ingreso']

                return orden_reparacion

        except mysql.connector.Error:
            return None

        finally:
            if conexion:
                ejecutar.close()
                conexion.close()

        return None

