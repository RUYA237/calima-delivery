from datos import ESTADOS
from validaciones import pedir_entero, pedir_opcion

OPCION_VOLVER = 0
OPCION_LISTAR_PEDIDOS = 1
OPCION_MAXIMA = 4

FILTRO_TODOS = "todos"
FILTRO_ESTADO = "estado"
FILTROS_PEDIDOS = (FILTRO_TODOS, FILTRO_ESTADO)

MENSAJE_PROXIMAMENTE = "Próximamente."
MENSAJE_SIN_PEDIDOS = "No hay pedidos con ese criterio."

ANCHO_ID = 10
ANCHO_CLIENTE = 22
ANCHO_TOTAL = 12
ANCHO_ESTADO = 16
ANCHO_LINEA = ANCHO_ID + ANCHO_CLIENTE + ANCHO_TOTAL + ANCHO_ESTADO
SEPARADOR = "-" * ANCHO_LINEA

MENU_EMPRESA = (
    "\n--- MODO EMPRESA ---\n" +
    "1. Listar pedidos\n" +
    "2. Ver detalle de un pedido\n" +
    "3. Cambiar estado de un pedido\n" +
    "4. Ver estadísticas\n" +
    "0. Volver al menú principal")


def filtrar_pedidos_por_estado(pedidos, estado):
    filtrados = []
    for pedido in pedidos:
        if pedido["estado"] == estado:
            filtrados.append(pedido)
    return filtrados


def mostrar_listado_pedidos(pedidos):
    if len(pedidos) == 0:
        print(MENSAJE_SIN_PEDIDOS)
        return
    print(SEPARADOR)
    print(f"{'Pedido':<{ANCHO_ID}}{'Cliente':<{ANCHO_CLIENTE}}"
          f"{'Total (€)':>{ANCHO_TOTAL}}{'Estado':>{ANCHO_ESTADO}}")
    print(SEPARADOR)
    for pedido in pedidos:
        id_pedido = pedido["id_pedido"]
        cliente = pedido["cliente"]
        total = pedido["total_eur"]
        estado = pedido["estado"]
        print(f"{id_pedido:<{ANCHO_ID}}{cliente:<{ANCHO_CLIENTE}}"
              f"{total:>{ANCHO_TOTAL}.2f}{estado:>{ANCHO_ESTADO}}")
    print(SEPARADOR)
    print(f"{len(pedidos)} pedido(s) mostrados.")


def listar_pedidos(pedidos):
    filtro = pedir_opcion("¿Qué pedidos quieres listar?", FILTROS_PEDIDOS)
    if filtro == FILTRO_TODOS:
        seleccionados = pedidos
    else:
        estado = pedir_opcion("Estado", ESTADOS)
        seleccionados = filtrar_pedidos_por_estado(pedidos, estado)
    mostrar_listado_pedidos(seleccionados)


def menu_empresa(pedidos):
    salir = False
    while not salir:
        print(MENU_EMPRESA)
        opcion = pedir_entero("Elige una opción: ", OPCION_VOLVER, OPCION_MAXIMA)
        if opcion == OPCION_LISTAR_PEDIDOS:
            listar_pedidos(pedidos)
        elif opcion == OPCION_VOLVER:
            salir = True
        else:
            print(MENSAJE_PROXIMAMENTE)