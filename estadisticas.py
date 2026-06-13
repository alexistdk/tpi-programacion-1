"""Módulo estadisticas.py — máximos/mínimos, promedios y conteo por continente."""

from helpers import sin_tildes
from operaciones import obtener_poblacion


def promedio(paises, campo):
    """Calcula el promedio del campo indicado sobre todos los países."""
    suma = 0
    for pais in paises:
        suma = suma + pais[campo]
    return suma / len(paises)


def contar_por_continente(paises):
    """Devuelve un diccionario contador: continente -> cantidad de países."""
    conteo = {}
    for pais in paises:
        continente = pais["continente"]
        conteo[continente] = conteo.get(continente, 0) + 1
    return conteo


def mostrar_estadisticas(paises):
    """Calcula y muestra todas las estadísticas del dataset."""
    if len(paises) == 0:
        print("No hay países cargados para calcular estadísticas.")
        return
    mayor = max(paises, key=obtener_poblacion)
    menor = min(paises, key=obtener_poblacion)
    print("\n--- ESTADÍSTICAS ---")
    print(f"País con mayor población: {mayor['nombre']} ({mayor['poblacion']:,} habitantes)")
    print(f"País con menor población: {menor['nombre']} ({menor['poblacion']:,} habitantes)")
    print(f"Promedio de población:  {promedio(paises, 'poblacion'):,.0f} habitantes")
    print(f"Promedio de superficie: {promedio(paises, 'superficie'):,.0f} km²")
    print("Cantidad de países por continente:")
    conteo = contar_por_continente(paises)
    for continente in sorted(conteo, key=sin_tildes):
        print(f"  {continente}: {conteo[continente]}")
