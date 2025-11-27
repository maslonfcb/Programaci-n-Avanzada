Este programa implementa una Skip List probabilística desde cero y ejecuta un benchmark simple de inserción y búsqueda. 
Su propósito es medir el rendimiento real de esta estructura para compararla posteriormente con un árbol balanceado (por ejemplo, AVL o Red-Black).

Qué hace el programa

Construye una Skip List con un nivel máximo de 20 y probabilidad de promoción p = 0.5.

Inserta exactamente 1,000,000 de valores consecutivos (del 1 al 1,000,000).

Mide el tiempo total de inserción usando time.perf_counter() (alta resolución).

Solicita al usuario un valor a buscar dentro del rango permitido.

Realiza la búsqueda en la Skip List y reporta:

Si el valor fue encontrado.

El tiempo de búsqueda en segundos y microsegundos.

Permite realizar múltiples búsquedas consecutivas hasta que el usuario escriba exit.

Qué se puede esperar al ejecutarlo

La fase de inserción puede tardar varios segundos dependiendo del hardware.

Las búsquedas individuales deben ser muy rápidas (microsegundos), debido a la naturaleza logarítmica de la Skip List.

El uso de memoria es considerable, ya que cada nodo contiene múltiples punteros según su nivel aleatorio.

El programa no genera archivos ni gráficos; solo imprime resultados en consola.