Este repositorio contiene un benchmark en Python que compara el rendimiento concurrente de dos estructuras de datos: 
una SkipList (con inserciones protegidas por un lock global) y un AVL (inserciones protegidas por un lock global). 
El benchmark simula carga mixta con 8 hilos: cada hilo inserta un bloque contiguo de claves y, tras cada inserción, realiza búsquedas aleatorias en lotes.

 
Implementa:

- SkipList con insert_lock (lock global para insert) y búsquedas concurrentes sin lock.

- AVLTree con lock global para inserciones; búsquedas realizadas sin lock (lectura optimista).

- Worker multihilo: 8 hilos, cada uno inserta su bloque y ejecuta búsquedas intercaladas.

- Medición y salida en texto plano (líneas cortas y explicativas).



Qué miden exactamente las cifras

- Tiempo total concurrente: tiempo real (wall-clock) desde que se lanzan todos los hilos hasta que terminan todos.

- Tiempo acumulado en inserciones: suma de los tiempos medidos por cada hilo dentro de la operación insert() (acumulativo). 
Representa el trabajo "activo" de inserción sumado en todos los hilos.

- Tiempo acumulado en búsquedas: suma de los tiempos que los hilos pasan ejecutando search() (acumulativo).
