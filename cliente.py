from datos import CATEGORIAS
from validaciones import pedir_entero, pedir_opcion

OPCION_VOLVER = 0
OPCION_VER_CATALOGO = 1
OPCION_MAXIMA = 6

FILTRO_TODO = "todo"
FILTRO_RESTAURANTE = "restaurante"
FILTRO_CATEGORIA = "categoria"
FILTROS_CATALOGO = (FILTRO_TODO, FILTRO_RESTAURANTE, FILTRO_CATEGORIA)

TEXTO_DISPONIBLE = "Sí"
TEXTO_NO_DISPONIBLE = "No"
MENSAJE_PROXIMAMENTE = "Próximamente."
MENSAJE_CATALOGO_VACIO = "No hay productos con ese criterio."

ANCHO_ID = 6
ANCHO_NOMBRE = 30
ANCHO_RESTAURANTE = 16
ANCHO_CATEGORIA = 14
ANCHO_PRECIO = 11
ANCHO_DISPONIBLE = 13
ANCHO_LINEA = (ANCHO_ID + ANCHO_NOMBRE + ANCHO_RESTAURANTE + ANCHO_CATEGORIA
               + ANCHO_PRECIO + ANCHO_DISPONIBLE)
SEPARADOR = "-" * ANCHO_LINEA

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


def menu_cliente(catalogo):
    salir = False
    while not salir:
        print(MENU_CLIENTE)
        opcion = pedir_entero("Elige una opción: ", OPCION_VOLVER, OPCION_MAXIMA)
        if opcion == OPCION_VER_CATALOGO:
            ver_catalogo(catalogo)
        elif opcion == OPCION_VOLVER:
            salir = True
        else:
            print(MENSAJE_PROXIMAMENTE)