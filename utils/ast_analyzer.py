import ast

class SecurityASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.has_string_formatting_in_sql = False
        self.is_valid_ast = True
        
    def visit_Call(self, node):
        # Look for cursor.execute() type calls with string formatting
        if hasattr(node.func, 'attr') and node.func.attr == 'execute':
            if node.args and isinstance(node.args[0], (ast.JoinedStr, ast.BinOp)): # f-strings or % formatting
                self.has_string_formatting_in_sql = True
            elif node.args and isinstance(node.args[0], ast.Call) and hasattr(node.args[0].func, 'attr') and node.args[0].func.attr == 'format':
                self.has_string_formatting_in_sql = True
        self.generic_visit(node)

def analyze_python_code(code: str) -> dict:
    """Parses code to AST and runs basic security checks."""
    try:
        tree = ast.parse(code)
        visitor = SecurityASTVisitor()
        visitor.visit(tree)
        return {
            "valid_python": True,
            "has_sql_injection_pattern": visitor.has_string_formatting_in_sql,
            "error": None
        }
    except SyntaxError as e:
        return {
            "valid_python": False,
            "has_sql_injection_pattern": False,
            "error": str(e)
        }
