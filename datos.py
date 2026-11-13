CATEGORIAS = {"pizza", "hamburguesa", "postre", "bebida"}
ESTADOS = ("recibido", "en_preparacion", "en_reparto", "entregado", "cancelado")
ENVIO_EUR = 2.50
ENVIO_GRATIS_DESDE_EUR = 25.00
DECIMALES = 2

CATALOGO = [
    {"id_producto": "P01", "nombre": "Pizza Margarita", "restaurante": "Napoli Pizza",
     "categoria": "pizza", "precio_eur": 8.50, "disponible": True},
    {"id_producto": "P02", "nombre": "Pizza Pepperoni", "restaurante": "Napoli Pizza",
     "categoria": "pizza", "precio_eur": 10.00, "disponible": True},
    {"id_producto": "P03", "nombre": "Pizza Cuatro Quesos", "restaurante": "Napoli Pizza",
     "categoria": "pizza", "precio_eur": 11.50, "disponible": False},
    {"id_producto": "P04", "nombre": "Pizza Barbacoa", "restaurante": "Napoli Pizza",
     "categoria": "pizza", "precio_eur": 11.00, "disponible": True},
    {"id_producto": "P05", "nombre": "Tiramisú", "restaurante": "Napoli Pizza",
     "categoria": "postre", "precio_eur": 4.50, "disponible": True},
    {"id_producto": "P06", "nombre": "Agua mineral 50cl", "restaurante": "Napoli Pizza",
     "categoria": "bebida", "precio_eur": 1.50, "disponible": True},
    {"id_producto": "P07", "nombre": "Hamburguesa Clásica", "restaurante": "Burger Calima",
     "categoria": "hamburguesa", "precio_eur": 7.50, "disponible": True},
    {"id_producto": "P08", "nombre": "Hamburguesa Doble Queso", "restaurante": "Burger Calima",
     "categoria": "hamburguesa", "precio_eur": 9.50, "disponible": True},
    {"id_producto": "P09", "nombre": "Hamburguesa Vegana", "restaurante": "Burger Calima",
     "categoria": "hamburguesa", "precio_eur": 9.00, "disponible": False},
    {"id_producto": "P10", "nombre": "Hamburguesa Pollo Crujiente", "restaurante": "Burger Calima",
     "categoria": "hamburguesa", "precio_eur": 8.50, "disponible": True},
    {"id_producto": "P11", "nombre": "Cola 33cl", "restaurante": "Burger Calima",
     "categoria": "bebida", "precio_eur": 2.00, "disponible": True},
    {"id_producto": "P12", "nombre": "Brownie con helado", "restaurante": "Burger Calima",
     "categoria": "postre", "precio_eur": 4.00, "disponible": True},
    {"id_producto": "P13", "nombre": "Tarta de queso", "restaurante": "Dulce Isla",
     "categoria": "postre", "precio_eur": 4.50, "disponible": True},
    {"id_producto": "P14", "nombre": "Helado de vainilla", "restaurante": "Dulce Isla",
     "categoria": "postre", "precio_eur": 3.50, "disponible": True},
    {"id_producto": "P15", "nombre": "Limonada natural", "restaurante": "Dulce Isla",
     "categoria": "bebida", "precio_eur": 2.50, "disponible": True},
    {"id_producto": "P16", "nombre": "Batido de fresa", "restaurante": "Dulce Isla",
     "categoria": "bebida", "precio_eur": 3.00, "disponible": False},
]


def buscar_producto(catalogo, id_producto):
    for producto in catalogo:
        if producto["id_producto"] == id_producto:
            return producto
    return None


def crear_linea(catalogo, id_producto, cantidad):
    producto = buscar_producto(catalogo, id_producto)
    return (id_producto, cantidad, producto["precio_eur"])


def crear_carrito_vacio():
    return {}


def carrito_a_lineas(catalogo, carrito):
    lineas = []
    for id_producto in carrito:
        lineas.append(crear_linea(catalogo, id_producto, carrito[id_producto]))
    return lineas

def calcular_subtotal(lineas):
    subtotal = 0
    for id_producto, cantidad, precio_unitario in lineas:
        subtotal = subtotal + cantidad * precio_unitario
    return round(subtotal, DECIMALES)


def calcular_envio(subtotal):
    if subtotal >= ENVIO_GRATIS_DESDE_EUR:
        return 0
    return ENVIO_EUR


def calcular_total(lineas):
    subtotal = calcular_subtotal(lineas)
    return round(subtotal + calcular_envio(subtotal), DECIMALES)


def crear_pedido(id_pedido, cliente, direccion, lineas, estado):
    return {
        "id_pedido": id_pedido,
        "cliente": cliente,
        "direccion": direccion,
        "lineas": lineas,
        "estado": estado,
        "total_eur": calcular_total(lineas),
    }


def crear_pedidos_iniciales(catalogo):
    pedidos = []
    pedidos.append(crear_pedido(
        "PED-001", "Lucía Fernández", "Calle Alcalá 45, Madrid",
        [crear_linea(catalogo, "P01", 2), crear_linea(catalogo, "P11", 2)],
        "entregado"))
    pedidos.append(crear_pedido(
        "PED-002", "Marcos Ruiz", "Avenida de América 12, Madrid",
        [crear_linea(catalogo, "P08", 2), crear_linea(catalogo, "P10", 1),
         crear_linea(catalogo, "P11", 3)],
        "en_reparto"))
    pedidos.append(crear_pedido(
        "PED-003", "Carmen Soto", "Calle Toledo 7, Madrid",
        [crear_linea(catalogo, "P02", 1), crear_linea(catalogo, "P06", 1)],
        "en_preparacion"))
    pedidos.append(crear_pedido(
        "PED-004", "Javier Morales", "Calle Atocha 101, Madrid",
        [crear_linea(catalogo, "P07", 1), crear_linea(catalogo, "P12", 1)],
        "recibido"))
    pedidos.append(crear_pedido(
        "PED-005", "Elena Vidal", "Paseo del Prado 3, Madrid",
        [crear_linea(catalogo, "P04", 1), crear_linea(catalogo, "P15", 1)],
        "cancelado"))
    return pedidos


PEDIDOS = crear_pedidos_iniciales(CATALOGO)