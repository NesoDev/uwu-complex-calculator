from abc import ABC, abstractmethod
from typing import Dict, List
import ast
from .graph import Graph
from .node import LoopNode, FunctionCallNode, ConditionalNode, SimpleStatementNode

class FunctionParser(ABC):
    @abstractmethod
    def parse(self, code: str) -> Graph:
        pass

    @abstractmethod
    def to_dict(self, code: str) -> Dict:
        pass

    @abstractmethod
    def identify_node_type(self, line: str) -> Graph:
        pass

class PythonParser(FunctionParser):
    def __init__(self):
        self.max_loop_depth = 1
        self.is_recursive = False
        self.main_function_name = None

    def parse(self, code: str) -> Graph:
        graph = Graph()
        try:
            # Reset state for new parse
            self.max_loop_depth = 1
            self.is_recursive = False
            self.main_function_name = None
            
            tree = ast.parse(code)
            code_dict = self.to_dict(code)
            
            # First pass: identify main function and check for recursion
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.main_function_name = node.name
                    # Check for recursive calls
                    for subnode in ast.walk(node):
                        if (isinstance(subnode, ast.Call) and 
                            hasattr(subnode.func, 'id') and 
                            subnode.func.id == node.name):
                            self.is_recursive = True
                            break
                    break
            
            # Second pass: analyze loop depths
            self._analyze_loop_depths(tree)
            
            # Third pass: create nodes
            for node in ast.walk(tree):
                if isinstance(node, (ast.For, ast.While)):
                    # Get loop depth for this specific loop
                    current_depth = self._get_loop_depth(node)
                    self.max_loop_depth = max(self.max_loop_depth, current_depth)
                    
                    graph.add_node(LoopNode({
                        "line": node.lineno,
                        "code": code_dict,
                        "nested_depth": self.max_loop_depth
                    }))
                elif isinstance(node, ast.Call):
                    # Check if this is a recursive call
                    is_recursive_call = (hasattr(node.func, 'id') and 
                                      node.func.id == self.main_function_name and 
                                      self.is_recursive)
                    
                    graph.add_node(FunctionCallNode({
                        "line": node.lineno if hasattr(node, 'lineno') else 0,
                        "code": code_dict,
                        "is_recursive": is_recursive_call
                    }))
                elif isinstance(node, (ast.If, ast.IfExp)):
                    graph.add_node(ConditionalNode({
                        "line": node.lineno,
                        "code": code_dict
                    }))
                elif isinstance(node, ast.Expr):
                    graph.add_node(SimpleStatementNode({
                        "line": node.lineno,
                        "code": code_dict
                    }))
                    
        except Exception as e:
            print(f"Error parsing Python code: {str(e)}")
            
        return graph

    def _analyze_loop_depths(self, tree: ast.AST) -> None:
        """Analyze the entire AST to find maximum loop depth"""
        def visit_node(node, current_depth=0):
            if isinstance(node, (ast.For, ast.While)):
                current_depth += 1
                self.max_loop_depth = max(self.max_loop_depth, current_depth)
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, current_depth)
        
        visit_node(tree)

    def _get_loop_depth(self, node: ast.AST) -> int:
        """Get the nesting depth of a specific loop node"""
        depth = 1
        parent = node
        
        while True:
            found_parent = False
            for potential_parent in ast.walk(ast.parse(self.current_code)):
                for child in ast.iter_child_nodes(potential_parent):
                    if isinstance(child, ast.AST) and ast.dump(child) == ast.dump(parent):
                        if isinstance(potential_parent, (ast.For, ast.While)):
                            depth += 1
                        parent = potential_parent
                        found_parent = True
                        break
                if found_parent:
                    break
            if not found_parent:
                break
        
        return depth

    def to_dict(self, code: str) -> Dict:
        self.current_code = code
        lines = code.split('\n')
        code_dict = {}
        current_indent = 0
        parent_lines = []

        for i, line in enumerate(lines, 1):
            indent = len(line) - len(line.lstrip())
            stripped_line = line.strip()
            
            if stripped_line:
                if indent > current_indent:
                    parent_lines.append(i - 1)
                elif indent < current_indent:
                    while parent_lines and indent <= current_indent:
                        parent_lines.pop()
                        current_indent -= 4

                code_dict[i] = {
                    'line': stripped_line,
                    'indent': indent,
                    'parent': parent_lines[-1] if parent_lines else None
                }
                current_indent = indent

        return code_dict

    def identify_node_type(self, line: str) -> str:
        try:
            node = ast.parse(line).body[0]
            if isinstance(node, (ast.For, ast.While)):
                return "loop"
            elif isinstance(node, ast.Call):
                return "function_call"
            elif isinstance(node, (ast.If, ast.IfExp)):
                return "conditional"
            else:
                return "simple_statement"
        except:
            return "simple_statement"
