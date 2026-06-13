"""Módulo datos.py — lectura/escritura del CSV y operaciones sobre países."""
 
from helpers import pedir_texto, pedir_opcion, pedir_entero_positivo
 
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
        from estadisticas import mostrar_paises
        mostrar_paises(filtrados)
 
