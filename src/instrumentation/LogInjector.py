import ast
from src.instrumentation.helper import injectTryExcept

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

    def getLogStmts (self):
        behaviorLog =ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="adli", ctx=ast.Load()),
                    attr="logBehavior",
                    ctx=ast.Load()
                ),
                args=[
                    ast.Constant(value=self.entry["_uid"]),
                    ast.Constant(value=self.entry["_behaviorId"])
                ],
                keywords=[]
            )
        )

        variableLogs = []
        for participant in self.entry["_participants"]:
            variableLogs.append(ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="adli", ctx=ast.Load()),
                        attr="logVariable",
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Constant(value=self.entry["_uid"]),
                        ast.Constant(value=self.entry["_behaviorId"]),
                        ast.Constant(value=participant["participantName"]),
                        ast.Name(id=participant["variableName"], ctx=ast.Load())
                    ],
                    keywords=[]
                )
            ))

        return [behaviorLog, variableLogs]

    def visit(self, node):
        self.entry = is_in_map(node, self.mapping)

        '''
            If a node is a stmt and doesn't have a body, simply
            log the behavior before the statement.

            If it has a body, then depending on the type of statement,
            we have to log the behavior at the right place. 
        '''
        if isinstance(node, ast.stmt) and self.entry:

            if "body" not in node._fields:
                injected_node = self.getLogStmts()
                
                entry = self.entry
                return injectTryExcept([*injected_node, self.generic_visit(node)], entry)
            else:
                method = getattr(self, f"visit_{node.__class__.__name__}", None)
                if method is not None:
                    return method(node)

        return self.generic_visit(node)

    def visit_If(self, node):
        if not self.entry:
            return self.generic_visit(node)
        
        injected_node = self.getLogStmts()
        entry = self.entry
        return injectTryExcept([*injected_node, self.generic_visit(node)], entry)

    def visit_For(self, node):
        if not self.entry:
            return self.generic_visit(node)
        
        injected_node = self.getLogStmts()
        node.body.append(injected_node)
        entry = self.entry
        return injectTryExcept([*injected_node, self.generic_visit(node)], entry)

    def visit_While(self, node):
        if not self.entry:
            return self.generic_visit(node)
        
        injected_node = self.getLogStmts()
        node.body.append(injected_node)        
        entry = self.entry
        return injectTryExcept([*injected_node, self.generic_visit(node)], entry)