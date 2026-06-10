"""Modulo encargado de iniciar la aplicacion"""
from datos.repositorio import RepositorioDatos
from presentacion.menu import InterfazSimple


def iniciar_aplicacion():
    """Funcion para iniciar la aplicacion, 
    que crea una instancia del repositorio y del menu, 
    y luego muestra el menu al usuario"""
    base_de_datos = RepositorioDatos()
    interfaz = InterfazSimple(base_de_datos)

    interfaz.iniciar()


# Se encarga de verificar si se ejecuta directamente esta clase para iniar la app
if __name__ == "__main__":
    iniciar_aplicacion()
