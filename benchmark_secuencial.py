import random
import time

# ============================
#   AVL TREE IMPLEMENTATION
# ============================

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def height(n):
    return n.height if n else 0

def update_height(n):
    n.height = max(height(n.left), height(n.right)) + 1

def get_balance(n):
    return height(n.left) - height(n.right) if n else 0

def rotate_left(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    update_height(z)
    update_height(y)
    return y

def rotate_right(z):
    y = z.left
    T3 = y.right
    y.right = z
    z.left = T3
    update_height(z)
    update_height(y)
    return y

def avl_insert(node, key):
    if not node:
        return AVLNode(key)

    if key < node.key:
        node.left = avl_insert(node.left, key)
    else:
        node.right = avl_insert(node.right, key)

    update_height(node)

    balance = get_balance(node)

    # Left Left Case
    if balance > 1 and key < node.left.key:
        return rotate_right(node)

    # Right Right Case
    if balance < -1 and key > node.right.key:
        return rotate_left(node)

    # Left Right Case
    if balance > 1 and key > node.left.key:
        node.left = rotate_left(node.left)
        return rotate_right(node)

    # Right Left Case
    if balance < -1 and key < node.right.key:
        node.right = rotate_right(node.right)
        return rotate_left(node)

    return node

def avl_search(node, key):
    while node:
        if key == node.key:
            return True
        elif key < node.key:
            node = node.left
        else:
            node = node.right
    return False


# ============================
#      SKIP LIST
# ============================

class Node:
    def __init__(self, value, level):
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=20, p=0.5):
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

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        new_level = self.random_level()

        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        new_node = Node(value, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, value):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
        current = current.forward[0]
        return (current is not None and current.value == value)


# ============================
#    BENCHMARK SECUENCIAL
# ============================

def benchmark_secuencial():

    N = 1_000_000
    Q = 100_000  # búsquedas aleatorias

    print("\n=== BENCHMARK SECUENCIAL: SKIP LIST vs AVL ===")

    # ------------------------
    #       SKIP LIST
    # ------------------------
    print("\n--- SKIP LIST ---")
    sl = SkipList()

    t0 = time.perf_counter()
    for i in range(1, N + 1):
        sl.insert(i)
    t1 = time.perf_counter()

    sl_insert_time = t1 - t0
    print(f"Tiempo inserción SkipList: {sl_insert_time:.4f} s")

    # Búsquedas aleatorias
    queries = [random.randint(1, N) for _ in range(Q)]

    t2 = time.perf_counter()
    for q in queries:
        sl.search(q)
    t3 = time.perf_counter()

    sl_search_total = t3 - t2
    sl_search_avg = sl_search_total / Q * 1e6  # microsegundos

    print(f"Tiempo total búsqueda SkipList (100k): {sl_search_total:.4f} s")
    print(f"Promedio por búsqueda: {sl_search_avg:.3f} µs")

    # ------------------------
    #           AVL
    # ------------------------
    print("\n--- AVL ---")
    root = None

    t4 = time.perf_counter()
    for i in range(1, N + 1):
        root = avl_insert(root, i)
    t5 = time.perf_counter()

    avl_insert_time = t5 - t4
    print(f"Tiempo inserción AVL: {avl_insert_time:.4f} s")

    # Búsquedas aleatorias
    t6 = time.perf_counter()
    for q in queries:
        avl_search(root, q)
    t7 = time.perf_counter()

    avl_search_total = t7 - t6
    avl_search_avg = avl_search_total / Q * 1e6

    print(f"Tiempo total búsqueda AVL (100k): {avl_search_total:.4f} s")
    print(f"Promedio por búsqueda: {avl_search_avg:.3f} µs")

    # ------------------------
    #       COMPARACIÓN
    # ------------------------
    print("\n=== RESUMEN ===")
    print(f"SkipList inserción: {sl_insert_time:.4f} s")
    print(f"AVL inserción     : {avl_insert_time:.4f} s")

    print(f"SkipList búsqueda total: {sl_search_total:.4f} s")
    print(f"AVL búsqueda total     : {avl_search_total:.4f} s")

    print(f"SkipList promedio búsqueda: {sl_search_avg:.3f} µs")
    print(f"AVL promedio búsqueda     : {avl_search_avg:.3f} µs")


if __name__ == "__main__":
    benchmark_secuencial()
