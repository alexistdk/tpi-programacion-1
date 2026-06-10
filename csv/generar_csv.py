"""Genera paises.csv a partir de la API pública restcountries.com.

Descarga nombre, población, superficie y continente de todos los países
y los guarda en el formato que usa el programa:

    nombre,poblacion,superficie,continente

Uso: python3 generar_csv.py
"""

import csv
import json
import unicodedata
import urllib.request

URL = "https://restcountries.com/v3.1/all?fields=name,translations,population,area,continents"

CONTINENTES = {
    "Africa": "África",
    "Antarctica": "Antártida",
    "Asia": "Asia",
    "Europe": "Europa",
    "North America": "América del Norte",
    "Oceania": "Oceanía",
    "South America": "América del Sur",
}


def descargar_datos():
    """Descarga el JSON de la API y lo devuelve como lista de diccionarios."""
    with urllib.request.urlopen(URL) as respuesta:
        return json.load(respuesta)


def convertir(datos):
    """Convierte el JSON de la API al formato de la consigna.

    Excluye los registros con datos incompletos (población o superficie
    en cero) porque el programa no admite campos vacíos.
    """
    filas = []
    excluidos = []
    for pais in datos:
        # nombre en español cuando existe traducción, si no el nombre común
        nombre = pais.get("translations", {}).get("spa", {}).get("common") or pais["name"]["common"]
        # sin comas en los nombres para que el CSV se pueda parsear con split(",")
        nombre = nombre.replace(",", "")
        poblacion = pais.get("population")
        superficie = pais.get("area")
        continentes = pais.get("continents") or []
        if not nombre or not poblacion or not superficie or superficie <= 0 or not continentes:
            excluidos.append(nombre)
            continue
        filas.append({
            "nombre": nombre,
            "poblacion": int(poblacion),
            "superficie": int(round(superficie)),
            # si un país figura en dos continentes se toma el principal (el primero)
            "continente": CONTINENTES[continentes[0]],
        })
    return filas, excluidos


def clave_alfabetica(fila):
    """Clave de ordenamiento que ignora tildes ("África" no debe quedar al final)."""
    return unicodedata.normalize("NFKD", fila["nombre"]).encode("ascii", "ignore").decode()


def guardar_csv(filas, ruta="paises.csv"):
    """Escribe las filas ordenadas alfabéticamente en el archivo CSV."""
    filas.sort(key=clave_alfabetica)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"])
        escritor.writeheader()
        escritor.writerows(filas)


def main():
    print("Descargando datos de", URL)
    datos = descargar_datos()
    filas, excluidos = convertir(datos)
    guardar_csv(filas)
    print(f"Se escribieron {len(filas)} países en paises.csv")
    if excluidos:
        print(f"Se excluyeron {len(excluidos)} territorios con datos incompletos:")
        for nombre in excluidos:
            print("  -", nombre)


if __name__ == "__main__":
    main()
