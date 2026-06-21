"""Modulo encargado de persistencia de datos con la base de datos"""

from datos.cliente_abm_bd import ClienteADMBD
from datos.dispositivo_abm_bd import DispositivoABMBD
from datos.tecnico_abm_bd import TecnicoABMBD
from datos.reparacion_abm_bd import ReparacionABMBD


class RepositorioDatos(ClienteADMBD, DispositivoABMBD, TecnicoABMBD, ReparacionABMBD):

    """
        Clase unificadora del sistema de persistencia.
        Utiliza herencia múltiple para agrupar todos los módulos ABM especializados
        en una única interfaz limpia para la capa de presentación (Menú).
        """

    def __init__(self):
        # Inicializa el constructor de ConexionBaseBD para configurar las credenciales de MySQL
        super().__init__()

        print(
            "\n🚀 [Sistema de Datos] Módulos de persistencia vinculados con éxito.")
