Este programa implementa una demostración interactiva y visual del funcionamiento interno
de una estructura de datos conocida como Skip List. A diferencia de las skip lists
aleatorias tradicionales, esta versión utiliza una distribución determinística de niveles
para facilitar el aprendizaje y la observación del proceso de búsqueda.

Qué hace el programa:
- Construye una Skip List con 5 niveles (0 al 4), donde el nivel 4 es el más alto.
- Contiene los enteros del 1 al 1000 distribuidos según reglas fijas:
    * Nivel 4: múltiplos de 200
    * Nivel 3: múltiplos de 100
    * Nivel 2: múltiplos de 20
    * Nivel 1: múltiplos de 5
    * Nivel 0: todos los números del 1 al 1000
- Permite al usuario ingresar un número para ver cómo la skip list lo busca paso a paso.
- La visualización muestra:
    * Avances horizontales en cada nivel
    * Descensos hacia niveles inferiores
    * Dónde aparece el valor objetivo en distintos niveles
    * Confirmación final en el nivel 0
    * Estadísticas de rendimiento comparadas con búsqueda lineal

Qué esperar al ejecutarlo:
- Una presentación clara de la estructura de niveles.
- Una animación textual de la búsqueda.
- Un análisis del recorrido realizado.
- Confirmación de si el número se encuentra o no en la lista.

Este archivo es únicamente informativo. El código principal se encuentra en el archivo skip_list.py
correspondiente.
