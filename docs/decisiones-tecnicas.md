# Decisiones técnicas

## Estructura de datos: lista de diccionarios

El dataset se carga en memoria como una **lista de diccionarios**, donde cada país es:

```python
{"nombre": str, "poblacion": int, "superficie": int, "continente": str}
```

Razones de la elección:

- **Cumple el criterio de evaluación** de uso de listas y diccionarios.
- La **lista** modela naturalmente una colección ordenada de registros: se recorre
  con `for` para mostrar/buscar/filtrar, se le hace `append()` en las altas y se
  reordena con `sorted()`.
- El **diccionario** da acceso por nombre de campo (`pais["poblacion"]`), mucho más
  legible que índices posicionales, y refleja directamente las columnas del CSV.
- `poblacion` y `superficie` se guardan como `int` (no `str`) para poder comparar,
  ordenar y promediar sin conversiones repetidas; la conversión y validación se hace
  una sola vez, al leer el archivo.

Alternativas descartadas:

- *Listas paralelas* (una lista por columna): frágiles, los índices pueden
  desincronizarse al agregar o eliminar registros.
- *Lista de listas*: no documenta qué guarda cada posición.
- *Clases / namedtuples*: válidas, pero exceden el alcance de la materia.

## Arquitectura del programa

Modularización por responsabilidad, según la estructura de la Etapa 4 del plan:

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Menú principal, loop del programa y despacho de opciones |
| `archivo.py` | Lectura/escritura de `paises.csv` y manejo de errores de formato |
| `operaciones.py` | Agregar, actualizar, buscar, filtrar y ordenar |
| `estadisticas.py` | Máximos/mínimos, promedios y conteo por continente |

Principios aplicados:

- **Una función = una responsabilidad**: cada opción del menú invoca una función
  específica que recibe la lista de países como parámetro y devuelve un resultado.
- **Validación en la frontera**: las entradas del usuario y el contenido del CSV se
  validan apenas ingresan al programa; el resto del código asume datos correctos.
- **Mensajes claros**: todo caso de error (entrada inválida, búsqueda sin
  resultados, CSV roto) produce un mensaje explicativo y nunca un cierre abrupto.

## Origen del dataset

`csv/paises.csv` se genera con `csv/generar_csv.py` a partir de la API pública
[restcountries.com](https://restcountries.com/), con esta limpieza:

- Nombres en español (campo `translations.spa` de la API), sin comas para que el
  archivo pueda parsearse con un simple `split(",")`.
- Superficie redondeada a entero (km²); continente único (si un país figura en dos
  continentes se toma el principal).
- Se excluyen 5 territorios sin población (la consigna no admite campos vacíos).
- 245 países, ordenados alfabéticamente ignorando tildes.
