from datos import (CATEGORIAS, ESTADO_INICIAL, buscar_producto, carrito_a_lineas,
                   calcular_subtotal, calcular_envio, calcular_total,
                   crear_carrito_vacio, crear_pedido, generar_id_pedido)
from validaciones import pedir_entero, pedir_opcion, pedir_texto_no_vacio

OPCION_VOLVER = 0
OPCION_VER_CATALOGO = 1
OPCION_ANADIR_CARRITO = 2
OPCION_QUITAR_CARRITO = 3
OPCION_VER_CARRITO = 4
OPCION_CONFIRMAR_PEDIDO = 5
OPCION_VER_MIS_PEDIDOS = 6
OPCION_MAXIMA = 6

ID_CANCELAR = "0"
CANTIDAD_MINIMA = 1

FILTRO_TODO = "todo"
FILTRO_RESTAURANTE = "restaurante"
FILTRO_CATEGORIA = "categoria"
FILTROS_CATALOGO = (FILTRO_TODO, FILTRO_RESTAURANTE, FILTRO_CATEGORIA)

TEXTO_DISPONIBLE = "Sí"
TEXTO_NO_DISPONIBLE = "No"
MENSAJE_CATALOGO_VACIO = "No hay productos con ese criterio."
MENSAJE_ID_NO_EXISTE = "Error: no existe ningún producto con ese identificador."
MENSAJE_NO_DISPONIBLE = "Error: ese producto no está disponible ahora mismo."
MENSAJE_NO_EN_CARRITO = "Error: ese producto no está en el carrito."
MENSAJE_CARRITO_VACIO = "El carrito está vacío."
MENSAJE_CANCELADA = "Operación cancelada."
MENSAJE_PEDIDO_CONFIRMADO = "Pedido confirmado."
MENSAJE_SIN_PEDIDOS_CLIENTE = "No hay pedidos a nombre de ese cliente."

ANCHO_ID = 6
ANCHO_NOMBRE = 30
ANCHO_RESTAURANTE = 16
ANCHO_CATEGORIA = 14
ANCHO_PRECIO = 11
ANCHO_DISPONIBLE = 13
ANCHO_LINEA = (ANCHO_ID + ANCHO_NOMBRE + ANCHO_RESTAURANTE + ANCHO_CATEGORIA
               + ANCHO_PRECIO + ANCHO_DISPONIBLE)
SEPARADOR = "-" * ANCHO_LINEA

ANCHO_CARRITO_NOMBRE = 30
ANCHO_CARRITO_CANTIDAD = 10
ANCHO_CARRITO_PRECIO = 13
ANCHO_CARRITO_SUBTOTAL = 15
ANCHO_LINEA_CARRITO = (ANCHO_ID + ANCHO_CARRITO_NOMBRE + ANCHO_CARRITO_CANTIDAD
                       + ANCHO_CARRITO_PRECIO + ANCHO_CARRITO_SUBTOTAL)
ANCHO_ETIQUETA_RESUMEN = ANCHO_LINEA_CARRITO - ANCHO_CARRITO_SUBTOTAL
SEPARADOR_CARRITO = "-" * ANCHO_LINEA_CARRITO

ANCHO_MIS_PEDIDOS_ID = 10
ANCHO_MIS_PEDIDOS_TOTAL = 12
ANCHO_MIS_PEDIDOS_ESTADO = 16
ANCHO_LINEA_MIS_PEDIDOS = (ANCHO_MIS_PEDIDOS_ID + ANCHO_MIS_PEDIDOS_TOTAL
                           + ANCHO_MIS_PEDIDOS_ESTADO)
SEPARADOR_MIS_PEDIDOS = "-" * ANCHO_LINEA_MIS_PEDIDOS

