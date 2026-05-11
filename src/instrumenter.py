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
from src.helper import getArgumentLogStmt

BEHAVIOR_PREFIX = "b_"
PARTICIPANT_PRE_PREFIX = "p_pre_"
PARTICIPANT_POST_PREFIX = "p_post_"
ARGUMENT_PREFIX = "p_arg_"

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
    
    def __init__(self):
        super().__init__()
        self.behaviorName = None

    def visit_FunctionDef(self, node):
        '''
            If the function name is prefixed with "b_" then it is considered
            a behavior and the relevant log statements are injected.

            The convention for behavior names is:
            - Behavior: b_<behavior_name>        
        '''
        func_name = node.name

        if not func_name.startswith(BEHAVIOR_PREFIX):
            return self.generic_visit(node)
        
        # Set behavior name before visiting body of function
        self.behaviorName = func_name[len(BEHAVIOR_PREFIX):]

        # Visit body of function to inject logs for participants and arguments
        node = self.generic_visit(node)
            
        # Inject behavior log statement and try except block to log failures
        node.body.insert(0,getBehaviorLogStmt(self.behaviorName))        
        node.body = [injectTryExcept(node.body, self.behaviorName)]

        # Reset behavior name after visiting body of function to avoid logging
        # participants and arguments for non-behavior assign statements
        self.behaviorName = None

        return node

    def visit_Assign(self, node):
        '''
            If the assign statement is prefixed with a keyword then it is replaced
            with the relevant log statement. 

            The convention is as follows:
            - Pre-behavior participant: p_pre_<participant_name>
            - Post-behavior participant: p_post_<participant_name>
            - Argument value: p_arg_<argument_name>

            These conventions are used when implementing the design and allow the
            user to specify which information the instrumenter should log.        
        '''
        
        if (isinstance(node.targets[0], ast.Name) and self.behaviorName is not None):

            if node.targets[0].id.startswith(PARTICIPANT_PRE_PREFIX):
                name = node.targets[0].id[len(PARTICIPANT_PRE_PREFIX):]
                return getParticipantLogStmt(self.behaviorName, name, "pre", node.value)
            
            elif node.targets[0].id.startswith(PARTICIPANT_POST_PREFIX):
                name = node.targets[0].id[len(PARTICIPANT_POST_PREFIX):]
                return getParticipantLogStmt(self.behaviorName, name, "post", node.value)
            
            elif node.targets[0].id.startswith(ARGUMENT_PREFIX):
                name = node.targets[0].id[len(ARGUMENT_PREFIX):]
                return getArgumentLogStmt(self.behaviorName, name, node.value)
            
        return self.generic_visit(node)
    

def instrument_semantic_information():
    '''
        Instruments the source code with logging statements to log semantic information during runtime. 

        TODO: Extend this to support folders. Currently, all the programs have to be in the same folder.
    '''
    source_code = sys.stdin.read()

    '''
        The package is a dictionary which holdes the files and
        their content. The workbench streams this automatically in
        the server.
    '''
    package = json.loads(source_code)
            
    script_dir = Path(__file__).resolve().parent
    output_folder = Path(os.path.join(script_dir, "output"))
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)

    for file in package:
        if not package[file]["name"].endswith(".py"):
            continue
        source = package[file]["content"]

        # Create injector and inject logs in the source code
        injector = LogInjector()
        instrumentedCode = injector.visit(ast.parse(source))

        # Inject statement to import semanticLogger for use during runtime
        importNode = ast.parse("from LoggingHelper import semanticLogger").body[0]
        instrumentedCode.body.insert(0, importNode)

        # Write the instrumented code to the output folder
        instrumented_file_path = os.path.join(output_folder, os.path.basename(package[file]["name"]))
        with open(instrumented_file_path, "w") as instrumented_file:
            instrumented_file.write(ast.unparse(instrumentedCode))

    src = script_dir / "LoggingHelper.py"
    dst = output_folder / "LoggingHelper.py"
    shutil.copy2(src, dst)

    # Stream output
    buffer = zip_folder_in_memory(output_folder)
    while True:
        chunk = buffer.read(4096)
        if not chunk:
            break
        sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.flush()

    