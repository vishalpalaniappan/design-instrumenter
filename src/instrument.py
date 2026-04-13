import io
import sys
import os
import json
import ast
import shutil
import zipfile
from src.instrumentation.LogInjector import LogInjector
from src.instrumentation.helper import injectTryExcept
from pathlib import Path

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

def instrument_semantic_information(source, stream = False):
    if stream:
        source_code = sys.stdin.read()
    else:
        with open(source, "r") as source_file:
            source_code = source_file.read()

    package = json.loads(source_code)

    script_dir = Path(__file__).resolve().parent
    output_folder = os.path.join(script_dir, "temp")
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)

    for file in package:
        stmtIndex = package[file]["statementIndex"]
        source = package[file]["content"]
        injector = LogInjector(stmtIndex)
        new_tree = injector.visit(ast.parse(source))

        importNode = ast.parse("from LoggingHelper import adli").body[0]
        new_tree.body.insert(0, importNode)

        instrumented_file_path = os.path.join(output_folder, os.path.basename(package[file]["name"]))
        with open(instrumented_file_path, "w") as instrumented_file:
            instrumented_file.write(ast.unparse(new_tree))

    src = script_dir / "instrumentation" / "LoggingHelper.py"
    dst = Path(output_folder) / "LoggingHelper.py"

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

    if (stream):
        buffer = zip_folder_in_memory(output_folder)
        while True:
            chunk = buffer.read(4096)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()

    # shutil.rmtree(output_folder, ignore_errors=True)