from typing import List
from .node import Node

class Graph:
    def __init__(self):
        self.nodes: List[Node] = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def get_overall_complexity(self) -> str:
        # Calcular la complejidad general basada en todos los nodos
        # Por ahora, simplemente devuelve la complejidad más alta
        if not self.nodes:
            return "O(1)"
        
        complexities = []
        for node in self.nodes:
            complexity = node.complexity
            if complexity:
                complexities.append(complexity)
        
        # Encontrar la complejidad más alta
        if not complexities:
            return "O(1)"
            
        def complexity_value(c: str) -> float:
            if c == "O(1)":
                return 1
            elif c == "O(n)":
                return 2
            elif c.startswith("O(n^"):
                return 2 + float(c[4:-1])
            return 1
            
        return max(complexities, key=complexity_value)
