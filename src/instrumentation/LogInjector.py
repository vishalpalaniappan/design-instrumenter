import ast

def is_in_map(node, mapping_data):
    '''
        Check if the given AST node is present in the mapping data.
    '''
    for entry in mapping_data:
        if (not hasattr(node, "lineno") or  not hasattr(node, "end_lineno")):
            continue

        if (not (node.lineno == entry["_start_line"])):
            continue

        if("_behaviorId" in entry and entry["_behaviorId"]):
            return entry
    
    return False

class LogInjector(ast.NodeTransformer):

    def __init__(self, mapping):
        self.mapping = mapping

    def visit(self, node):
        self.entry = is_in_map(node, self.mapping)
        if isinstance(node, ast.stmt) and self.entry:
            method = getattr(self, f"visit_{node.__class__.__name__}", None)
            if method is not None:
                return method(node)

        return self.generic_visit(node)

    
    def visit_Expr(self, node):
        new_node = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="print", ctx=ast.Load()),
                args=[ast.Constant(value=self.entry["_behaviorId"])],
                keywords=[]
            )
        )
        return [new_node, self.generic_visit(node)]

    def visit_If(self, node):
        return node

    def visit_For(self, node):
        return node

    def visit_While(self, node):
        return node

    def visit_FunctionDef(self, node):
        return node
