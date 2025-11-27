#!/usr/bin/env python3
"""
Skip List didáctica — CORREGIDA

- Niveles 0..4 (4 = superior, 0 = base)
- Contenido 1..1000
- Distribución determinística:
    nivel 4 -> múltiplos de 200
    nivel 3 -> múltiplos de 100
    nivel 2 -> múltiplos de 20
    nivel 1 -> múltiplos de 5
    nivel 0 -> todos
- Si al bajar llegas exactamente sobre el valor (pred_value == target),
  se marca aparición en ese nivel y no se avanza sobre él.
"""
from typing import List, Dict, Optional, Tuple
import bisect

MIN_VALUE = 1
MAX_VALUE = 1000
LEVELS = 5
TOP_LEVEL = LEVELS - 1

LEVEL_STEPS = {4: 200, 3: 100, 2: 20, 1: 5, 0: 1}
NEIGHBORHOOD_RADIUS = 10


def build_levels(min_v: int = MIN_VALUE, max_v: int = MAX_VALUE) -> Dict[int, List[int]]:
    base = list(range(min_v, max_v + 1))
    levels = {}
    for lvl in range(LEVELS):
        step = LEVEL_STEPS[lvl]
        if step == 1:
            levels[lvl] = base.copy()
        else:
            levels[lvl] = [v for v in base if v % step == 0]
    return levels


def compact_repr(arr: List[int], highlight_idx: Optional[int] = None) -> str:
    n = len(arr)
    if n <= 12:
        parts = []
        for i, v in enumerate(arr):
            if highlight_idx is not None and i == highlight_idx:
                parts.append(f">[{v}]<")
            else:
                parts.append(f"[{v}]")
        return " ".join(parts)
    # otherwise show prefix, maybe middle around highlight, suffix
    pref = arr[:3]
    suf = arr[-3:]
    parts = [f"[{v}]" for v in pref]
    if highlight_idx is not None and 3 <= highlight_idx < n - 3:
        left = max(3, highlight_idx - 1)
        right = min(n - 3, highlight_idx + 2)
        parts.append("...")
        parts += [f"[{v}]" for v in arr[left:right]]
        parts.append("...")
    else:
        parts.append("...")
    parts += [f"[{v}]" for v in suf]
    # if highlight in prefix or suffix, show marker
    line = " ".join(parts)
    if highlight_idx is not None and highlight_idx < 3:
        line = line.replace(f"[{arr[highlight_idx]}]", f">[{arr[highlight_idx]}]<", 1)
    elif highlight_idx is not None and highlight_idx >= n - 3:
        # replace last occurrence corresponding to suffix item
        target = f"[{arr[highlight_idx]}]"
        # find last occurrence of that target in the joined string (safe)
        idx = line.rfind(target)
        if idx != -1:
            line = line[:idx] + f">{target[1: -1]}<".replace("", "") + line[idx + len(target):]  # fallback no-op
        # simpler: don't overcomplicate, skip precise marking in suffix
    return line


def neighborhood_repr(arr: List[int], target: int, radius: int = NEIGHBORHOOD_RADIUS) -> Tuple[str, int]:
    idx = bisect.bisect_left(arr, target)
    start = max(0, idx - radius)
    end = min(len(arr), idx + radius + 1)
    sub = arr[start:end]
    pred_offset = bisect.bisect_left(sub, target) - 1
    parts = []
    for v in sub:
        if v == target:
            parts.append(f">[{v}]<")
        else:
            parts.append(f"[{v}]")
    return " ".join(parts), pred_offset


