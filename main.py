"""TPI Programación 1 — Gestión de Datos de Países en Python.

Aplicación de consola que gestiona un dataset de países (nombre, población,
superficie y continente) leído desde un archivo CSV, con menú interactivo:
alta, actualización, búsqueda, filtros, ordenamientos y estadísticas.

Uso: python3 main.py (desde la raíz del proyecto)
"""

import unicodedata

# ============================================================
# Constantes
# ============================================================

RUTA_CSV = "csv/paises.csv"
ENCABEZADO = "nombre,poblacion,superficie,continente"


# ============================================================
# Archivo: lectura y escritura del CSV
# ============================================================

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
        archivo.readline()  # se saltea la línea de encabezado
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


# ============================================================
# Entrada de datos con validación
# ============================================================

def pedir_texto(mensaje):
    """Pide un texto al usuario y reintenta hasta que no sea vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Error: el valor no puede estar vacío. Intentá de nuevo.")


def pedir_opcion(mensaje, minimo, maximo):
    """Pide un número de opción de menú y reintenta hasta que sea un entero
    dentro del rango [minimo, maximo]."""
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


# ============================================================
# Funciones auxiliares de criterio (usadas como key en
# sorted, max y min)
# ============================================================

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


# ============================================================
# Operaciones
# ============================================================

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


def buscar_paises(paises, texto):
    """Devuelve los países cuyo nombre contiene el texto (sin distinguir mayúsculas)."""
    encontrados = []
    for pais in paises:
        if texto.lower() in pais["nombre"].lower():
            encontrados.append(pais)
    return encontrados


def buscar_pais_exacto(paises, nombre):
    """Devuelve el país cuyo nombre coincide exactamente (sin distinguir mayúsculas), o None."""
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            return pais
    return None


def validar_nombre(paises, nombre):
    """Valida que el nombre no esté vacío ni repetido.
    Lanza ValueError con un mensaje descriptivo si no cumple."""
    if nombre == "":
        raise ValueError("el nombre no puede estar vacío")
    if buscar_pais_exacto(paises, nombre) is not None:
        raise ValueError(f"'{nombre}' ya existe en la lista, ingrese otro nombre")


def agregar_pais(paises):
    """Da de alta un nuevo país pidiendo y validando sus datos."""
    # subciclo: insistir hasta recibir un nombre válido (no vacío ni repetido)
    while True:
        try:
            nombre = input("Nombre del país: ").strip()
            validar_nombre(paises, nombre)
            break
        except ValueError as e:
            print("Error:", e)
    poblacion = pedir_entero_positivo("Población: ")
    superficie = pedir_entero_positivo("Superficie (km²): ")
    continente = pedir_texto("Continente: ")
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
        # el error lo atrapa el try/except del loop principal
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
    """Devuelve los países cuyo campo (poblacion o superficie) está dentro del rango."""
    filtrados = []
    for pais in paises:
        if minimo <= pais[campo] <= maximo:
            filtrados.append(pais)
    return filtrados


def ordenar_paises(paises, clave, descendente):
    """Devuelve una lista nueva ordenada según la función clave indicada."""
    return sorted(paises, key=clave, reverse=descendente)


# ============================================================
# Estadísticas
# ============================================================

def pais_mayor_poblacion(paises):
    """Devuelve el país con mayor población."""
    return max(paises, key=obtener_poblacion)


def pais_menor_poblacion(paises):
    """Devuelve el país con menor población."""
    return min(paises, key=obtener_poblacion)


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
    mayor = pais_mayor_poblacion(paises)
    menor = pais_menor_poblacion(paises)
    print("\n--- ESTADÍSTICAS ---")
    print(f"País con mayor población: {mayor['nombre']} ({mayor['poblacion']:,} habitantes)")
    print(f"País con menor población: {menor['nombre']} ({menor['poblacion']:,} habitantes)")
    print(f"Promedio de población:  {promedio(paises, 'poblacion'):,.0f} habitantes")
    print(f"Promedio de superficie: {promedio(paises, 'superficie'):,.0f} km²")
    print("Cantidad de países por continente:")
    conteo = contar_por_continente(paises)
    for continente in sorted(conteo, key=sin_tildes):
        print(f"  {continente}: {conteo[continente]}")


# ============================================================
# Menú y programa principal
# ============================================================

def mostrar_menu():
    """Imprime las opciones del menú principal."""
    print("\n--- GESTIÓN DE DATOS DE PAÍSES ---")
    print("1. Mostrar todos los países")
    print("2. Buscar país por nombre")
    print("3. Agregar país")
    print("4. Actualizar país")
    print("5. Filtrar países")
    print("6. Ordenar países")
    print("7. Estadísticas")
    print("8. Salir")


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
        # subciclo: insistir hasta que el rango sea coherente
        while True:
            try:
                minimo = pedir_entero_positivo("Valor mínimo: ")
                maximo = pedir_entero_positivo("Valor máximo: ")
                if minimo > maximo:
                    raise ValueError("el mínimo no puede ser mayor que el máximo")
                break
            except ValueError as e:
                print("Error:", e)
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


def main():
    """Carga el dataset y ejecuta el loop principal del menú."""
    paises = cargar_paises(RUTA_CSV)
    if paises is None:
        return
    print(f"Se cargaron {len(paises)} países desde '{RUTA_CSV}'.")

    opcion = 0
    while opcion != 8:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Error: debe ingresar un número entero")
            continue

        try:
            if opcion == 1:
                mostrar_paises(paises)
            elif opcion == 2:
                menu_buscar(paises)
            elif opcion == 3:
                agregar_pais(paises)
            elif opcion == 4:
                actualizar_pais(paises)
            elif opcion == 5:
                menu_filtrar(paises)
            elif opcion == 6:
                menu_ordenar(paises)
            elif opcion == 7:
                mostrar_estadisticas(paises)
            elif opcion == 8:
                print("Saliendo del programa...")
            else:
                print("Opción inválida. Elija un número del 1 al 8.")
        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
