"""Módulo estadisticas.py — ordenamientos, estadísticas, visualización y submenús."""

import unicodedata


def sin_tildes(texto):
    """Devuelve el texto en minúsculas y sin tildes, para comparar alfabéticamente."""
    texto = unicodedata.normalize("NFKD", texto)
    return texto.encode("ascii", "ignore").decode().lower()


def obtener_nombre(pais):
    """Devuelve el nombre del país preparado para ordenar alfabéticamente."""
    return sin_tildes(pais["nombre"])


def obtener_poblacion(pais):
    """Devuelve la población del país."""
    return pais["poblacion"]


def obtener_superficie(pais):
    """Devuelve la superficie del país."""
    return pais["superficie"]


def mostrar_paises(paises):
    """Muestra la lista de países en una tabla alineada."""
    if len(paises) == 0:
        print("No hay países para mostrar.")
        return
    print()
    print(f"{'Nombre':<42}{'Población':>14}{'Superficie':>14}  Continente")
    print("-" * 90)
    for pais in paises:
        print(f"{pais['nombre']:<42}{pais['poblacion']:>14,}{pais['superficie']:>14,}  {pais['continente']}")
    print("-" * 90)
    print(f"Total: {len(paises)} países.")


def ordenar_paises(paises, clave, descendente):
    """Devuelve una lista nueva ordenada según la función clave indicada."""
    return sorted(paises, key=clave, reverse=descendente)


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


def menu_buscar(paises, buscar_paises, pedir_texto):
    """Pide un texto y muestra los países que coinciden."""
    texto = pedir_texto("Nombre (o parte del nombre) a buscar: ")
    encontrados = buscar_paises(paises, texto)
    if len(encontrados) == 0:
        print(f"No se encontraron países que contengan '{texto}'.")
    else:
        mostrar_paises(encontrados)


def menu_filtrar(paises, filtrar_por_continente, filtrar_por_rango, pedir_texto, pedir_opcion, pedir_entero_positivo):
    """Submenú de filtros: por continente o por rango de población/superficie."""
    print("\n--- FILTRAR PAÍSES ---")
    print("1. Por continente")
    print("2. Por rango de población")
    print("3. Por rango de superficie")
    opcion = pedir_opcion("Seleccione una opción: ", 1, 3)
    if opcion == 1:
        continente = pedir_texto("Continente: ")
        filtrados = filtrar_por_continente(paises, continente)
    else:
        if opcion == 2:
            campo = "poblacion"
        else:
            campo = "superficie"
        while True:
            minimo = pedir_entero_positivo("Valor mínimo: ")
            maximo = pedir_entero_positivo("Valor máximo: ")
            if minimo > maximo:
                print("Error: el mínimo no puede ser mayor que el máximo.")
            else:
                break
        filtrados = filtrar_por_rango(paises, campo, minimo, maximo)
    if len(filtrados) == 0:
        print("Ningún país cumple con el filtro.")
    else:
        mostrar_paises(filtrados)


def menu_ordenar(paises, pedir_opcion):
    """Submenú de ordenamiento: campo y sentido."""
    print("\n--- ORDENAR PAÍSES ---")
    print("1. Por nombre")
    print("2. Por población")
    print("3. Por superficie")
    opcion_campo = pedir_opcion("Seleccione una opción: ", 1, 3)
    if opcion_campo == 1:
        clave = obtener_nombre
    elif opcion_campo == 2:
        clave = obtener_poblacion
    else:
        clave = obtener_superficie
    print("1. Ascendente")
    print("2. Descendente")
    opcion_sentido = pedir_opcion("Seleccione el sentido: ", 1, 2)
    descendente = (opcion_sentido == 2)
    mostrar_paises(ordenar_paises(paises, clave, descendente))
