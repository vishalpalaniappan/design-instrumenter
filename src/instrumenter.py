import io
import os
import ast
import sys
import json
import shutil
import zipfile
from pathlib import Path
from src.helper import copyFile
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
            behaviorName = func_name[2:] 

        for participantName in args:
            if participantName == "self":
                continue
            node.body.insert(0,getParticipantLogStmt(behaviorName, participantName))
            
        node.body.insert(0,getBehaviorLogStmt(behaviorName))        
        node.body = [injectTryExcept(node.body, behaviorName)]

        return self.generic_visit(node)

def instrument_semantic_information(source, stream = False):
    if stream:
        source_code = sys.stdin.read()
    else:
        with open(source, "r") as source_file:
            source_code = source_file.read()

    package = json.loads(source_code)
            
    script_dir = Path(__file__).resolve().parent
    output_folder = Path(os.path.join(script_dir.parent, "output"))
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

    copyFile(script_dir, output_folder, "LoggingHelper.py")

    if (stream):
        buffer = zip_folder_in_memory(output_folder)
        while True:
            chunk = buffer.read(4096)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()
    else:
        with open(output_folder / "instrumented_output.py", "w") as f:
            f.write(ast.unparse(instrumentedCode))