def find_all_cycles(adj_table):
    graph = {}
    for node, edges in adj_table.items():
        graph[node] = edges if isinstance(edges, list) else [edges]

    all_cycles = set()
    current_path = []
    visited_in_path = set()

    def dfs(current_node, start_node=None, depth=0):
        nonlocal all_cycles, current_path, visited_in_path
        # Если мы уже посещали эту вершину в текущем пути
        if current_node in visited_in_path:
            cycle_start_idx = current_path.index(current_node)
            cycle = current_path[cycle_start_idx:]

            # Нормализуем цикл: начинаем с наименьшей вершины
            if len(cycle) > 1:  # Игнорируем петли на одной вершине
                # Находим индекс минимальной вершины
                min_idx = min(range(len(cycle)), key=lambda i: cycle[i])
                normalized_cycle = tuple(cycle[min_idx:] + cycle[:min_idx])
                normalized_cycle = normalized_cycle + (normalized_cycle[0],)
                all_cycles.add(normalized_cycle)
            return

        current_path.append(current_node)
        visited_in_path.add(current_node)
        # Рекурсивно обходим соседей
        for neighbor in graph.get(current_node, []):
            dfs(neighbor, start_node if start_node else current_node, depth + 1)

        current_path.pop()
        visited_in_path.remove(current_node)

    # Запускаем поиск из всех вершин
    for node in graph.keys():
        if node not in visited_in_path:
            current_path = []
            visited_in_path = set()
            dfs(node)
    return [list(cycle) for cycle in all_cycles]


def find_all_cycles_with_all_states(adj_table):
    graph = {}
    for node, edges in adj_table.items():
        graph[node] = edges if isinstance(edges, list) else [edges]

    all_cycles = set()
    current_path = []
    visited_in_path = set()
    all_states = []  # Список для хранения всех состояний

    def dfs(current_node, start_node=None, depth=0):
        nonlocal all_cycles, current_path, visited_in_path, all_states
        # Проверяем, не посещали ли уже эту вершину в текущем пути
        if current_node in visited_in_path:
            cycle_start_idx = current_path.index(current_node)
            cycle = current_path[cycle_start_idx:] + [current_node]

            if len(cycle) > 2:  # Игнорируем петли и обратные ребра
                min_idx = min(range(len(cycle) - 1), key=lambda i: cycle[i])
                normalized_cycle = tuple(cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]])
                all_cycles.add(normalized_cycle)
            return

        current_path.append(current_node)
        visited_in_path.add(current_node)

        # Рекурсивно обходим соседей
        for neighbor in graph.get(current_node, []):
            dfs(neighbor, start_node if start_node else current_node, depth + 1)

        current_path.pop()
        visited_in_path.remove(current_node)
    # Запускаем обход из всех вершин
    for node in graph.keys():
        if node not in visited_in_path:
            init_state = {
                'step': len(all_states) + 1,
                'action': 'start_new_component',
                'start_node': node,
                'found_cycles': list(all_cycles)
            }

            current_path = []
            visited_in_path = set()
            dfs(node)

    return [list(cycle) for cycle in all_cycles], all_states

k_graph = {
    0: [1],
    1: [0]
}

cycles_detailed, states = find_all_cycles_with_all_states(k_graph)
print(f"Найдено циклов: {len(cycles_detailed)}")
