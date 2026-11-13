from datos import DECIMALES, ESTADOS, buscar_producto, crear_pedido
from validaciones import pedir_entero, pedir_opcion, pedir_texto_no_vacio

OPCION_VOLVER = 0
OPCION_LISTAR_PEDIDOS = 1
OPCION_VER_DETALLE = 2
OPCION_CAMBIAR_ESTADO = 3
OPCION_ESTADISTICAS = 4
OPCION_MAXIMA = 4

FILTRO_TODOS = "todos"
FILTRO_ESTADO = "estado"
FILTROS_PEDIDOS = (FILTRO_TODOS, FILTRO_ESTADO)

ACCION_AVANZAR = "avanzar"
ACCION_CANCELAR = "cancelar"
ACCIONES_ESTADO = (ACCION_AVANZAR, ACCION_CANCELAR)

ESTADO_RECIBIDO = ESTADOS[0]
ESTADO_EN_PREPARACION = ESTADOS[1]
ESTADO_EN_REPARTO = ESTADOS[2]
ESTADO_ENTREGADO = ESTADOS[3]
ESTADO_CANCELADO = ESTADOS[4]

MENSAJE_SIN_PEDIDOS = "No hay pedidos con ese criterio."
MENSAJE_PEDIDO_NO_EXISTE = "Error: no existe ningún pedido con ese identificador."
MENSAJE_NO_AVANZA = "Error: el pedido está en un estado final y no puede avanzar."
MENSAJE_NO_CANCELABLE = f"Error: solo se puede cancelar un pedido en estado {ESTADO_RECIBIDO}."
MENSAJE_SIN_VENTAS = "Todavía no hay ventas (los pedidos cancelados no cuentan)."
MENSAJE_NOTA_CANCELADOS = "Los pedidos cancelados no cuentan en ingresos ni en ventas."

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


def calcular_siguiente_estado(estado):
    if estado == ESTADO_RECIBIDO:
        return ESTADO_EN_PREPARACION
    if estado == ESTADO_EN_PREPARACION:
        return ESTADO_EN_REPARTO
    if estado == ESTADO_EN_REPARTO:
        return ESTADO_ENTREGADO
    return None


def reemplazar_estado(pedidos, id_pedido, nuevo_estado):
    nuevos = []
    for pedido in pedidos:
        if pedido["id_pedido"] == id_pedido:
            nuevos.append(crear_pedido(pedido["id_pedido"], pedido["cliente"],
                                       pedido["direccion"], pedido["lineas"],
                                       nuevo_estado))
        else:
            nuevos.append(pedido)
    return nuevos


def cambiar_estado_pedido(pedidos):
    id_pedido = pedir_texto_no_vacio("Identificador del pedido: ").upper()
    pedido = buscar_pedido(pedidos, id_pedido)
    if pedido is None:
        print(MENSAJE_PEDIDO_NO_EXISTE)
        return pedidos
    print(f"El pedido {id_pedido} está en estado {pedido['estado']}.")
    accion = pedir_opcion("¿Qué quieres hacer?", ACCIONES_ESTADO)
    if accion == ACCION_AVANZAR:
        nuevo_estado = calcular_siguiente_estado(pedido["estado"])
        if nuevo_estado is None:
            print(MENSAJE_NO_AVANZA)
            return pedidos
    else:
        if pedido["estado"] != ESTADO_RECIBIDO:
            print(MENSAJE_NO_CANCELABLE)
            return pedidos
        nuevo_estado = ESTADO_CANCELADO
    print(f"Pedido {id_pedido}: {pedido['estado']} -> {nuevo_estado}.")
    return reemplazar_estado(pedidos, id_pedido, nuevo_estado)


def calcular_ingresos(pedidos):
    ingresos = 0
    numero_pedidos = 0
    for pedido in pedidos:
        if pedido["estado"] != ESTADO_CANCELADO:
            ingresos = ingresos + pedido["total_eur"]
            numero_pedidos = numero_pedidos + 1
    return round(ingresos, DECIMALES), numero_pedidos


def contar_unidades_vendidas(pedidos):
    unidades = {}
    for pedido in pedidos:
        if pedido["estado"] != ESTADO_CANCELADO:
            for id_producto, cantidad, precio_unitario in pedido["lineas"]:
                if id_producto in unidades:
                    unidades[id_producto] = unidades[id_producto] + cantidad
                else:
                    unidades[id_producto] = cantidad
    return unidades


def buscar_mas_vendido(unidades):
    mejor_id = None
    mejor_cantidad = 0
    for id_producto in unidades:
        if unidades[id_producto] > mejor_cantidad:
            mejor_id = id_producto
            mejor_cantidad = unidades[id_producto]
    return mejor_id, mejor_cantidad


def mostrar_estadisticas(catalogo, pedidos):
    print(SEPARADOR_DETALLE)
    print("Pedidos por estado:")
    for estado in ESTADOS:
        cuantos = len(filtrar_pedidos_por_estado(pedidos, estado))
        print(f"  {estado}: {cuantos}")
    ingresos, numero_pedidos = calcular_ingresos(pedidos)
    if numero_pedidos == 0:
        print(MENSAJE_SIN_VENTAS)
        print(SEPARADOR_DETALLE)
        return
    ticket_medio = round(ingresos / numero_pedidos, DECIMALES)
    id_mas_vendido, unidades = buscar_mas_vendido(contar_unidades_vendidas(pedidos))
    nombre = buscar_producto(catalogo, id_mas_vendido)["nombre"]
    print(f"Ingresos totales: {ingresos:.2f} €")
    print(f"Ticket medio: {ticket_medio:.2f} €")
    print(f"Producto más vendido: {nombre} ({id_mas_vendido}) con {unidades} unidades")
    print(MENSAJE_NOTA_CANCELADOS)
    print(SEPARADOR_DETALLE)


def menu_empresa(catalogo, pedidos):
    salir = False
    while not salir:
        print(MENU_EMPRESA)
        opcion = pedir_entero("Elige una opción: ", OPCION_VOLVER, OPCION_MAXIMA)
        if opcion == OPCION_LISTAR_PEDIDOS:
            listar_pedidos(pedidos)
        elif opcion == OPCION_VER_DETALLE:
            ver_detalle_pedido(catalogo, pedidos)
        elif opcion == OPCION_CAMBIAR_ESTADO:
            pedidos = cambiar_estado_pedido(pedidos)
        elif opcion == OPCION_ESTADISTICAS:
            mostrar_estadisticas(catalogo, pedidos)
        else:
            salir = True
    return pedidos