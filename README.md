# CALIMA DELIVERY

Programa de consola en Python que simula una aplicación de reparto de comida a domicilio. Tiene dos modos: **cliente** (consultar el catálogo, preparar un carrito, confirmar pedidos y ver los suyos) y **empresa** (listar pedidos, ver su detalle, cambiar su estado y consultar estadísticas). Los datos de partida (16 productos, 3 restaurantes y 5 pedidos) están cargados en el propio programa y el total de cada pedido se calcula a partir de ellos.

**Grupo:** XX (pendiente de completar)

**Integrantes:**

- Olivas Lopez Arian
- López Campos Alvaro
- Yagüe Hidalgo Raúl

## Requisitos

- Python 3.6 o superior (el programa usa f-strings).
- No hay dependencias externas: solo se usa la biblioteca estándar. No hay que instalar nada.

Para comprobar la versión instalada:

```bash
python3 --version
```

## Cómo ejecutarlo

1. Descomprime el archivo y abre una terminal dentro de la carpeta del proyecto (la que contiene `main.py`).
2. Ejecuta:

```bash
python3 main.py
```

En Windows se usa `python main.py`.

El programa se maneja escribiendo el número de la opción y pulsando Intro. Si se escribe algo no válido (letras, un número fuera de rango, una opción que no existe), muestra un mensaje de error y repite la pregunta.

## Opciones de los menús

### Menú principal

| Opción | Qué hace |
|---|---|
| 1 | Entra en el modo cliente |
| 2 | Entra en el modo empresa |
| 0 | Sale del programa |

### Modo cliente

| Opción | Qué hace |
|---|---|
| 1. Ver catálogo | Pregunta si se quiere ver `todo`, filtrar por `restaurante` o por `categoria`, y muestra una tabla con identificador, producto, restaurante, categoría, precio y disponibilidad |
| 2. Añadir producto al carrito | Pide el id y la cantidad y lo añade (suma si ya estaba). Solo admite productos que existen y están disponibles. Escribiendo `0` se cancela |
| 3. Quitar producto del carrito | Pide el id y quita ese producto entero del carrito |
| 4. Ver carrito | Muestra las líneas, subtotal, envío y total |
| 5. Confirmar pedido | Pide nombre y dirección, crea el pedido con estado `recibido`, muestra el ticket y vacía el carrito |
| 6. Ver mis pedidos | Pide el nombre del cliente y muestra sus pedidos |
| 0. Volver al menú principal | Vuelve al menú anterior |

Al filtrar, el texto se puede escribir con mayúsculas o minúsculas (`POSTRE` equivale a `postre`). El carrito se conserva si se cambia al modo empresa y se vuelve.

### Modo empresa

| Opción | Qué hace |
|---|---|
| 1. Listar pedidos | Pregunta si se quieren ver `todos` los pedidos o filtrar por `estado`, y muestra una tabla con pedido, cliente, total y estado |
| 2. Ver detalle de un pedido | Pide el id del pedido (por ejemplo `PED-004`) y muestra cliente, dirección, ciudad, líneas, total y estado |
| 3. Cambiar estado de un pedido | Pide el id y la acción: `avanzar` pasa al siguiente estado y `cancelar` cancela el pedido (solo si está en `recibido`) |
| 4. Ver estadísticas | Muestra pedidos por estado, ingresos, ticket medio y producto más vendido |
| 0. Volver al menú principal | Vuelve al menú anterior |

Los estados posibles son: `recibido`, `en_preparacion`, `en_reparto`, `entregado` y `cancelado`. La secuencia al avanzar es `recibido` → `en_preparacion` → `en_reparto` → `entregado`.

## Estructura de ficheros

```
calima_delivery/
├── main.py
├── datos.py
├── validaciones.py
├── cliente.py
├── empresa.py
├── README.md
└── docs/
    └── memoria.pdf
```

| Fichero | Responsabilidad |
|---|---|
| `main.py` | Programa principal: crea el carrito vacío, muestra el menú de roles y lanza el modo elegido. Pasa los datos a cada modo por parámetro y guarda lo que devuelven (carrito y pedidos). |
| `datos.py` | **Aquí se definen los datos de partida y las constantes**: categorías, estados, envío, `CATALOGO` (16 productos) y `PEDIDOS` (5 pedidos). Incluye las funciones de carrito, identificadores de pedido y cálculo de subtotal, envío y total. |
| `validaciones.py` | Funciones para pedir datos por teclado con control de errores: número entero en un rango, texto no vacío y opción de una lista. |
| `cliente.py` | Modo cliente: menú, catálogo, carrito, confirmar pedido y ver mis pedidos. |
| `empresa.py` | Modo empresa: menú, listar pedidos, detalle, cambio de estado y estadísticas. |
| `docs/memoria.pdf` | Memoria del proyecto. |

## Supuestos adoptados

- Los datos viven solo en memoria: no se leen ni se guardan ficheros, así que al cerrar el programa vuelve a empezar con los datos de partida.
- Los pedidos precargados usan identificadores y precios del catálogo; el total de cada pedido se calcula (subtotal más envío), no está escrito a mano.
- El envío cuesta 2,50 € y es gratis cuando el subtotal llega a 25,00 €.
- Hay un pedido precargado por cada estado posible.
- Algunos productos del catálogo aparecen como no disponibles (`No` en la columna Disponible) a propósito.
- Al añadir un producto no hay tope de cantidad; solo se exige un mínimo de 1. Escribir `0` cancela la operación.
- Los pedidos nuevos reciben identificadores correlativos a partir de `PED-006`.
- «Ver mis pedidos» no distingue mayúsculas de minúsculas (`ana` encuentra `Ana`), pero sí distingue tildes.
- Un pedido solo se puede cancelar si está en `recibido`. Un pedido `entregado` o `cancelado` no cambia más.
- Los pedidos cancelados no cuentan en los ingresos, el ticket medio ni el producto más vendido. Las estadísticas lo indican en pantalla.
- Si hay empate en el producto más vendido, se muestra el primero que aparece.

## Limitaciones conocidas

- Si se cierra la entrada con Ctrl+D (fin de entrada) o se interrumpe con Ctrl+C, el programa termina con un error de Python en lugar de un mensaje. Las entradas escritas normalmente (letras, números, vacíos) sí están controladas.
- No se guardan datos entre ejecuciones: los pedidos nuevos y los cambios de estado se pierden al salir.