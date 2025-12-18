def find_all_cycles(adjacency_table):
    def dfs_recursive(current_node, parent_node, visited, path, cycles, depth=0):
        if visited[current_node] == 1:
            if current_node in path:
                # Формируем цикл: от первого вхождения current_node до конца пути
                cycle_start = path.index(current_node)
                cycle = path[cycle_start:] + [current_node]
                cycle = normalize_cycle(cycle)

                if cycle not in cycles:
                    cycles.append(cycle)
            return

        visited[current_node] = 1
        path.append(current_node)

        # Обход всех соседей текущего узла
        for neighbor in adjacency_table.get(current_node, []):
            if neighbor != parent_node:
                dfs_recursive(neighbor, current_node, visited, path, cycles, depth + 1)
        path.pop()
        visited[current_node] = 2

    def normalize_cycle(cycle):
        if not cycle:
            return cycle

        min_idx = 0
        for i in range(1, len(cycle)):
            if cycle[i] < cycle[min_idx]:
                min_idx = i

        normalized = cycle[min_idx:] + cycle[:min_idx]

        if len(normalized) > 2:
            reversed_cycle = normalized[::-1]
            if reversed_cycle < normalized:
                return reversed_cycle
        return normalized

    visited = {node: 0 for node in adjacency_table.keys()}  # 0 - не посещена, 1 - в процессе, 2 - обработана
    all_cycles = []

    for node in adjacency_table.keys():
        if visited[node] == 0:
            current_path = []
            dfs_recursive(node, -1, visited, current_path, all_cycles)

    return all_cycles

k_graph = {
    0: [1],
    1: [0, 2, 3],
    2: [0, 1],
    3: [0, 1, 2],
}

cycles_k = find_all_cycles(k_graph)
print(f"Найденные циклы в K: {cycles_k}")
