"""Modulo que se encarga del menu del sistema de gestion de reparaciones"""
from models.dispositivo import Dispositivo
from models.tecnico import Tecnico
from models.cliente import Cliente
from models.reparacion import Reparacion


class InterfazSimple:
    """Recibe la instancia de la capa de datos(repositorio)"""

    def __init__(self, repositorio):
        self.datos = repositorio

    def iniciar(self):
        """Metodo para iniciar la interfaz, 
        muestra el menu principal y espera la opcion del usuario"""

        if not self.datos.obtener_tecnicos():
            tecnico_inicial = Tecnico(
                1, "Eduardo", "Incrocci", "30021371", "1123456789", "MAÑANA")
            self.datos.guardar_tecnico(tecnico_inicial)

        while True:
            print("\n" + "="*40)
            print("--- SISTEMA DE GESTION DE REPARACIONES ---")
            print("="*40)
            print("1. Registrar Cliente y Dispositivo")
            print("2- Modificar datos de Cliente")
            print("3. Crear Nueva Orden de Reparacion")
            print("4. Cambiar Estado de una Orden de Reparacion")
            print("5. Agregar Nota del Tecnico a una Orden de Reparacion")
            print("6. Listar Reparaciones del Taller")
            print("7. Salir")
            print("="*40)

            opcion = input("Seleccione una opcion (1-7): ")

            if opcion == "1":
                self._registrar_cliente_y_dispositivo()
            elif opcion == "2":
                self._modificar_datos_cliente()
            elif opcion == "3":
                self._crear_orden()
            elif opcion == "4":
                self._modificar_estado()
            elif opcion == "5":
                self._agregar_nota()
            elif opcion == "6":
                self._listar_reparaciones()
            elif opcion == "7":
                print("\nSaliendo del sistema...")
                break
            else:
                print("\nOpcion invalida. Por favor, intente nevamente.")

    def _registrar_cliente_y_dispositivo(self):
        # Metodo para registrar un nuevo cliente y su dispositivo asociado
        print("\n--- PASO 1: REGISTRO DEL CLIENTE ---")
        nombre = input("Ingrese el nombre del cliente: ")
        apellido = input("Ingrese el apellido del cliente: ")
        dni = input("Ingrese el DNI del cliente: ")

        telefono = input("Ingrese el telefono del cliente: ")
        # Validamos que el telefono tenga al menos 10 digitos y solo contenga numeros
        while not telefono or not telefono.isdigit() or len(telefono) < 10:
            print(
                """Telefono invalido. Asegurese de ingresar
                un numero de telefono valido (minimo 10 digitos).""")
            telefono = input("Ingrese el telefono del cliente: ")

        correo = input("Ingrese el email del cliente: ").strip()
        # Validamos que el correo tenga el formato correcto
        while "@" not in correo or "." not in correo:
            print("""Correo invalido. Asegurese de que el correo
                  tenga el formato correcto (ej: usuario@dominio.com)""")
            correo = input("Ingrese el email del cliente: ").strip()

        nuevo_cliente = Cliente(
            0, nombre, apellido, dni, telefono, correo)

        print("\n--- PASO 2: REGISTRO DEL DISPOSITIVO ---")

        imei = input("Numero de IMEI (15 digitos): ")
        # Validamos que el IMEI tenga exactamente 15 digitos y solo contenga numeros
        while not imei or not imei.isdigit() or len(imei) != 15:
            print(
                """IMEI invalido. Asegurese de ingresar 
                un numero de IMEI valido (exactamente 15 digitos).""")
            imei = input("Numero de IMEI (15 digitos): ")

        if self.datos.buscar_dispositivo_por_imei(imei) is not None:
            print("\n El IMEI ingresado ya existe en el sistema. Intente nuevamente.")

        marcas_validas = ["Apple", "Samsung", "Huawei", "Xiaomi",
                          "Motorola", "Sony", "LG", "Nokia", "TCL", "Otras"]

        while True:
            marca = input(
                f"Marca ({', '.join(marcas_validas)}): ").strip().capitalize()
            if marca in marcas_validas:
                break
            print("Marca inválida. Intente nuevamente.")

        modelo = input("Modelo: ")

        nuevo_dispositivo = Dispositivo(imei, marca, modelo, nuevo_cliente)

        self.datos.guardar_cliente(nuevo_cliente)
        self.datos.guardar_dispositivo(nuevo_dispositivo)

        print("\nCliente y Dispositivo registrados exitosamente!")

    def _modificar_datos_cliente(self):
        print("\n--- MODIFICAR DATOS DE CLIENTE ---")
        clientes = self.datos.obtener_clientes()
        if not clientes:
            print("\n No hay clientes registrados. Cargue un cliente primero.")
            return
        print("\n Seleccione el cliente a modificar:")
        for i, cliente in enumerate(clientes):
            print(
                f"{i}) {cliente.nombre} {cliente.apellido} | DNI: {cliente.documento}")
            id_cliente = int(input("Ingrese el numero del cliente: "))
            cliente_seleccionado = clientes[id_cliente]
            print("\n Ingrese la opcion que desea modificar: ")
            print("1. Telefono")
            print("2. Correo Electronico")
            opcion_modificar = input("Seleccione una opcion (1-2): ")
            if opcion_modificar == "1":
                nuevo_telefono = input("Ingrese el nuevo telefono: ")
                cliente_seleccionado.actualizar_datos(
                    nuevo_telefono=nuevo_telefono)

                self.datos.actualizar_cliente(cliente_seleccionado)

                print("\nTelefono actualizado exitosamente!")

            elif opcion_modificar == "2":
                nuevo_correo = input("Ingrese el nuevo correo electronico: ")
                cliente_seleccionado.actualizar_datos(
                    nuevo_correo=nuevo_correo)
                self.datos.actualizar_cliente(cliente_seleccionado)

                print("\nCorreo electronico actualizado exitosamente!")

    def _crear_orden(self):
        print("\n--- CREAR ORDEN DE REPARACIÓN ---")
        dispositivos = self.datos.obtener_dispositivos()

        if not dispositivos:
            print(
                "\n No hay equipos registrados. Cargue un cliente y dispositivo primero.")
            return

        print("\n Selecciones el dispositivo:")
        for i, dispositivo in enumerate(dispositivos):
            print(f"""[{i}] {dispositivo.marca} {dispositivo.modelo} |
                  Cliente: {dispositivo.cliente.nombre}
                  {dispositivo.cliente.apellido}""")

        id_dispositivo = int(input("Ingrese el numero del dispositivo: "))
        falla_reportada = input("Describa la falla reportada: ")
        tecnico_asignado = self.datos.obtener_tecnicos()[0]

        # Se instancia Reparacion sin el tecnico (el modelo no lo recibe ahí)
        nueva_orden = Reparacion(
            0, dispositivos[id_dispositivo], tecnico_asignado, falla_reportada)
        tecnico_asignado.agregar_reparacion(nueva_orden)

        self.datos.guardar_reparacion(nueva_orden)
        print(f"\n Orden #{nueva_orden.id} creada exitosamente!")

    def _modificar_estado(self):
        # Traemos las reparaciones
        ordenes = self.datos.obtener_reparaciones()
        if not ordenes:
            print("\n No hay ordenes en el taller")
            return

        print("\n--- ORDENES EN EL TALLER ---")
        # Listamos las ordenes existentes en la BD
        for i, orden in enumerate(ordenes):
            print(
                f"""[{i}] Orden #{orden.id} |
                Dispositivo: {orden.dispositivo.modelo} |
                Estado: {orden.estado}""")

        # Pedimos al usuario que ingrese la orden de reaparacion que desea modificar.
        id_buscar = int(input("\nIngrese el ID de la orden a modificar: "))

        orden_encontrada = self.datos.buscar_reparacion_por_id(id_buscar)

        if orden_encontrada:

            print(
                f"""\nOrden Encontrada: {orden_encontrada.dispositivo.marca}
                {orden_encontrada.dispositivo.modelo}""")
            print(f"Estado actual: {orden_encontrada.estado}")

            print("\nSeleccione el nuevo estado:")
            print("[1] INGRESADO")
            print("[2] EN DIAGNOSTICO")
            print("[3] EN REPARACION")
            print("[4] LISTO")
            print("[5] ENTREGADO")
            print("[6] CANCELADO")

            opcion_elegida = input("Ingrese el numero del nuevo estado: ")

            # Asignamos el valor correspondiente elegido a la opcion correcta

            if opcion_elegida == "1":
                nuevo_estado = "INGRESADO"
            elif opcion_elegida == "2":
                nuevo_estado = "EN DIAGNOSTICO"
            elif opcion_elegida == "3":
                nuevo_estado = "EN REPARACION"
            elif opcion_elegida == "4":
                nuevo_estado = "LISTO"
            elif opcion_elegida == "5":
                nuevo_estado = "ENTREGADO"
            elif opcion_elegida == "6":
                nuevo_estado = "CANCELADO"
            else:
                print("\nOpcion Invalida. Intente nuevamente.")
                return

            orden_encontrada.estado = nuevo_estado

            self.datos.actualizar_reparacion(orden_encontrada)
            print(
                f"\nEstado actualizado con exito a {nuevo_estado} en la base de datos")

        else:
            print("\n No se encontro ninguna orden con ese ID.")

    def _agregar_nota(self):
        # Traemos las reparaciones
        ordenes = self.datos.obtener_reparaciones()
        if not ordenes:
            print("\n No hay ordenes registradas en el taller")
            return

        print("\n" + "="*40)
        print("--- ORDENES EN EL TALLER ---")
        print("="*40)
        # Listar las ordenes de reparacion registradas en el sistema
        for orden in ordenes:
            print(
                f"""\Orden N°: {orden.id} |
                Equipo: {orden.dispositivo.marca} {orden.dispositivo.modelo} |
                Estado: {orden.estado}""")
            print(
                f"""Cliente: {orden.dispositivo.cliente.nombre}
                {orden.dispositivo.cliente.apellido} |
                Falla: {orden.falla}""")
            print("="*40)

        id_buscar = int(input("\nIngrese el ID de la orden a agregar nota: "))

        orden_encontrada = self.datos.buscar_reparacion_por_id(id_buscar)

        if orden_encontrada:
            nota = input("Escriba los detalles tecnicos: ")
            orden_encontrada.agregar_nota_tecnico(nota)

            self.datos.actualizar_reparacion(orden_encontrada)

            print("\nNota agregada con exito al sistema")
        else:
            print("\nNo se encontró la orden con el ID proporcionado.")

    def _listar_reparaciones(self):
        ordenes = self.datos.obtener_reparaciones()
        # Si no hay ordenes, mostramos un mensaje y retornamos al menu
        if not ordenes:
            print("\nNo hay ordenes registradas en el taller.")
            return

        print("\n" + "="*40)
        print("--- REPARACIONES EN EL TALLER ---")
        print("="*40)

        # Listamos las ordenes con sus detalles.
        for orden in ordenes:
            print(f"\nORDEN #{orden.id} -- Estado: {orden.estado}")
            print(
                f""""Equipo: {orden.dispositivo.marca} {orden.dispositivo.modelo} |
                Falla: {orden.falla} | IMEI: {orden.dispositivo.imei}""")
            print(f"""Cliente: {orden.dispositivo.cliente.nombre}
                  {orden.dispositivo.cliente.apellido} |
                  DNI: {orden.dispositivo.cliente.documento} |
                  Telefono: {orden.dispositivo.cliente.telefono}""")
            print(
                f"Notas Tecnicas:\n{orden.notas if orden.notas else 'No hay notas agregadas.'}")
            print("="*40)
