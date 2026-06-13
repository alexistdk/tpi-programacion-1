"""Módulo archivo.py — lectura/escritura del CSV y manejo de errores de formato."""

RUTA_CSV = "csv/paises.csv"
ENCABEZADO = "nombre,poblacion,superficie,continente"


def cargar_paises(ruta):
    """Lee el CSV y devuelve la lista de países como diccionarios.

    Las líneas con formato inválido se informan y se omiten.
    Si el archivo no existe devuelve None.
    """
    try:
        archivo = open(ruta, encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ruta}'.")
        print("Verificá que exista y que el programa se ejecute desde la raíz del proyecto.")
        return None

    paises = []
    with archivo:
        archivo.readline()
        numero_linea = 1
        for linea in archivo:
            numero_linea = numero_linea + 1
            linea = linea.strip()
            if linea == "":
                continue
            campos = linea.split(",")
            if len(campos) != 4 or "" in campos:
                print(f"Aviso: línea {numero_linea} con formato inválido, se omite: {linea}")
                continue
            try:
                pais = {
                    "nombre": campos[0],
                    "poblacion": int(campos[1]),
                    "superficie": int(campos[2]),
                    "continente": campos[3],
                }
            except ValueError:
                print(f"Aviso: línea {numero_linea} con números inválidos, se omite: {linea}")
                continue
            paises.append(pais)
    return paises


def guardar_paises(paises, ruta):
    """Reescribe el archivo CSV completo con la lista de países."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(ENCABEZADO + "\n")
        for pais in paises:
            linea = f"{pais['nombre']},{pais['poblacion']},{pais['superficie']},{pais['continente']}"
            archivo.write(linea + "\n")
