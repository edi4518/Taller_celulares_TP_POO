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

            opcion = input("Seleccione una opcion (1-7): ").strip()

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

        while not dni or not dni.isdigit():
            print("DNI invalido. Asegurese de ingresar un numero de DNI valido.")
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
            None, nombre, apellido, dni, telefono, correo)

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
                f"Marca ({', '.join(marcas_validas)}): ").strip()
            if marca.upper() in ["LG", "TCL"]:
                marca = marca.upper()
            else:
                marca = marca.capitalize()

            if marca in marcas_validas:
                break
            print("Marca inválida. Intente nuevamente.")

        modelo = input("Modelo: ").strip()

        print("\n Validando datos ingresados...")
        try:
            nuevo_cliente = Cliente(
                None, nombre, apellido, dni, telefono, correo)
            nuevo_dispositivo = Dispositivo(imei, marca, modelo, nuevo_cliente)
        except ValueError as exc:
            print(f"Error al crear cliente o dispositivo: {exc}")
            print("Registro cancelado. Intente nuevamente.")
            return

        print("\n Datos válidos. Registrando...")

        id_cliente_creado = self.datos.guardar_cliente(nuevo_cliente)

        if id_cliente_creado:
            nuevo_cliente.id_cliente = id_cliente_creado
            if self.datos.guardar_dispositivo(nuevo_dispositivo):
                print("\nCliente y dispositivo registrado exitosamente!")
            else:
                print("\nError al registrar el dispositivo. Intente nuevamente.")
                print(
                    "El cliente registrado se eliminará para mantener la consistencia de los datos.")
                self.datos.eliminar_dispositivo_por_cliente(
                    nuevo_cliente.id_cliente)
                self.datos.eliminar_cliente(id_cliente_creado)

                print("Registro cancelado. Intente nuevamente.")
        else:
            print("\nError al registrar el cliente. Intente nuevamente.")

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

        try:
            id_cliente = int(input("Ingrese el numero del cliente: "))
            if id_cliente < 0 or id_cliente >= len(clientes):
                print("\n Numero de cliente invalido. Intente nuevamente.")
                return
        except ValueError:
            print("\n Entrada invalida. Por favor, ingrese un numero valido.")
            return

        cliente_seleccionado = clientes[id_cliente]
        print("\n Ingrese la opcion que desea modificar: ")
        print("1. Telefono")
        print("2. Correo Electronico")
        opcion_modificar = input("Seleccione una opcion (1-2): ")
        if opcion_modificar == "1":
            nuevo_telefono = input("Ingrese el nuevo telefono: ")
            if cliente_seleccionado.actualizar_datos(
                    nuevo_telefono=nuevo_telefono):
                if self.datos.actualizar_cliente(cliente_seleccionado):
                    print("\nTelefono actualizado exitosamente!")
                else:
                    print("\nError al actualizar el telefono en la base de datos.")
            else:
                print("\nTelefono invalido. Intente nuevamente.")

        elif opcion_modificar == "2":
            nuevo_correo = input("Ingrese el nuevo correo electronico: ")
            if cliente_seleccionado.actualizar_datos(
                    nuevo_correo=nuevo_correo):
                if self.datos.actualizar_cliente(cliente_seleccionado):
                    print("\nCorreo electronico actualizado exitosamente!")
                else:
                    print(
                        "\nError al actualizar el correo electronico en la base de datos.")
            else:
                print("\nCorreo electronico invalido. Intente nuevamente.")

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

        try:
            id_dispositivo = int(input("Ingrese el numero del dispositivo: "))
            if id_dispositivo < 0 or id_dispositivo >= len(dispositivos):
                print("\n Seleccion de dispositivo invalida. Intente nuevamente.")
                return
        except ValueError:
            print("\n Entrada invalida. Por favor, ingrese un numero valido.")
            return
        falla_reportada = input("Describa la falla reportada: ").strip()
        if not falla_reportada:
            print(
                "\n La descripcion de la falla no puede estar vacia. Intente nuevamente.")
            return

        tecnico = self.datos.obtener_tecnicos()
        if not tecnico:
            print("\n No hay tecnicos disponibles. Intente mas tarde.")
            return
        tecnico_asignado = tecnico[0]

        # Se instancia Reparacion sin el tecnico (el modelo no lo recibe ahí)
        nueva_orden = Reparacion(
            None, dispositivos[id_dispositivo], tecnico_asignado, falla_reportada)
        tecnico_asignado.agregar_reparacion(nueva_orden)

        id_orden_creada = self.datos.guardar_reparacion(nueva_orden)
        if id_orden_creada:
            nueva_orden.id = id_orden_creada
            tecnico_asignado.agregar_reparacion(nueva_orden)
            print(f"\n Orden #{nueva_orden.id} creada exitosamente!")
        else:
            print("\n Error al crear la orden de reparacion. Intente nuevamente.")

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
                f""" Orden N°: {orden.id} |
                Dispositivo: {orden.dispositivo.modelo} |
                Estado: {orden.estado}""")

        try:

            # Pedimos al usuario que ingrese la orden de reaparacion que desea modificar.
            id_buscar = int(input("\nIngrese el ID de la orden a modificar: "))
        except ValueError:
            print("\n Entrada invalida. Por favor, ingrese un numero valido.")
            return

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
            opcion_elegida = input(
                "Ingrese el numero del nuevo estado: ").strip()

            estados = {
                "1": "INGRESADO",
                "2": "EN DIAGNOSTICO",
                "3": "EN REPARACION",
                "4": "LISTO",
                "5": "ENTREGADO",
                "6": "CANCELADO"
            }

            # Asignamos el valor correspondiente elegido a la opcion correcta

            if opcion_elegida in estados:
                nuevo_estado = estados[opcion_elegida]
                if orden_encontrada.cambiar_estado(nuevo_estado):
                    if self.datos.actualizar_reparacion(orden_encontrada):

                        print(
                            f"\nEstado actualizado exitosamente a {nuevo_estado} en el sistema.")
                    else:
                        print("\nError al actualizar el estado en la base de datos.")

                else:
                    print("\nEstado invalido. Intente nuevamente.")

            else:
                print("\nOpcion invalida. Intente nuevamente.")
        else:
            print("\nNo se encontró la orden con el ID proporcionado.")

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
                f"""\nOrden N°: {orden.id} |
                Equipo: {orden.dispositivo.marca} {orden.dispositivo.modelo} |
                Estado: {orden.estado}""")
            print(
                f"""Cliente: {orden.dispositivo.cliente.nombre}
                {orden.dispositivo.cliente.apellido} |
                Falla: {orden.falla}""")
            print("="*40)
        try:
            id_buscar = int(
                input("\nIngrese el ID de la orden a agregar nota: "))
        except ValueError:
            print("\n Entrada invalida. Por favor, ingrese un numero valido.")
            return

        orden_encontrada = self.datos.buscar_reparacion_por_id(id_buscar)

        if orden_encontrada:
            nota = input("Escriba los detalles tecnicos: ").strip()
            if orden_encontrada.agregar_nota_tecnico(nota):
                if self.datos.actualizar_reparacion(orden_encontrada):
                    print("\nNota agregada con exito al sistema")
                else:
                    print("\nError al agregar la nota en la orden. Intente nuevamente.")
            else:
                print("\nError: La nota no puede ser procesada. Intente nuevamente.")
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
                f"Equipo: {orden.dispositivo.marca} {orden.dispositivo.modelo}")
            print(f"IMEI: {orden.dispositivo.imei}")
            print(f"Falla: {orden.falla}")
            print("-" * 50)
            print(
                f"Cliente: {orden.dispositivo.cliente.nombre} {orden.dispositivo.cliente.apellido}")
            print(
                f"DNI: {orden.dispositivo.cliente.documento} | Tel: {orden.dispositivo.cliente.telefono}")
            print("-" * 50)

            notas_formateadas = orden.notas if orden.notas else "No hay notas agregadas."
            print(f" Notas Técnicas:\n{notas_formateadas}")
            print("="*50)
