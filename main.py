from datos import CATALOGO, PEDIDOS, crear_carrito_vacio
from validaciones import pedir_entero
from cliente import menu_cliente
from empresa import menu_empresa

OPCION_SALIR = 0
OPCION_CLIENTE = 1
OPCION_EMPRESA = 2

MENSAJE_DESPEDIDA = "Hasta pronto."

MENU_PRINCIPAL = (
    "\n=== CALIMA DELIVERY ===\n" +
    "1. Modo cliente\n" +
    "2. Modo empresa\n" +
    "0. Salir")


def menu_principal(catalogo, pedidos):
    carrito = crear_carrito_vacio()
    salir = False
    while not salir:
        print(MENU_PRINCIPAL)
        opcion = pedir_entero("Elige una opción: ", OPCION_SALIR, OPCION_EMPRESA)
        if opcion == OPCION_CLIENTE:
            carrito, pedidos = menu_cliente(catalogo, carrito, pedidos)
        elif opcion == OPCION_EMPRESA:
            pedidos = menu_empresa(catalogo, pedidos)
        else:
            salir = True
    print(MENSAJE_DESPEDIDA)


menu_principal(CATALOGO, PEDIDOS)