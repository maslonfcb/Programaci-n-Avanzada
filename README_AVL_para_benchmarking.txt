Este programa implementa un Árbol AVL y realiza un benchmark centrado exclusivamente en medir su rendimiento durante la inserción de 1,000,000 elementos y en la búsqueda 
interactiva de valores. Está diseñado para observar de manera práctica el comportamiento de un AVL real bajo carga intensa.

Qué hace el programa:

Construye un Árbol AVL completamente balanceado insertando los enteros del 1 al 1,000,000 en orden creciente.

Mide el tiempo total de construcción del árbol.

Permite al usuario realizar búsquedas interactivas:

Se ingresa un número por consola.

El programa indica si existe en el árbol.

Mide el tiempo exacto de la búsqueda en microsegundos.

Opera indefinidamente hasta que el usuario escriba exit o quit.

Funcionamiento interno del árbol AVL:
Inserción

El programa ejecuta la inserción típica BST seguida de:

actualización de alturas,

cálculo de factor de balance,

y aplicación de las rotaciones necesarias (LL, RR, LR y RL).

Garantiza que la altura del árbol se mantenga en O(log n) incluso al insertar un millón de elementos en orden ascendente, escenario donde un BST normal colapsaría a una lista.

Búsqueda

La búsqueda es estrictamente iterativa.

Recorre el árbol siguiendo comparaciones de valores.

Mantiene complejidad O(log n).

Qué esperar al ejecutarlo:

Una construcción completa del AVL que puede tardar varios segundos dependiendo del hardware.

Un árbol perfectamente balanceado a pesar de recibir entradas ordenadas.

Búsquedas extremadamente rápidas (microsegundos).

Retroalimentación completa:

Si el valor fue encontrado.

Tiempo exacto de búsqueda.

Validación de entradas incorrectas o fuera de rango.

En qué se diferencia del benchmark secuencial SkipList vs AVL:

Este archivo solo evalúa AVL, no compara estructuras.

El benchmark es interactivo, permite al usuario probar búsquedas en tiempo real.

A diferencia del benchmark comparativo:

No evalúa 100k búsquedas automáticas.

No genera estadísticas promedio.

No contrasta rendimiento contra otra estructura.

No genera un resumen final comparativo.

Este programa sirve más como herramienta de experimentación que como estudio estadístico.