def search_visual(levels: Dict[int, List[int]], target: int):
    print(f"Contenido: enteros {MIN_VALUE}..{MAX_VALUE}")
    print(f"Niveles: 0 (base) .. {TOP_LEVEL} (superior). Se inicia en nivel {TOP_LEVEL}.\n")

    if target < MIN_VALUE or target > MAX_VALUE:
        print(f"✖ Fuera de rango: {target}\n")
        return

    appearances = {lvl: False for lvl in range(LEVELS)}
    horizontal = 0
    vertical = 0

    # pred_value es el valor del nodo donde nos quedamos en el nivel superior (None = header)
    pred_value: Optional[int] = None

    for lvl in range(TOP_LEVEL, -1, -1):
        arr = levels[lvl]
        print(f"=== Nivel {lvl} ===")

        # calcular índice del predecessor en este nivel a partir de pred_value
        if pred_value is None:
            pred_idx = -1
        else:
            # bisect_right - 1 es el índice del último <= pred_value
            pred_idx = bisect.bisect_right(arr, pred_value) - 1

        # Mostrar representación
        if lvl >= 2:
            repr_line = compact_repr(arr, highlight_idx=(pred_idx if pred_idx >= 0 else None))
            print(repr_line)
            if pred_idx >= 0:
                print(f"(Inicio en valor {arr[pred_idx]} en este nivel)")
            else:
                print("(Inicio desde cabecera virtual antes del primer bloque)")
        else:
            line, pred_offset = neighborhood_repr(arr, target)
            print(line)
            if pred_idx >= 0:
                pv = arr[pred_idx]
                print(f"(Inicio en valor {pv} en este nivel.")
            else:
                print("(Inicio desde cabecera virtual.")

        # --- CORRECCIÓN CRÍTICA: si pred_value == target => marca aparición YA ---
        if pred_value is not None and pred_idx >= 0 and arr[pred_idx] == target:
            appearances[lvl] = True
            print(f"[Nivel {lvl}] Atención: ya estamos SOBRE el valor {target}.")
            # No avanzamos horizontalmente; el predecessor para el nivel inferior será este mismo nodo
            pred_for_next_idx = pred_idx
        else:
            # avanzar estrictamente sobre valores < target
            idx = pred_idx + 1
            while idx < len(arr) and arr[idx] < target:
                print(f"[Nivel {lvl}] Avanzando → {arr[idx]}  (porque {arr[idx]} < {target})")
                horizontal += 1
                idx += 1

            # ahora idx es primer índice con arr[idx] >= target, o idx == len(arr)
            if idx < len(arr) and arr[idx] == target:
                appearances[lvl] = True
                print(f"[Nivel {lvl}] El valor {target} APARECE en este nivel (arr[{idx}] == {target}).")
                pred_for_next_idx = idx  # empezar abajo desde este nodo
            else:
                if idx < len(arr):
                    print(f"[Nivel {lvl}] No puedo avanzar más: arr[{idx}] = {arr[idx]} >= {target}")
                else:
                    print(f"[Nivel {lvl}] Llegué al final del nivel (no hay más elementos a la derecha).")
                pred_for_next_idx = idx - 1  # predecessor real (puede ser -1)

        # Mapear pred_for_next_idx a pred_value para el siguiente nivel
        if pred_for_next_idx >= 0:
            pred_value = arr[pred_for_next_idx]
        else:
            pred_value = None

        # contar descenso si bajamos
        if lvl > 0:
            vertical += 1
            print(f"[Acción] Bajando desde nivel {lvl} al {lvl - 1} (inicio en "
                  f"{pred_value if pred_value is not None else 'cabecera virtual'}).\n")
        else:
            print("")  # separación final

    # Resultado
    found = appearances[0]  # confirmación en base
    print("\n--- RESULTADO FINAL ---")
    if found:
        print(f"✔ El valor {target} existe en la Skip List (confirmado en nivel 0).")
    else:
        print(f"✖ El valor {target} NO existe en la Skip List.")

    present = [lvl for lvl, seen in appearances.items() if seen]
    if present:
        print("Aparece exactamente en los niveles:", present)
    else:
        print("No aparece exactamente en ningún nivel (improbable dado que 1..1000 están).")

    print("\n--- ESTADÍSTICAS ---")
    print(f"Movimientos horizontales: {horizontal}")
    print(f"Descensos (verticales): {vertical}")
    print("--- FIN BÚSQUEDA ---\n")


def main():
    levels = build_levels()
    print("===========================================")
    print("   SKIP LIST DIDÁCTICA (Consola) - Demo")
    print("===========================================\n")
    print(f"Esta skip list contiene exactamente los enteros {MIN_VALUE}..{MAX_VALUE}.")
    print("Hay 5 niveles numerados 0..4 (4 = superior, 0 = base).")
    for lvl in range(TOP_LEVEL, -1, -1):
        step = LEVEL_STEPS[lvl]
        desc = "todos los enteros" if step == 1 else f"múltiplos de {step}"
        print(f"  - Nivel {lvl}: {desc}")
    print("\nEscribe un número (1..1000) para ver la búsqueda, 'exit' para terminar.\n")

    while True:
        s = input("Valor a buscar (1..1000) o 'exit': ").strip()
        if s.lower() in ("exit", "quit"):
            print("Saliendo...")
            break
        try:
            v = int(s)
        except ValueError:
            print("Entrada inválida. Introduce un entero 1..1000 o 'exit'.\n")
            continue
        if v < MIN_VALUE or v > MAX_VALUE:
            print("Valor fuera de rango.\n")
            continue
        search_visual(levels, v)


if __name__ == "__main__":
    main()







