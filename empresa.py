from datos import ESTADOS, buscar_producto
from validaciones import pedir_entero, pedir_opcion, pedir_texto_no_vacio

OPCION_VOLVER = 0
OPCION_LISTAR_PEDIDOS = 1
OPCION_VER_DETALLE = 2
OPCION_MAXIMA = 4

FILTRO_TODOS = "todos"
FILTRO_ESTADO = "estado"
FILTROS_PEDIDOS = (FILTRO_TODOS, FILTRO_ESTADO)

MENSAJE_PROXIMAMENTE = "Próximamente."
MENSAJE_SIN_PEDIDOS = "No hay pedidos con ese criterio."
MENSAJE_PEDIDO_NO_EXISTE = "Error: no existe ningún pedido con ese identificador."

ANCHO_ID = 10
ANCHO_CLIENTE = 22
ANCHO_TOTAL = 12
ANCHO_ESTADO = 16
ANCHO_LINEA = ANCHO_ID + ANCHO_CLIENTE + ANCHO_TOTAL + ANCHO_ESTADO
SEPARADOR = "-" * ANCHO_LINEA

ANCHO_DETALLE = 60
SEPARADOR_DETALLE = "-" * ANCHO_DETALLE

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


def buscar_pedido(pedidos, id_pedido):
    for pedido in pedidos:
        if pedido["id_pedido"] == id_pedido:
            return pedido
    return None


def mostrar_detalle(catalogo, pedido):
    print(SEPARADOR_DETALLE)
    print(f"Pedido:    {pedido['id_pedido']}")
    print(f"Cliente:   {pedido['cliente']}")
    print(f"Dirección: {pedido['direccion']}")
    print("Líneas:")
    for id_producto, cantidad, precio_unitario in pedido["lineas"]:
        nombre = buscar_producto(catalogo, id_producto)["nombre"]
        subtotal = cantidad * precio_unitario
        print(f"  {cantidad} x {nombre} ({id_producto}) a {precio_unitario:.2f} € = {subtotal:.2f} €")
    print(f"Total:     {pedido['total_eur']:.2f} €")
    print(f"Estado:    {pedido['estado']}")
    print(SEPARADOR_DETALLE)


def ver_detalle_pedido(catalogo, pedidos):
    id_pedido = pedir_texto_no_vacio("Identificador del pedido: ").upper()
    pedido = buscar_pedido(pedidos, id_pedido)
    if pedido is None:
        print(MENSAJE_PEDIDO_NO_EXISTE)
        return
    mostrar_detalle(catalogo, pedido)


def menu_empresa(catalogo, pedidos):
    salir = False
    while not salir:
        print(MENU_EMPRESA)
        opcion = pedir_entero("Elige una opción: ", OPCION_VOLVER, OPCION_MAXIMA)
        if opcion == OPCION_LISTAR_PEDIDOS:
            listar_pedidos(pedidos)
        elif opcion == OPCION_VER_DETALLE:
            ver_detalle_pedido(catalogo, pedidos)
        elif opcion == OPCION_VOLVER:
            salir = True
        else:
            print(MENSAJE_PROXIMAMENTE)
    return pedidos