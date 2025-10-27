from diktyonphi import Graph, GraphType
from typing import Dict, List

class WeightedGraph(Graph):
    def __init__(self, neighbor_matrix: List[List[float]]):
        super().__init__(GraphType.DIRECTED)
        self._matrix = neighbor_matrix
        for i in range(len(neighbor_matrix)):
            for j in range(len(neighbor_matrix[i])):
                if neighbor_matrix[i][j] >= 0:
                    self.add_edge(i, j, {"weight": neighbor_matrix[i][j]})

    def get_graph(self) -> Graph:
        new_graph = Graph(self.type)
        # Přidej všechny uzly
        for node_id in self.node_ids():
            new_graph.add_node(node_id)
        # Přidej všechny hrany se stejnými atributy
        for node_id in self.node_ids():
            for neighbor_id, attrs in self.get_neighbors(node_id).items():
                new_graph.add_edge(node_id, neighbor_id, attrs.copy())
        return new_graph
    
    def component_count(self) -> int:
        def get_and_flag_neighbors(node_id: int, current_component: set, visited: set, components: list):
            visited.add(node_id)
            current_component.add(node_id)
            neighbors = self.get_neighbors(node_id)
            for neighbor_id in neighbors:
                if neighbor_id not in visited:
                    get_and_flag_neighbors(neighbor_id, current_component, visited, components)
                elif neighbor_id not in current_component:
                    for i in range(len(components)):
                        if neighbor_id in components[i]:
                            current_component.update(components.pop(i))
                            break
            return current_component
        
        components = list()
        visited = set()
        for node_id in self.node_ids():
            if node_id not in visited:
                current_component = set()
                get_and_flag_neighbors(node_id, current_component, visited, components)
                components.append(current_component)
        return len(components)
        
    def get_sorted_weights(self):
        weights = [self._matrix[i][j]
                for i in range(len(self._matrix))
                for j in range(len(self._matrix[i]))
                if self._matrix[i][j] >= 0]
        return iter(sorted(weights))


if __name__ == "__main__":
    # Example usage
    neighbor_matrix = [
    [-1, 2, -1, -1, -1, -1, -1],  # 0 → 1 (váha 2)
    [-1, -1, -1, -1, -1, -1, -1], # 1
    [-1, -1, -1, 5, -1, -1, -1],  # 2 → 3 (váha 5)
    [-1, -1, -1, -1, -1, -1, -1], # 3
    [-1, 1, -1, -1, -1, 1, -1],  # 4 → 5 (váha 1)
    [-1, -1, -1, -1, -1, -1, 3],  # 5 → 6 (váha 3)
    [-1, -1, -1, -1, -1, -1, -1], # 6
    ]
    
    weighted_graph = WeightedGraph(neighbor_matrix)
    weighted_graph.export_to_png("weighted_graph.png")
    
    print("Component count:", weighted_graph.component_count())
    print("Sorted weights:", list(weighted_graph.get_sorted_weights()))