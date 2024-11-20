from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class Node(ABC):
    def __init__(self, code: Dict):
        self.code = code
        self.complexity = self.calculate_complexity()

    @abstractmethod
    def calculate_complexity(self) -> str:
        pass

class SimpleStatementNode(Node):
    def calculate_complexity(self) -> str:
        return "O(1)"

class LoopNode(Node):
    def calculate_complexity(self) -> str:
        # Obtener la profundidad del bucle
        depth = self.code.get("nested_depth", 1)
        if depth <= 0:
            depth = 1
            
        # Retornar O(n^depth)
        if depth == 1:
            return "O(n)"
        else:
            return f"O(n^{depth})"

class ConditionalNode(Node):
    def calculate_complexity(self) -> str:
        return "O(1)"

class FunctionCallNode(Node):
    def calculate_complexity(self) -> str:
        # Si la función es recursiva, retornar O(2^n)
        if self.code.get("is_recursive", False):
            return "O(2^n)"
        return "O(1)"
