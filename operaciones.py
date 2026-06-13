"""Módulo operaciones.py — agregar, actualizar, buscar, filtrar y ordenar países."""

from helpers import sin_tildes, pedir_texto, pedir_texto_sin_coma, pedir_opcion, pedir_entero_positivo
from archivo import guardar_paises, RUTA_CSV


def buscar_pais_exacto(paises, nombre):
    """Devuelve el país cuyo nombre coincide exactamente (sin distinguir mayúsculas), o None."""
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            return pais
    return None


def buscar_paises(paises, texto):
    """Devuelve los países cuyo nombre contiene el texto (sin distinguir mayúsculas)."""
    encontrados = []
    for pais in paises:
        if texto.lower() in pais["nombre"].lower():
            encontrados.append(pais)
    return encontrados


def validar_nombre(paises, nombre):
    """Valida que el nombre no esté vacío ni repetido. Lanza ValueError si no cumple."""
    if nombre == "":
        raise ValueError("el nombre no puede estar vacío")
    if "," in nombre:
        raise ValueError("el nombre no puede contener comas (,)")
    if buscar_pais_exacto(paises, nombre) is not None:
        raise ValueError(f"'{nombre}' ya existe en la lista, ingrese otro nombre")


def agregar_pais(paises):
    """Da de alta un nuevo país pidiendo y validando sus datos."""
    while True:
        try:
            nombre = input("Nombre del país: ").strip()
            validar_nombre(paises, nombre)
            break
        except ValueError as e:
            print("Error:", e)
    poblacion = pedir_entero_positivo("Población: ")
    superficie = pedir_entero_positivo("Superficie (km²): ")
    continente = pedir_texto_sin_coma("Continente: ")
    pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }
    paises.append(pais)
    guardar_paises(paises, RUTA_CSV)
    print(f"País '{nombre}' agregado con éxito.")


def actualizar_pais(paises):
    """Actualiza la población y la superficie de un país existente."""
    nombre = pedir_texto("Nombre del país a actualizar: ")
    pais = buscar_pais_exacto(paises, nombre)
    if pais is None:
        raise ValueError(f"no se encontró el país '{nombre}'")
    print(f"Datos actuales de {pais['nombre']}: "
          f"población {pais['poblacion']:,}, superficie {pais['superficie']:,} km².")
    pais["poblacion"] = pedir_entero_positivo("Nueva población: ")
    pais["superficie"] = pedir_entero_positivo("Nueva superficie (km²): ")
    guardar_paises(paises, RUTA_CSV)
    print(f"País '{pais['nombre']}' actualizado con éxito.")


def filtrar_por_continente(paises, continente):
    """Devuelve los países del continente indicado (sin distinguir mayúsculas)."""
    filtrados = []
    for pais in paises:
        if pais["continente"].lower() == continente.lower():
            filtrados.append(pais)
    return filtrados


def filtrar_por_rango(paises, campo, minimo, maximo):
    """Devuelve los países cuyo campo está dentro del rango indicado."""
    filtrados = []
    for pais in paises:
        if minimo <= pais[campo] <= maximo:
            filtrados.append(pais)
    return filtrados


def obtener_nombre(pais):
    """Devuelve el nombre del país preparado para ordenar alfabéticamente."""
    return sin_tildes(pais["nombre"])


def obtener_poblacion(pais):
    """Devuelve la población del país."""
    return pais["poblacion"]


def obtener_superficie(pais):
    """Devuelve la superficie del país."""
    return pais["superficie"]


def ordenar_paises(paises, clave, descendente):
    """Devuelve una lista nueva ordenada según la función clave indicada."""
    return sorted(paises, key=clave, reverse=descendente)


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


def menu_buscar(paises):
    """Pide un texto y muestra los países que coinciden."""
    texto = pedir_texto("Nombre (o parte del nombre) a buscar: ")
    encontrados = buscar_paises(paises, texto)
    if len(encontrados) == 0:
        print(f"No se encontraron países que contengan '{texto}'.")
    else:
        mostrar_paises(encontrados)


def menu_filtrar(paises):
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


def menu_ordenar(paises):
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
