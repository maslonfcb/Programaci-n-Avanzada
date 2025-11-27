import threading
import random
import time

# ============================================================
# AVL TREE
# ============================================================
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.lock = threading.Lock()

    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)

        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)

        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key):
        with self.lock:
            start = time.time()
            self.root = self._insert(self.root, key)
            return time.time() - start

    def search(self, key):
        node = self.root
        start = time.time()
        while node:
            if key == node.key:
                return True, time.time() - start
            node = node.left if key < node.key else node.right
        return False, time.time() - start


# ============================================================
# SKIPLIST
# ============================================================
class SkipListNode:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    MAX_LEVEL = 16
    P = 0.5

    def __init__(self):
        self.header = SkipListNode(-1, self.MAX_LEVEL)
        self.level = 0
        self.insert_lock = threading.Lock()  # Único lock global para inserción

    def random_level(self):
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def search(self, key):
        node = self.header
        start = time.time()
        for lvl in reversed(range(self.level + 1)):
            while node.forward[lvl] and node.forward[lvl].key < key:
                node = node.forward[lvl]
        node = node.forward[0]
        if node and node.key == key:
            return True, time.time() - start
        return False, time.time() - start

    def insert(self, key):
        with self.insert_lock:
            update = [None] * (self.MAX_LEVEL + 1)
            node = self.header

            # 1. Encontrar posición
            for lvl in reversed(range(self.level + 1)):
                while node.forward[lvl] and node.forward[lvl].key < key:
                    node = node.forward[lvl]
                update[lvl] = node

            node = node.forward[0]

            if node and node.key == key:
                return 0.0  # No insertar duplicado

            # 2. Nivel para el nuevo nodo
            lvl = self.random_level()

            if lvl > self.level:
                for i in range(self.level + 1, lvl + 1):
                    update[i] = self.header
                self.level = lvl

            # 3. Inserción real
            new_node = SkipListNode(key, lvl)

            start = time.time()
            for i in range(lvl + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

            return time.time() - start


# ============================================================
# TRABAJO DE LOS HILOS
# ============================================================
def worker(structure, values, results):
    insert_time = 0.0
    search_time = 0.0

    for x in values:
        insert_time += structure.insert(x)

        # Lote de búsquedas aleatorias
        for _ in range(10):
            target = random.randint(1, 1_000_000)
            _, t = structure.search(target)
            search_time += t

    results.append((insert_time, search_time))


# ============================================================
# BENCHMARK GENERAL
# ============================================================
def run_benchmark(structure, name):
    print(f"\nEjecutando {name}...")

    threads = []
    results = []

    NUM_THREADS = 8
    BLOCK = 1_000_000 // NUM_THREADS

    start_global = time.time()

    for i in range(NUM_THREADS):
        start = i * BLOCK + 1
        end = (i + 1) * BLOCK
        t = threading.Thread(target=worker, args=(structure, range(start, end+1), results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_insert = sum(r[0] for r in results)
    total_search = sum(r[1] for r in results)
    total_time = time.time() - start_global

    print("\nResultados:")
    print(f"- Tiempo total concurrente: {total_time:.4f} segundos")
    print(f"- Tiempo acumulado en inserciones: {total_insert:.4f} segundos")
    print(f"- Tiempo acumulado en búsquedas: {total_search:.4f} segundos")


# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    run_benchmark(SkipList(), "SkipList")
    run_benchmark(AVLTree(), "AVL")



