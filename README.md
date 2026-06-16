# tpi-programacion-1

TPI Programación 1 — Gestión de Datos de Países en Python: filtros, ordenamientos y estadísticas

Tecnicatura Universitaria en Programación a Distancia — UTN

Materia: Programación 1

Integrantes: 
Alexis Delgado -  Comision 5
Felipe Villanueva - Comision 6


Descripción

Aplicación de consola desarrollada en Python que permite gestionar un dataset de países. Los datos se leen desde un archivo CSV y el sistema ofrece un menú interactivo con diversas funcionalidades.


Estructura del proyecto
```
tpi-programacion-1/
│
├── main.py              # Punto de entrada del programa
├── csv/
│   └── paises.csv       # Dataset base de países
├── generar_csv.py       # Script para regenerar el CSV desde la API restcountries.com
└── README.md
```

Instrucciones de uso

Requisitos:
-Python 3.x instalado.


Cómo ejecutar:
Cloná el repositorio o descargá los archivos.
Desde la raíz del proyecto, ejecutá:
```bash
python3 main.py
```
Es importante ejecutarlo desde la raíz del proyecto para que encuentre correctamente el archivo csv/paises.csv.




Funcionalidades del menú

Opciones:
1  Mostrar todos los países
2  Buscar país por nombre (coincidencia parcial)
3  Agregar un nuevo país
4  Actualizar población y superficie de un país
5  Filtrar por continente, rango de población o superficie
6  Ordenar por nombre, población o superficie (ascendente/descendente)
7  Ver estadísticas generales
8  Salir


Ejemplos de uso

Agregar un país

Seleccione una opción: 3
Nombre del país: Wakanda
Población: 1000000
Superficie (km²): 50000
Continente: África
País 'Wakanda' agregado con éxito.

Buscar un país

Seleccione una opción: 2
Nombre (o parte del nombre) a buscar: arg

Nombre                                      Población    Superficie  Continente
------------------------------------------------------------------------------------------
Argentina                                  45,376,763     2,780,400  América del Sur
------------------------------------------------------------------------------------------
Total: 1 países.

Filtrar por continente

Seleccione una opción: 5
1. Por continente
2. Por rango de población
3. Por rango de superficie
Seleccione una opción: 1
Continente: Europa
[lista de países europeos]

Ver estadísticas

Seleccione una opción: 7

--- ESTADÍSTICAS ---
País con mayor población: China (1,412,600,000 habitantes)
País con menor población: Ciudad del Vaticano (800 habitantes)
Promedio de población:  40,123,456 habitantes
Promedio de superficie: 612,345 km²
Cantidad de países por continente:
  África: 54
  América del Norte: 23
  ...


Validaciones implementadas:

No se permiten nombres vacíos ni con comas.
No se permiten países duplicados (comparación sin tildes ni mayúsculas).
Las cantidades deben ser enteros positivos.
El CSV se valida al cargar: las líneas con formato inválido se omiten con un aviso.
Los filtros de rango validan que el mínimo no sea mayor que el máximo.



Integrantes y Contribuciones:
Alexis Delgado - Desarrollo del programa principal (main.py), generación del CSV (generar_csv.py).
Felipe Villanueva - Documentación, modularización del código y colaboración en el desarrollo general.


Links
- Video demostrativo: https://drive.google.com/file/d/1NumcM9pPeOKU4j22mrxEzQ0c-1hzOZcE/view?usp=sharing
- PDF adjunto en el repositorio.
