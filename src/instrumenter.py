import os
import ast
import shutil
from pathlib import Path
from src.helper import getBehaviorLogStmt, getParticipantLogStmt, injectTryExcept

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
        node.body = [injectTryExcept(node.body, behaviorName)]

        return self.generic_visit(node)

def instrument_semantic_information(source, stream = False):

    with open(source, "r") as source_file:
        source_code = source_file.read()

    injector = LogInjector()
    instrumentedCode = injector.visit(ast.parse(source_code))

    importNode = ast.parse("from LoggingHelper import adli").body[0]
    instrumentedCode.body.insert(0, importNode)

    script_dir = Path(__file__).resolve().parent
    output_folder = Path(os.path.join(script_dir.parent, "output"))
    src = script_dir / "LoggingHelper.py"
    dst = output_folder / "LoggingHelper.py"

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

    with open(output_folder / "instrumented_output.py", "w") as f:
        f.write(ast.unparse(instrumentedCode))