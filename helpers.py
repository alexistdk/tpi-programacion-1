"""Módulo helpers.py — funciones genéricas de validación y utilidades."""

import unicodedata


def sin_tildes(texto):
    """Devuelve el texto en minúsculas y sin tildes, para comparar alfabéticamente."""
    texto = unicodedata.normalize("NFKD", texto)
    return texto.encode("ascii", "ignore").decode().lower()


def pedir_texto(mensaje):
    """Pide un texto al usuario y reintenta hasta que no sea vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Error: el valor no puede estar vacío. Intentá de nuevo.")


def pedir_texto_sin_coma(mensaje):
    """Pide un texto no vacío y sin comas (una coma rompería el formato del CSV)."""
    while True:
        texto = pedir_texto(mensaje)
        if "," not in texto:
            return texto
        print("Error: el valor no puede contener comas (,). Intentá de nuevo.")


def pedir_opcion(mensaje, minimo, maximo):
    """Pide un número de opción y reintenta hasta que sea un entero dentro del rango."""
    while True:
        try:
            opcion = int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero")
            continue
        if minimo <= opcion <= maximo:
            return opcion
        print(f"Error: la opción debe estar entre {minimo} y {maximo}")


def pedir_entero_positivo(mensaje):
    """Pide un número al usuario y reintenta hasta que sea un entero mayor a cero."""
    while True:
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)
        except ValueError:
            print("Error: debe ser un número entero. Intentá de nuevo.")
            continue
        if numero > 0:
            return numero
        print("Error: debe ser un entero mayor a cero. Intentá de nuevo.")
