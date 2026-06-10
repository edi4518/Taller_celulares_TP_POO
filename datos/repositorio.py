"""Modulo encargado de persistencia de datos con la base de datos"""
from models.tecnico import Tecnico
import mysql.connector
from models.cliente import Cliente
from models.dispositivo import Dispositivo
from models.reparacion import Reparacion


class RepositorioDatos:
    """Construtor de la clase RepositorioDatos que
    se encarga de realizar la conexion a la base de datos"""

    def __init__(self,):
        # Configuramos parametros de conexion a la base de datos

        self.config_db = {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'database': 'taller_celulares',
            'port': 3307
        }

    def _obtener_conexion(self):
        # Establece una conexión a la base de datos utilizando los parámetros configurados
        return mysql.connector.connect(**self.config_db)

    # GESTION DE CLIENTES

    def guardar_cliente(self, cliente):
        # Establece una conexion con la BD.
        conexion = self._obtener_conexion()
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

        ejecutar.close()
        conexion.close()

    def obtener_clientes(self):
        conexion = self._obtener_conexion()
        ejecutar = conexion.cursor(dictionary=True)

        query = "SELECT * FROM clientes"
        ejecutar.execute(query)

        # Obtener todas las filas resultantes de la consulta
        filas = ejecutar.fetchall()

        ejecutar.close()
        conexion.close()

        # Lista vacia donde vamos a ir guardando los objetos Cliente ya fabricados
        lista_clientes = []

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
        return lista_clientes

    def actualizar_cliente(self, cliente):
        # Modifica los datos del correo o tel de un cliente existente en BD

        conexion = self._obtener_conexion()
        ejecutar = conexion.cursor()

        query = """UPDATE clientes SET
                nombre = %s, apellido = %s,
                documento = %s,telefono = %s,
                correo = %s
                WHERE id_cliente = %s"""

        valores = (cliente.nombre, cliente.apellido, cliente.documento,
                   cliente.teklefono, cliente.correo, cliente.id_cliente)

        ejecutar.execute(query, valores)
        conexion.commit()

        ejecutar.close()
        conexion.close()

    # GESTION DE DISPOSITIVOS

    def guardar_dispositivo(self, dispositivo):
        conexion = self._obtener_conexion()
        ejecutar = conexion.cursor()

        query = "INSERT INTO dispositivos (imei, marca, modelo, cliente_id) VALUES (%s,%s,%s,%s)"

        valores = (dispositivo.imei, dispositivo.marca,
                   dispositivo.modelo, dispositivo.cliente.id_cliente)

        ejecutar.execute(query, valores)
        conexion.commit()

        ejecutar.close()
        conexion.close()

    def obtener_dispositivos(self):
        conexion = self._obtener_conexion()
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

        ejecutar.close()
        conexion.close()

        lista_dispositivos = []

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
        return lista_dispositivos

    def buscar_dispositivo_por_imei(self, imei):
        conexion = self._obtener_conexion()
        ejecutar = conexion.cursor(dictionary=True)

        query = """SELECT d.imei, d.marca, d.modelo, d.cliente_id,
                c.nombre AS nombre_cliente, c.apellido AS apellido_cliente,
                c.documento, c.telefono, c.correo
                FROM dispositivos d
                INNER JOIN clientes c
                ON d.cliente_id = c.id_cliente WHERE d.imei = %s"""

        ejecutar.execute(query, (imei,))
        resultado = ejecutar.fetchone()

        ejecutar.close()
        conexion.close()

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
        return None

    # GESTION DE TECNICOS
    def guardar_tecnico(self, tecnico):
        conexion = self._obtener_conexion()
        ejecutar = conexion.cursor()

        query = """INSERT INTO tecnicos
                (nombre, apellido, documento, telefono, turno)
                VALUES (%s,%s,%s,%s,%s)"""

        valores = (tecnico.nombre, tecnico.apellido,
                   tecnico.documento, tecnico.telefono, tecnico.turno)

        ejecutar.execute(query, valores)
        conexion.commit()

        tecnico.id_tecnico = ejecutar.lastrowid

        ejecutar.close()
        conexion.close()

    def obtener_tecnicos(self):
        # Establece una conexion con la BD.
        conexion = self._obtener_conexion()
        ejecutar = conexion.cursor(dictionary=True)

        # Generamos la consulta SQL para obtener todos
        # los tecnicos registrados en la tabla "tecnicos".
        query = "SELECT * FROM tecnicos"
        ejecutar.execute(query)
        filas = ejecutar.fetchall()

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

    # GESTION DE REPARACIONES
    def guardar_reparacion(self, reparacion):

        conexion = self._obtener_conexion()
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

        ejecutar.close()
        conexion.close()

    def obtener_reparaciones(self):
        conexion = self._obtener_conexion()
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

        ejecutar.close()
        conexion.close()

        lista_reparaciones = []
        for fila in filas:
            cliente_listado = Cliente(
                id_cliente=0,
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

            reparacion_listado = Reparacion(
                id_reparacion=fila['id_reparacion'],
                dispositivo_obj=equipo_listado,
                tecnico_obj=None,
                falla_reportada=fila['falla'],
                notas_tecnico=fila["notas"]
            )
            reparacion_listado.estado = fila['estado']
            lista_reparaciones.append(reparacion_listado)
        return lista_reparaciones

    def actualizar_reparacion(self, reparacion):

        conexion = self._obtener_conexion()
        ejecutar = conexion.cursor()

        # Mandamos el UPDATE apuntando especificamente al ID de la orden

        query = "UPDATE reparaciones SET estado = %s, notas = %s WHERE id_reparacion = %s"

        valores = (reparacion.estado, reparacion.notas, reparacion.id)

        ejecutar.execute(query, valores)
        conexion.commit()

        ejecutar.close()
        conexion.close()

    def buscar_reparacion_por_id(self, id_reparacion):
        """Busca una reparacion por si ID y devuelve un objeto Rep"""
        conexion = self._obtener_conexion()
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

        ejecutar.close()
        conexion.close()

        if resultado:
            equipo = Dispositivo(
                resultado['imei'], resultado['marca'], resultado['modelo'], None)

            tecnico = Tecnico(
                id_tecnico=resultado['id_tecnico'],
                nombre=resultado['nombre_tecnico'],
                apellido=resultado['apellido_tecnico'],
                documento=resultado['documento_tecnico'],
                telefono=resultado['telefono'],
                turno=resultado['turno']
            )

            orden_reparacion = Reparacion(
                dispositivo_obj=equipo,
                tecnico_obj=tecnico,
                falla_reportada=resultado['falla'],
                id_reparacion=resultado['id_reparacion']
            )

            orden_reparacion.estado = resultado['estado']
            orden_reparacion.notas = resultado['notas']
            orden_reparacion.fecha_ingreso = resultado['fecha_ingreso']

            return orden_reparacion
        return None
