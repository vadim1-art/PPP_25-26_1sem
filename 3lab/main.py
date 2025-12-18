def find_all_cycles(adjacency_table):
    def dfs_recursive(current_node, parent_node, visited, path, cycles, depth=0):
        if visited[current_node] == 1:
            if current_node in path:
                # Формируем цикл: от первого вхождения current_node до конца пути
                cycle_start = path.index(current_node)
                cycle = path[cycle_start:]
                cycle.append(current_node)
                cycle = normalize_cycle(cycle)

                if cycle not in cycles and len(cycle) > 3:
                    cycles.append(cycle)
            return

        visited[current_node] = 1
        path.append(current_node)

        # Рекурсивно обходим всех соседей
        for neighbor in adjacency_table.get(current_node, []):
            if neighbor != parent_node:
                dfs_recursive(neighbor, current_node, visited, path, cycles, depth + 1)
        path.pop()
        visited[current_node] = 2

    def normalize_cycle(cycle):
        if not cycle:
            return cycle

        min_idx = 0
        for i in range(1, len(cycle) - 1):
            if cycle[i] < cycle[min_idx]:
                min_idx = i

        normalized = cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]]

        if len(normalized) > 2:
            reversed_cycle = [normalized[0]] + normalized[-2:0:-1] + [normalized[0]]
            if reversed_cycle[1] < normalized[1]:
                return reversed_cycle
        return normalized

    visited = {node: 0 for node in adjacency_table.keys()}  # 0 - не посещена, 1 - в процессе, 2 - обработана
    all_cycles = []

    for node in adjacency_table.keys():
        if visited[node] == 0:
            current_path = []
            dfs_recursive(node, -1, visited, current_path, all_cycles)

    return all_cycles


def get_intermediate_states(adjacency_table, start_node):
    states = []

    def dfs_with_tracking(current_node, parent_node, visited, path, cycles, depth=0):
        state = {
            'depth': depth,
            'current_node': current_node,
            'parent_node': parent_node,
            'visited': visited.copy(),
            'current_path': path.copy(),
            'found_cycles': [cycle.copy() for cycle in cycles]
        }
        states.append(state)

        if visited[current_node] == 1:
            if current_node in path:
                cycle_start = path.index(current_node)
                cycle = path[cycle_start:] + [current_node]
                if len(cycle) > 3 and cycle not in cycles:
                    cycles.append(cycle.copy())
                    # Сохраняем состояние после нахождения цикла
                    state_after = state.copy()
                    state_after['found_cycles'] = [cycle.copy() for cycle in cycles]
                    states.append(state_after)
            return

        visited[current_node] = 1
        path.append(current_node)

        for neighbor in adjacency_table.get(current_node, []):
            if neighbor != parent_node:
                dfs_with_tracking(neighbor, current_node, visited, path, cycles, depth + 1)

        path.pop()
        visited[current_node] = 2

    visited = {node: 0 for node in adjacency_table.keys()}
    cycles = []
    path = []

    dfs_with_tracking(start_node, -1, visited, path, cycles)
    return states

if __name__ == "__main__":
    print("Пример: полный граф K3 (треугольник)")
    k3_graph = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1]
    }

    cycles_k3 = find_all_cycles(k3_graph)
    print(f"Найденные циклы в K3: {cycles_k3}")