MENU_CLIENTE = (
    "\n--- MODO CLIENTE ---\n" +
    "1. Ver catálogo\n" +
    "2. Añadir producto al carrito\n" +
    "3. Quitar producto del carrito\n" +
    "4. Ver carrito\n" +
    "5. Confirmar pedido\n" +
    "6. Ver mis pedidos\n" +
    "0. Volver al menú principal")


def obtener_restaurantes(catalogo):
    vistos = set()
    restaurantes = []
    for producto in catalogo:
        restaurante = producto["restaurante"]
        if restaurante not in vistos:
            vistos.add(restaurante)
            restaurantes.append(restaurante)
    return restaurantes


def filtrar_catalogo(catalogo, campo, valor):
    filtrados = []
    for producto in catalogo:
        if producto[campo] == valor:
            filtrados.append(producto)
    return filtrados


def mostrar_catalogo(productos):
    if len(productos) == 0:
        print(MENSAJE_CATALOGO_VACIO)
        return
    print(SEPARADOR)
    print(f"{'ID':<{ANCHO_ID}}{'Producto':<{ANCHO_NOMBRE}}"
          f"{'Restaurante':<{ANCHO_RESTAURANTE}}{'Categoría':<{ANCHO_CATEGORIA}}"
          f"{'Precio (€)':>{ANCHO_PRECIO}}{'Disponible':>{ANCHO_DISPONIBLE}}")
    print(SEPARADOR)
    for producto in productos:
        id_producto = producto["id_producto"]
        nombre = producto["nombre"]
        restaurante = producto["restaurante"]
        categoria = producto["categoria"]
        precio = producto["precio_eur"]
        if producto["disponible"]:
            disponible = TEXTO_DISPONIBLE
        else:
            disponible = TEXTO_NO_DISPONIBLE
        print(f"{id_producto:<{ANCHO_ID}}{nombre:<{ANCHO_NOMBRE}}"
              f"{restaurante:<{ANCHO_RESTAURANTE}}{categoria:<{ANCHO_CATEGORIA}}"
              f"{precio:>{ANCHO_PRECIO}.2f}{disponible:>{ANCHO_DISPONIBLE}}")
    print(SEPARADOR)
    print(f"{len(productos)} producto(s) mostrados.")


def ver_catalogo(catalogo):
    filtro = pedir_opcion("¿Cómo quieres ver el catálogo?", FILTROS_CATALOGO)
    if filtro == FILTRO_TODO:
        productos = catalogo
    elif filtro == FILTRO_RESTAURANTE:
        restaurante = pedir_opcion("Restaurante", obtener_restaurantes(catalogo))
        productos = filtrar_catalogo(catalogo, FILTRO_RESTAURANTE, restaurante)
    else:
        categoria = pedir_opcion("Categoría", sorted(CATEGORIAS))
        productos = filtrar_catalogo(catalogo, FILTRO_CATEGORIA, categoria)
    mostrar_catalogo(productos)


def copiar_carrito(carrito):
    copia = {}
    for id_producto in carrito:
        copia[id_producto] = carrito[id_producto]
    return copia


def pedir_producto_disponible(catalogo):
    while True:
        id_producto = pedir_texto_no_vacio(
            f"Identificador del producto ({ID_CANCELAR} para cancelar): ").upper()
        if id_producto == ID_CANCELAR:
            return None
        producto = buscar_producto(catalogo, id_producto)
        if producto is None:
            print(MENSAJE_ID_NO_EXISTE)
        elif not producto["disponible"]:
            print(MENSAJE_NO_DISPONIBLE)
        else:
            return producto


def anadir_al_carrito(catalogo, carrito):
    producto = pedir_producto_disponible(catalogo)
    if producto is None:
        print(MENSAJE_CANCELADA)
        return carrito
    cantidad = pedir_entero("Cantidad: ", CANTIDAD_MINIMA)
    nuevo = copiar_carrito(carrito)
    id_producto = producto["id_producto"]
    if id_producto in nuevo:
        nuevo[id_producto] = nuevo[id_producto] + cantidad
    else:
        nuevo[id_producto] = cantidad
    print(f"Añadido: {cantidad} x {producto['nombre']}.")
    return nuevo


