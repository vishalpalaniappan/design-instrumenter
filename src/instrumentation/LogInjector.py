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
                        ast.Constant(value=participant["participantName"]),
                        ast.Name(id=participant["variableName"], ctx=ast.Load())
                    ],
                    keywords=[]
                )
            ))

        return [variableLogs, behaviorLog]

    def visit(self, node):
        self.entry = is_in_map(node, self.mapping)


        '''
            If a node is a stmt and doesn't have a body, simply
            log the behavior before the statement.

            If it has a body, then depending on the type of statement,
            we have to log the behavior at the right place. For example,
            with while loops, you want to log the behavior.

            I am using my tried and tested approach for now but I think
            if I think some more I will find a simpler way. Anyway, in the
            next stage, I will log the variables and I will log them before
            the statement is executed because it shows the participant value
            that the behavior used.

            This is different than my dynamic trace logger where I log the
            variables after the statement.
        '''
        if isinstance(node, ast.stmt) and self.entry:

            if "body" not in node._fields:
                new_node = self.getLogStmts()
                return [new_node, self.generic_visit(node)]
            else:
                method = getattr(self, f"visit_{node.__class__.__name__}", None)
                if method is not None:
                    return method(node)

        return self.generic_visit(node)

    def visit_If(self, node):
        if not self.entry:
            return self.generic_visit(node)
        
        new_node = self.getLogStmts()
        return [new_node, self.generic_visit(node)]

    def visit_For(self, node):
        if not self.entry:
            return self.generic_visit(node)
        
        new_node = self.getLogStmts()
        node.body.append(new_node)
        
        return [new_node, self.generic_visit(node)]

    def visit_While(self, node):
        if not self.entry:
            return self.generic_visit(node)
        
        new_node = self.getLogStmts()
        node.body.append(new_node)
        
        return [new_node, self.generic_visit(node)]