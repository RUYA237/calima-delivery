# CALIMA DELIVERY

Programa de consola en Python que simula una aplicación de reparto de comida a domicilio. Tiene dos modos: **cliente** (consultar el catálogo de productos de varios restaurantes) y **empresa** (consultar los pedidos y filtrarlos por estado). Los datos de partida (16 productos, 3 restaurantes y 5 pedidos) están cargados en el propio programa y todo el total de cada pedido se calcula a partir de ellos.


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

| Opción | Qué hace | Estado |
|---|---|---|
| 1. Ver catálogo | Pregunta si se quiere ver `todo`, filtrar por `restaurante` o por `categoria`, y muestra una tabla con identificador, producto, restaurante, categoría, precio y disponibilidad | Implementada |
| 2. Añadir producto al carrito | Pide el id y la cantidad y lo añade (suma si ya estaba) | Implementada |
| 3. Quitar producto del carrito | Pide el id y quita ese producto entero del carrito | Implementada |
| 4. Ver carrito | Muestra las líneas, subtotal, envío y total | Implementada |
| 5. Confirmar pedido | Mostrará «Próximamente.» | Sprints siguientes |
| 6. Ver mis pedidos | Mostrará «Próximamente.» | Sprints siguientes |
| 0. Volver al menú principal | Vuelve al menú anterior | Implementada |

Al filtrar, el texto se puede escribir con mayúsculas o minúsculas (`POSTRE` equivale a `postre`).

### Modo empresa

| Opción | Qué hace | Estado |
|---|---|---|
| 1. Listar pedidos | Pregunta si se quieren ver `todos` los pedidos o filtrar por `estado`, y muestra una tabla con pedido, cliente, total y estado | Implementada |
| 2. Ver detalle de un pedido | Mostrará «Próximamente.» | Sprints siguientes |
| 3. Cambiar estado de un pedido | Mostrará «Próximamente.» | Sprints siguientes |
| 4. Ver estadísticas | Mostrará «Próximamente.» | Sprints siguientes |
| 0. Volver al menú principal | Vuelve al menú anterior | Implementada |

Los estados posibles son: `recibido`, `en_preparacion`, `en_reparto`, `entregado` y `cancelado`.

## Estructura de ficheros

```
calima_delivery/
├── main.py
├── datos.py
├── validaciones.py
├── cliente.py
├── empresa.py
├── README.md
```

| Fichero | Responsabilidad |
|---|---|
| `main.py` | Programa principal: muestra el menú de roles y lanza el modo elegido. Pasa `CATALOGO` y `PEDIDOS` a cada modo por parámetro. |
| `datos.py` | **Aquí se definen los datos de partida y las constantes**: categorías, estados, envío, `CATALOGO` (16 productos) y `PEDIDOS` (5 pedidos). Incluye las funciones que calculan subtotal, envío y total. |
| `validaciones.py` | Funciones para pedir datos por teclado con control de errores: número entero en un rango, texto no vacío y opción de una lista. |
| `cliente.py` | Modo cliente: menú y «Ver catálogo» (filtrar y mostrar). |
| `empresa.py` | Modo empresa: menú y «Listar pedidos» (filtrar y mostrar). |
| `docs/memoria.pdf` | Memoria del proyecto. |

## Supuestos adoptados

- Los datos viven solo en memoria: no se leen ni se guardan ficheros, así que al cerrar el programa vuelve a empezar con los datos de partida.
- Los pedidos precargados usan identificadores y precios del catálogo; el total de cada pedido se calcula (subtotal más envío), no está escrito a mano.
- El envío cuesta 2,50 € y es gratis cuando el subtotal llega a 25,00 €.
- Hay un pedido precargado por cada estado posible.
- Algunos productos del catálogo aparecen como no disponibles (`No` en la columna Disponible) a propósito.

## Limitaciones conocidas

- En este Sprint 1 solo funcionan «Ver catálogo» y «Listar pedidos»; el resto de opciones de los menús muestran «Próximamente.».
- Si se cierra la entrada con Ctrl+D (fin de entrada) o se interrumpe con Ctrl+C, el programa termina con un error de Python en lugar de un mensaje. Las entradas escritas normalmente (letras, números, vacíos) sí están controladas.
- No se guardan datos entre ejecuciones.