def quitar_del_carrito(catalogo, carrito):
    if len(carrito) == 0:
        print(MENSAJE_CARRITO_VACIO)
        return carrito
    while True:
        id_producto = pedir_texto_no_vacio(
            f"Identificador del producto a quitar ({ID_CANCELAR} para cancelar): ").upper()
        if id_producto == ID_CANCELAR:
            print(MENSAJE_CANCELADA)
            return carrito
        if id_producto in carrito:
            nuevo = {}
            for clave in carrito:
                if clave != id_producto:
                    nuevo[clave] = carrito[clave]
            nombre = buscar_producto(catalogo, id_producto)["nombre"]
            print(f"Quitado del carrito: {nombre}.")
            return nuevo
        print(MENSAJE_NO_EN_CARRITO)


def mostrar_carrito(catalogo, carrito):
    if len(carrito) == 0:
        print(MENSAJE_CARRITO_VACIO)
        return
    lineas = carrito_a_lineas(catalogo, carrito)
    print(SEPARADOR_CARRITO)
    print(f"{'ID':<{ANCHO_ID}}{'Producto':<{ANCHO_CARRITO_NOMBRE}}"
          f"{'Cantidad':>{ANCHO_CARRITO_CANTIDAD}}{'Precio (€)':>{ANCHO_CARRITO_PRECIO}}"
          f"{'Subtotal (€)':>{ANCHO_CARRITO_SUBTOTAL}}")
    print(SEPARADOR_CARRITO)
    for id_producto, cantidad, precio_unitario in lineas:
        nombre = buscar_producto(catalogo, id_producto)["nombre"]
        subtotal_linea = cantidad * precio_unitario
        print(f"{id_producto:<{ANCHO_ID}}{nombre:<{ANCHO_CARRITO_NOMBRE}}"
              f"{cantidad:>{ANCHO_CARRITO_CANTIDAD}}{precio_unitario:>{ANCHO_CARRITO_PRECIO}.2f}"
              f"{subtotal_linea:>{ANCHO_CARRITO_SUBTOTAL}.2f}")
    print(SEPARADOR_CARRITO)
    subtotal = calcular_subtotal(lineas)
    envio = calcular_envio(subtotal)
    total = calcular_total(lineas)
    print(f"{'Subtotal (€)':>{ANCHO_ETIQUETA_RESUMEN}}{subtotal:>{ANCHO_CARRITO_SUBTOTAL}.2f}")
    print(f"{'Envío (€)':>{ANCHO_ETIQUETA_RESUMEN}}{envio:>{ANCHO_CARRITO_SUBTOTAL}.2f}")
    print(f"{'Total (€)':>{ANCHO_ETIQUETA_RESUMEN}}{total:>{ANCHO_CARRITO_SUBTOTAL}.2f}")


def mostrar_ticket(catalogo, pedido):
    print(SEPARADOR_CARRITO)
    print(f"Pedido:    {pedido['id_pedido']}")
    print(f"Cliente:   {pedido['cliente']}")
    print(f"Dirección: {pedido['direccion']}")
    print(SEPARADOR_CARRITO)
    print(f"{'ID':<{ANCHO_ID}}{'Producto':<{ANCHO_CARRITO_NOMBRE}}"
          f"{'Cantidad':>{ANCHO_CARRITO_CANTIDAD}}{'Precio (€)':>{ANCHO_CARRITO_PRECIO}}"
          f"{'Subtotal (€)':>{ANCHO_CARRITO_SUBTOTAL}}")
    print(SEPARADOR_CARRITO)
    for id_producto, cantidad, precio_unitario in pedido["lineas"]:
        nombre = buscar_producto(catalogo, id_producto)["nombre"]
        print(f"{id_producto:<{ANCHO_ID}}{nombre:<{ANCHO_CARRITO_NOMBRE}}"
              f"{cantidad:>{ANCHO_CARRITO_CANTIDAD}}{precio_unitario:>{ANCHO_CARRITO_PRECIO}.2f}"
              f"{cantidad * precio_unitario:>{ANCHO_CARRITO_SUBTOTAL}.2f}")
    print(SEPARADOR_CARRITO)
    print(f"{'Total (€)':>{ANCHO_ETIQUETA_RESUMEN}}{pedido['total_eur']:>{ANCHO_CARRITO_SUBTOTAL}.2f}")
    print(f"Estado: {pedido['estado']}")


