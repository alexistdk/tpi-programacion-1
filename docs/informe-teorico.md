# Informe teórico (borrador para el PDF)

**TPI Programación 1 — Gestión de Datos de Países en Python**

Este informe presenta los conceptos teóricos sobre los que se apoya la aplicación:
listas, diccionarios, funciones, condicionales, ordenamientos, estadísticas básicas
y archivos CSV.

## 1. Listas

Una lista es una estructura de datos **secuencial y mutable** que permite almacenar
una colección ordenada de elementos, no necesariamente del mismo tipo. Se accede a
sus elementos por índice (comenzando en 0) y su tamaño puede crecer o reducirse en
tiempo de ejecución mediante métodos como `append()`, `insert()` y `remove()`.

En este proyecto la lista es la estructura principal: el dataset completo de países
se carga en memoria como una lista, lo que permite recorrerla con `for` para mostrar,
buscar y filtrar registros, y agregarle elementos cuando el usuario da de alta un país.

```python
paises = []          # lista vacía
paises.append(pais)  # alta de un nuevo registro
```

## 2. Diccionarios

Un diccionario es una estructura que asocia **claves** con **valores**, permitiendo
recuperar un valor a partir de su clave en lugar de una posición numérica. Las claves
deben ser inmutables (típicamente cadenas) y únicas dentro del diccionario.

En el programa, cada país se representa como un diccionario con cuatro claves fijas:

```python
{"nombre": "Argentina", "poblacion": 46735004, "superficie": 2780400, "continente": "América del Sur"}
```

Esto hace que el código sea más legible que usar listas posicionales: escribir
`pais["poblacion"]` es autoexplicativo, mientras que `pais[1]` obliga a recordar
qué guarda cada posición. Los diccionarios también se usan como **contadores**
para las estadísticas (cantidad de países por continente), donde la clave es el
continente y el valor la cantidad acumulada.

## 3. Funciones

Una función es un bloque de código con nombre que encapsula una tarea y puede
recibir **parámetros** y devolver un **valor de retorno**. Las funciones permiten:

- **Modularizar**: dividir el problema en partes pequeñas y manejables
  (principio "una función = una responsabilidad").
- **Reutilizar**: la misma lógica (por ejemplo, validar un número entero positivo)
  se invoca desde varios puntos sin duplicar código.
- **Probar y mantener**: un error se corrige en un solo lugar.

El proyecto se organiza en módulos (`archivo.py`, `operaciones.py`, `estadisticas.py`)
donde cada función resuelve una única operación del menú.

## 4. Condicionales

Las estructuras condicionales (`if` / `elif` / `else`) permiten que el programa tome
decisiones según el estado de los datos o la entrada del usuario. En esta aplicación
se usan para:

- Ramificar el **menú principal** según la opción elegida.
- **Validar entradas**: rechazar campos vacíos, números no enteros o negativos.
- Controlar **casos límite**: búsquedas sin resultados, país inexistente al
  actualizar, archivo CSV con formato inválido.

Se complementan con los bucles `while` (repetir el menú hasta que el usuario elija
salir, reintentar una entrada inválida) y `for` (recorrer la lista de países).

## 5. Ordenamientos

Ordenar es reorganizar una colección según un criterio de comparación. Python ofrece
la función incorporada `sorted()`, que devuelve una **lista nueva** ordenada sin
modificar la original, y acepta dos parámetros clave:

- `key`: una función que extrae de cada elemento el valor por el cual ordenar.
- `reverse`: `True` para orden descendente.

```python
# países ordenados por población, de mayor a menor
sorted(paises, key=lambda p: p["poblacion"], reverse=True)
```

Internamente `sorted()` implementa el algoritmo **Timsort** (híbrido de merge sort
e insertion sort), con complejidad O(n log n) en el peor caso. Para este trabajo se
ordena por nombre (alfabético), población y superficie, en forma ascendente o
descendente según elija el usuario.

## 6. Estadísticas básicas

Sobre la lista de países se calculan medidas descriptivas simples:

- **Máximo y mínimo**: país con mayor/menor población, usando `max()` y `min()`
  con el parámetro `key` (igual que en los ordenamientos).
- **Promedio (media aritmética)**: suma de los valores dividida por la cantidad
  de elementos, `sum(valores) / len(valores)`. Se aplica a población y superficie.
- **Conteo por categoría**: cantidad de países por continente, acumulando en un
  diccionario contador:

```python
conteo = {}
for pais in paises:
    continente = pais["continente"]
    conteo[continente] = conteo.get(continente, 0) + 1
```

## 7. Archivos CSV

CSV (*Comma-Separated Values*) es un formato de texto plano para datos tabulares:
cada línea es un registro y los campos se separan con comas. La primera línea suele
ser un **encabezado** con los nombres de las columnas. Es un formato simple,
legible y compatible con planillas de cálculo, por eso es muy usado para
intercambiar datasets.

El archivo `paises.csv` del proyecto tiene esta forma:

```
nombre,poblacion,superficie,continente
Argentina,46735004,2780400,América del Sur
Brasil,213421037,8515767,América del Sur
```

Para trabajar con archivos, Python provee la función `open()` junto con el bloque
`with`, que garantiza el cierre del archivo aunque ocurra un error. Al leer, cada
línea se separa en campos y se convierte al tipo correcto (`int()` para población
y superficie), validando el formato: si una línea tiene campos faltantes o valores
no numéricos, el programa lo informa con un mensaje claro en lugar de finalizar
abruptamente.

## Bibliografía

- Python Software Foundation. *El tutorial de Python — 3.1.3 Listas y 5. Estructuras de datos*. https://docs.python.org/es/3/tutorial/datastructures.html
- Python Software Foundation. *El tutorial de Python — 4. Más herramientas para control de flujo* (condicionales, `for`, definición de funciones). https://docs.python.org/es/3/tutorial/controlflow.html
- Python Software Foundation. *Sorting Techniques (Sorting HOW TO)*. https://docs.python.org/es/3/howto/sorting.html
- Python Software Foundation. *El tutorial de Python — 7.2 Leyendo y escribiendo archivos*. https://docs.python.org/es/3/tutorial/inputoutput.html
- Python Software Foundation. *Funciones incorporadas: `sorted()`, `max()`, `min()`, `sum()`*. https://docs.python.org/es/3/library/functions.html
- RFC 4180. *Common Format and MIME Type for Comma-Separated Values (CSV) Files*. https://www.rfc-editor.org/rfc/rfc4180
- Apuntes de la cátedra Programación 1, Tecnicatura Universitaria en Programación a Distancia, UTN.
