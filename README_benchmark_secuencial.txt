Este programa implementa una comparación secuencial entre dos estructuras de datos:
un Árbol AVL y una Skip List clásica.
El objetivo es analizar su comportamiento interno y medir su rendimiento real cuando realizan grandes volúmenes de inserciones y búsquedas sin concurrencia.

Qué hace el programa:

Construye una Skip List y un Árbol AVL desde cero.

Inserta en cada estructura 1,000,000 de valores consecutivos (del 1 al 1,000,000).

Realiza 100,000 búsquedas aleatorias en ambas.

Mide:

Tiempo total de inserción.

Tiempo total de búsqueda.

Tiempo promedio por búsqueda individual.

Presenta un resumen comparativo final SkipList vs AVL.

Detalles de cada estructura:
Skip List

Implementación con niveles generados aleatoriamente.

Probabilidad de subida de nivel: p = 0.5.

Máximo de 20 niveles posibles.

Inserción utilizando un vector update para mantener los punteros por nivel.

Búsqueda descendiendo niveles desde el nivel más alto hasta nivel 0.

Árbol AVL

Inserción con rebalance automático:

Rotaciones LL, RR, LR y RL.

Actualización correcta de alturas.

Búsqueda iterativa por comparación de claves.

Qué esperar al ejecutarlo:

Un recorrido completo por la construcción secuencial de ambas estructuras.

Tiempos precisos de inserción y búsqueda para cada una.

Una comparación objetiva entre:

la estructura con rebalanceo estricto (AVL),

y la estructura probabilística por niveles (Skip List).

Resultados claros para analizar cuál estructura es más eficiente en un escenario secuencial puro.

Diferencias con la versión concurrente de 8 hilos (otro archivo del proyecto):

Este programa es totalmente secuencial:
no utiliza hilos, no emplea locks, no simula contención ni carga paralela.

Se centra únicamente en:
costo algorítmico puro, no en rendimiento bajo concurrencia.

La versión de 8 hilos sí mide:

contención real,

escalabilidad,

interferencia entre hilos,

y el impacto del locking en AVL y Skip List.

Este archivo es únicamente descriptivo.
El código principal se encuentra en el archivo correspondiente donde se implementa el benchmark secuencial.