def confirmar_pedido(catalogo, carrito, pedidos):
    if len(carrito) == 0:
        print(MENSAJE_CARRITO_VACIO)
        return carrito, pedidos
    cliente = pedir_texto_no_vacio("Nombre del cliente: ")
    direccion = pedir_texto_no_vacio("Dirección de entrega: ")
    lineas = carrito_a_lineas(catalogo, carrito)
    pedido = crear_pedido(generar_id_pedido(pedidos), cliente, direccion,
                          lineas, ESTADO_INICIAL)
    nuevos_pedidos = []
    for existente in pedidos:
        nuevos_pedidos.append(existente)
    nuevos_pedidos.append(pedido)
    print(MENSAJE_PEDIDO_CONFIRMADO)
    mostrar_ticket(catalogo, pedido)
    return crear_carrito_vacio(), nuevos_pedidos


def filtrar_pedidos_por_cliente(pedidos, nombre):
    encontrados = []
    for pedido in pedidos:
        if pedido["cliente"].lower() == nombre.lower():
            encontrados.append(pedido)
    return encontrados


def ver_mis_pedidos(pedidos):
    nombre = pedir_texto_no_vacio("Nombre del cliente: ")
    encontrados = filtrar_pedidos_por_cliente(pedidos, nombre)
    if len(encontrados) == 0:
        print(MENSAJE_SIN_PEDIDOS_CLIENTE)
        return
    print(SEPARADOR_MIS_PEDIDOS)
    print(f"{'Pedido':<{ANCHO_MIS_PEDIDOS_ID}}{'Total (€)':>{ANCHO_MIS_PEDIDOS_TOTAL}}"
          f"{'Estado':>{ANCHO_MIS_PEDIDOS_ESTADO}}")
    print(SEPARADOR_MIS_PEDIDOS)
    for pedido in encontrados:
        print(f"{pedido['id_pedido']:<{ANCHO_MIS_PEDIDOS_ID}}"
              f"{pedido['total_eur']:>{ANCHO_MIS_PEDIDOS_TOTAL}.2f}"
              f"{pedido['estado']:>{ANCHO_MIS_PEDIDOS_ESTADO}}")
    print(SEPARADOR_MIS_PEDIDOS)


def menu_cliente(catalogo, carrito, pedidos):
    salir = False
    while not salir:
        print(MENU_CLIENTE)
        opcion = pedir_entero("Elige una opción: ", OPCION_VOLVER, OPCION_MAXIMA)
        if opcion == OPCION_VER_CATALOGO:
            ver_catalogo(catalogo)
        elif opcion == OPCION_ANADIR_CARRITO:
            carrito = anadir_al_carrito(catalogo, carrito)
        elif opcion == OPCION_QUITAR_CARRITO:
            carrito = quitar_del_carrito(catalogo, carrito)
        elif opcion == OPCION_VER_CARRITO:
            mostrar_carrito(catalogo, carrito)
        elif opcion == OPCION_CONFIRMAR_PEDIDO:
            carrito, pedidos = confirmar_pedido(catalogo, carrito, pedidos)
        elif opcion == OPCION_VER_MIS_PEDIDOS:
            ver_mis_pedidos(pedidos)
        else:
            salir = True
    return carrito, pedidos