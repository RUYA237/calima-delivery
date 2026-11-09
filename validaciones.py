SEPARADOR_OPCIONES = ", "


def unir_opciones(opciones):
    texto = ""
    for opcion in opciones:
        if texto == "":
            texto = opcion
        else:
            texto = texto + SEPARADOR_OPCIONES + opcion
    return texto


def pedir_entero(mensaje, minimo=None, maximo=None):
    while True:
        texto = input(mensaje)
        try:
            numero = int(texto)
            if minimo is not None and numero < minimo:
                print(f"Error: el número debe ser como mínimo {minimo}.")
            elif maximo is not None and numero > maximo:
                print(f"Error: el número debe ser como máximo {maximo}.")
            else:
                return numero
        except ValueError:
            print("Error: debes escribir un número entero (sin letras ni decimales).")


def pedir_texto_no_vacio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Error: el texto no puede estar vacío.")


def pedir_opcion(mensaje, opciones):
    while True:
        texto = input(f"{mensaje} [{unir_opciones(opciones)}]: ").strip().lower()
        for opcion in opciones:
            if opcion.lower() == texto:
                return opcion
        print(f"Error: opción no válida. Elige una de: {unir_opciones(opciones)}.")