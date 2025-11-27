"""
Benchmark realista de SkipList (1 millón de inserciones).
- Pide al usuario el número a buscar (entero).
- Mide tiempo de inserción total y tiempo de búsqueda con alta resolución.
- Implementación probabilística estándar de Skip List.
"""

import random
import time

class Node:
    def __init__(self, value, level):
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=20, p=0.5):
        """
        max_level: altura máxima permitida (recomendado ~ log2(N))
        p: probabilidad para random_level (0.5 es estándar)
        """
        self.max_level = max_level
        self.p = p
        self.header = Node(-1, max_level)
        self.level = 0

    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, value):
        update = [None] * (self.max_level + 1)
        current = self.header

        # buscar posición (predecesores) desde el nivel actual máximo
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        # nivel aleatorio para el nuevo nodo
        new_level = self.random_level()

        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        new_node = Node(value, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, value) -> bool:
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
        current = current.forward[0]
        return (current is not None and current.value == value)


def benchmark_insert_and_search():
    N = 1_000_000
    print("\n=== BENCHMARK SKIP LIST (1,000,000 inserciones) ===")
    print("Construyendo skip list y realizando inserciones. Esto puede tardar algunos segundos...")

    sl = SkipList(max_level=20, p=0.5)

    t0 = time.perf_counter()
    # Insertamos valores 1..N
    for i in range(1, N + 1):
        sl.insert(i)
    t1 = time.perf_counter()

    insert_time = t1 - t0
    print(f"Tiempo total de inserción de {N:,} elementos: {insert_time:.4f} s")

    # Pedir al usuario el valor a buscar
    while True:
        s = input(f"\nIntroduce el entero a buscar (1..{N}) o 'exit' para terminar: ").strip()
        if s.lower() in ("exit", "quit"):
            print("Saliendo del benchmark.")
            break
        try:
            target = int(s)
        except ValueError:
            print("Entrada inválida: introduce un entero válido.")
            continue
        if not (1 <= target <= N):
            print(f"Fuera de rango: introduce un entero entre 1 y {N}.")
            continue

        # Medición precisa del tiempo de búsqueda
        t2 = time.perf_counter()
        found = sl.search(target)
        t3 = time.perf_counter()
        search_time = t3 - t2

        print(f"Encontrado: {found}")
        # Mostrar tiempo en segundos y en microsegundos para claridad
        print(f"Tiempo de búsqueda: {search_time:.9f} segundos ({search_time * 1e6:.1f} μs)")

    print("\n=== FIN BENCHMARK ===\n")

if __name__ == "__main__":
    benchmark_insert_and_search()

