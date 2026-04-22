import io
import os
import ast
import sys
import json
import shutil
import zipfile
from pathlib import Path
from src.helper import injectTryExcept
from src.helper import getBehaviorLogStmt
from src.helper import getParticipantLogStmt

def zip_folder_in_memory(folder_path: str):
    '''
        Zips the contents of a folder in memory so that
        it can be streamed to the client without having to
        write the zip file to disk.
    '''
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(full_path, folder_path)
                zf.write(full_path, rel_path)

    buffer.seek(0)
    return buffer

class LogInjector(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        func_name = node.name
        args = [arg.arg for arg in node.args.args]

        # Behavior name convention is b_<behavior_name>
        if not func_name.startswith("b_"):
            return self.generic_visit(node)
        else:            
            self.behaviorName = func_name[2:] 
            
        node.body.insert(0,getBehaviorLogStmt(self.behaviorName))        
        node.body = [injectTryExcept(node.body, self.behaviorName)]

        return self.generic_visit(node)

    def visit_Assign(self, node):
        if (isinstance(node.targets[0], ast.Name)):
            if node.targets[0].id.startswith("p_pre"):
                name = node.targets[0].id.split('_')[-1]
                return [
                    getParticipantLogStmt(self.behaviorName, ast.unparse(node.value), "pre"),
                    self.generic_visit(node)
                ]
            elif node.targets[0].id.startswith("p_post"):
                name = node.targets[0].id.split('_')[-1]
                return [
                    getParticipantLogStmt(self.behaviorName, ast.unparse(node.value), "post"),
                    self.generic_visit(node)
                ]
        return self.generic_visit(node)
    

def instrument_semantic_information(source, stream = False):
    if stream:
        source_code = sys.stdin.read()
    else:
        with open(source, "r") as source_file:
            source_code = source_file.read()

    package = json.loads(source_code)
            
    script_dir = Path(__file__).resolve().parent
    output_folder = Path(os.path.join(script_dir, "output"))
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)

    for file in package:
        if not package[file]["name"].endswith(".py"):
            continue
        source = package[file]["content"]
        injector = LogInjector()
        instrumentedCode = injector.visit(ast.parse(source))

        importNode = ast.parse("from LoggingHelper import adli").body[0]
        instrumentedCode.body.insert(0, importNode)

        instrumented_file_path = os.path.join(output_folder, os.path.basename(package[file]["name"]))
        with open(instrumented_file_path, "w") as instrumented_file:
            instrumented_file.write(ast.unparse(instrumentedCode))

    src = script_dir / "LoggingHelper.py"
    dst = output_folder / "LoggingHelper.py"
    shutil.copy2(src, dst)

    if (stream):
        buffer = zip_folder_in_memory(output_folder)
        while True:
            chunk = buffer.read(4096)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()

    