"""Modulo encargado de persistencia de datos con la base de datos"""
import mysql.connector
from models.tecnico import Tecnico
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

    # GESTION DE CLIENTES

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

    # GESTION DE DISPOSITIVOS

    def guardar_dispositivo(self, dispositivo):
        conexion = self._obtener_conexion()

        if conexion is None:
            return False

        try:

            ejecutar = conexion.cursor()

            query = "INSERT INTO dispositivos (imei, marca, modelo, cliente_id) VALUES (%s,%s,%s,%s)"

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

    # GESTION DE TECNICOS

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

    # GESTION DE REPARACIONES
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
