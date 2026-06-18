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

## Manejo de errores: dos estrategias

Las validaciones lanzan excepciones (`raise ValueError("mensaje descriptivo")`) en
lugar de imprimir directamente, y quien llama decide qué hacer con el error
(`try/except ValueError as e: print("Error:", e)`). Según qué tan recuperable sea
el error, conviven dos estrategias:

1. **Errores recuperables en el lugar** — se atrapan cerca de donde ocurren, con un
   *subciclo* que informa y reintenta hasta recibir un dato válido. El usuario no
   pierde lo que ya cargó. Casos: nombre vacío o duplicado en el alta
   (`validar_nombre`), rango con mínimo mayor que máximo en los filtros, opción de
   menú fuera de rango (`pedir_opcion`), entrada no numérica (`pedir_entero_positivo`).

2. **Errores que abortan la operación** — la función los lanza y **no** los atrapa:
   la excepción propaga hasta el `try/except` del loop principal en `main()`, que
   imprime el mensaje y vuelve a mostrar el menú. Caso: actualizar un país que no
   existe (ahí no tiene sentido insistir; probablemente el usuario quiera ir antes
   a la opción de búsqueda).

La ventaja de lanzar excepciones en vez de imprimir es que **la función que valida
no decide la política de manejo**: el mismo `validar_nombre` puede usarse en un
subciclo con reintento o dejarse propagar, sin tocar su código. El `try/except` del
loop principal funciona además como red de seguridad de todo el programa: cualquier
`ValueError` no manejado se informa y el programa sigue, nunca se corta abruptamente.

`csv/paises.csv` se genera con `csv/generar_csv.py` a partir de la API pública
[restcountries.com](https://restcountries.com/), con esta limpieza:

- Nombres en español (campo `translations.spa` de la API), sin comas para que el
  archivo pueda parsearse con un simple `split(",")`.
- Superficie redondeada a entero (km²); continente único (si un país figura en dos
  continentes se toma el principal).
- Se excluyen 5 territorios sin población (la consigna no admite campos vacíos).
- 245 países, ordenados alfabéticamente ignorando tildes.
