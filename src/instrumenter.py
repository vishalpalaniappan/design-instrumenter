import ast
from src.helper import getBehaviorLogStmt, getParticipantLogStmt

class LogInjector(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        func_name = node.name
        args = [arg.arg for arg in node.args.args]

        # Behavior name convention is b_<behavior_name>
        if not func_name.startswith("b_"):
            return self.generic_visit(node)
        else:            
            behaviorName = func_name[2:] 

        for participantName in args:
            if participantName == "self":
                continue
            node.body.insert(0,getParticipantLogStmt(behaviorName, participantName))
            
        node.body.insert(0,getBehaviorLogStmt(behaviorName))

        return self.generic_visit(node)

def instrument_semantic_information(source, stream = False):

    with open(source, "r") as source_file:
        source_code = source_file.read()

    injector = LogInjector()
    instrumentedCode = injector.visit(ast.parse(source_code))

    # ast.fix_missing_locations(instrumentedCode)

    with open("output/instrumented_output.py", "w") as f:
        f.write(ast.unparse(instrumentedCode))