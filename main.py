"""TPI Programación 1 — Gestión de Datos de Países en Python.
 
Punto de entrada del programa. Importa los módulos datos y estadisticas.
 
Uso: python3 main.py (desde la raíz del proyecto)
"""
 
from datos import cargar_paises, agregar_pais, actualizar_pais, menu_filtrar, RUTA_CSV
from estadisticas import mostrar_paises, mostrar_estadisticas, menu_buscar, menu_ordenar
 
 
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
 
 
paises = cargar_paises(RUTA_CSV)
if paises is None:
    exit()
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
 
