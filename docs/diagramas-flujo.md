# Diagramas de flujo

Diagramas de las operaciones principales del programa, en formato
[Mermaid](https://mermaid.js.org/). GitHub los renderiza directamente; para el PDF
se pueden exportar como imagen desde https://mermaid.live.

## 1. Flujo general del programa (menú principal)

```mermaid
flowchart TD
    A([Inicio]) --> B[Leer paises.csv]
    B --> C{¿Lectura correcta?}
    C -- No --> D[Mostrar error de formato] --> Z([Fin])
    C -- Sí --> E[/Mostrar menú/]
    E --> F[/Leer opción del usuario/]
    F --> G{¿Opción válida?}
    G -- No --> H[Mensaje: opción inválida] --> E
    G -- Sí --> I{¿Cuál opción?}
    I -- 1 --> O1[Mostrar todos los países]
    I -- 2 --> O2[Buscar país por nombre]
    I -- 3 --> O3[Agregar país]
    I -- 4 --> O4[Actualizar país]
    I -- 5 --> O5[Filtrar países]
    I -- 6 --> O6[Ordenar países]
    I -- 7 --> O7[Mostrar estadísticas]
    I -- "8 - Salir" --> Z
    O1 --> E
    O2 --> E
    O3 --> E
    O4 --> E
    O5 --> E
    O6 --> E
    O7 --> E
```

## 2. Buscar país por nombre

```mermaid
flowchart TD
    A([Inicio búsqueda]) --> B[/Pedir nombre a buscar/]
    B --> C{¿Entrada vacía?}
    C -- Sí --> D[Mensaje: el nombre no puede estar vacío] --> B
    C -- No --> E[Recorrer lista de países comparando<br>en minúsculas y por coincidencia parcial]
    E --> F{¿Hubo coincidencias?}
    F -- Sí --> G[Mostrar países encontrados]
    F -- No --> H[Mensaje: no se encontraron resultados]
    G --> Z([Volver al menú])
    H --> Z
```

## 3. Agregar país (alta con validaciones)

```mermaid
flowchart TD
    A([Inicio alta]) --> B[/Pedir nombre/]
    B --> C{¿Vacío o ya existe?}
    C -- Sí --> D[Mensaje de error] --> B
    C -- No --> E[/Pedir población/]
    E --> F{¿Entero positivo?}
    F -- No --> G[Mensaje: debe ser un entero positivo] --> E
    F -- Sí --> H[/Pedir superficie/]
    H --> I{¿Entero positivo?}
    I -- No --> J[Mensaje: debe ser un entero positivo] --> H
    I -- Sí --> K[/Pedir continente/]
    K --> L{¿Vacío?}
    L -- Sí --> M[Mensaje de error] --> K
    L -- No --> N["Crear diccionario del país y<br>agregarlo a la lista (append)"]
    N --> O[Guardar lista en paises.csv]
    O --> P[Mensaje: país agregado con éxito]
    P --> Z([Volver al menú])
```

## 4. Actualizar población y superficie de un país

```mermaid
flowchart TD
    A([Inicio actualización]) --> B[/Pedir nombre del país/]
    B --> C[Buscar el país en la lista]
    C --> D{¿Existe?}
    D -- No --> E[Mensaje: país no encontrado] --> Z([Volver al menú])
    D -- Sí --> F[/Pedir nueva población/]
    F --> G{¿Entero positivo?}
    G -- No --> H[Mensaje de error] --> F
    G -- Sí --> I[/Pedir nueva superficie/]
    I --> J{¿Entero positivo?}
    J -- No --> K[Mensaje de error] --> I
    J -- Sí --> L[Actualizar las claves del diccionario]
    L --> M[Guardar lista en paises.csv]
    M --> N[Mensaje: país actualizado con éxito]
    N --> Z
```

## 5. Filtrar países

```mermaid
flowchart TD
    A([Inicio filtro]) --> B[/Elegir criterio:<br>continente, población o superficie/]
    B --> C{¿Criterio?}
    C -- Continente --> D[/Pedir continente/]
    D --> E[Recorrer la lista y quedarse con<br>los países de ese continente]
    C -- Población --> F[/Pedir mínimo y máximo/]
    C -- Superficie --> F
    F --> H{¿Rango válido?}
    H -- No --> I[Mensaje: rango inválido] --> F
    H -- Sí --> J[Recorrer la lista y quedarse con<br>los países dentro del rango]
    E --> K{¿Hubo resultados?}
    J --> K
    K -- Sí --> L[Mostrar países filtrados]
    K -- No --> M[Mensaje: ningún país cumple el filtro]
    L --> Z([Volver al menú])
    M --> Z
```

## 6. Ordenar países

```mermaid
flowchart TD
    A([Inicio ordenamiento]) --> B[/Elegir campo:<br>nombre, población o superficie/]
    B --> C[/Elegir sentido:<br>ascendente o descendente/]
    C --> D{¿Opciones válidas?}
    D -- No --> E[Mensaje: opción inválida] --> B
    D -- Sí --> F["sorted(paises, key=campo, reverse=sentido)"]
    F --> G[Mostrar lista ordenada]
    G --> Z([Volver al menú])
```

## 7. Estadísticas

```mermaid
flowchart TD
    A([Inicio estadísticas]) --> B["País con mayor población: max(paises, key=poblacion)"]
    B --> C["País con menor población: min(paises, key=poblacion)"]
    C --> D["Promedio de población: sum / len"]
    D --> E["Promedio de superficie: sum / len"]
    E --> F[Conteo por continente:<br>recorrer la lista acumulando<br>en un diccionario contador]
    F --> G[Mostrar todos los resultados]
    G --> Z([Volver al menú])
```
