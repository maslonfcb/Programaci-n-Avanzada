import time
import sys
sys.setrecursionlimit(2_000_000)  # necesario para permitir profundidad alta si tu Python lo requiere


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # rotación
        x.right = y
        y.left = T2

        # actualizar alturas
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # rotación
        y.left = x
        x.right = T2

        # actualizar alturas
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, value):
        # Inserción BST normal
        if not root:
            return Node(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        # actualizar altura
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # verificar balance
        balance = self.get_balance(root)

        # casos de rotación
        # Left Left
        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)

        # Right Right
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)

        # Left Right
        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left
        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, value):
        current = root
        while current:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False


def benchmark_avl():
    N = 1_000_000
    print("\n=== BENCHMARK AVL (1,000,000 inserciones) ===")
    print("Construyendo AVL y realizando inserciones. Esto tardará varios segundos...")

    avl = AVLTree()
    root = None

    t0 = time.perf_counter()
    for i in range(1, N + 1):
        root = avl.insert(root, i)
    t1 = time.perf_counter()

    print(f"Tiempo total de inserción de {N:,} elementos: {t1 - t0:.4f} s")

    # Búsquedas del usuario
    while True:
        s = input(f"\nIntroduce el entero a buscar (1..{N}) o 'exit' para salir: ").strip()
        if s.lower() in ("exit", "quit"):
            print("Saliendo del benchmark.")
            break

        try:
            target = int(s)
        except ValueError:
            print("Entrada inválida: introduce un entero.")
            continue

        if not (1 <= target <= N):
            print(f"Fuera de rango: usa un número entre 1 y {N}.")
            continue

        t2 = time.perf_counter()
        found = avl.search(root, target)
        t3 = time.perf_counter()

        print(f"Encontrado: {found}")
        print(f"Tiempo de búsqueda: {t3 - t2:.9f} segundos ({(t3 - t2) * 1e6:.1f} µs)")

    print("\n=== FIN BENCHMARK ===\n")


if __name__ == "__main__":
    benchmark_avl()
