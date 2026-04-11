import os
import json
import ast
from src.instrumentation.LogInjector import LogInjector

def instrument_semantic_information(source):
    with open(source, "r") as source_file:
        source_code = source_file.read()

    package = json.loads(source_code)

    for file in package:
        stmtIndex = package[file]["statementIndex"]
        source = package[file]["content"]
        injector = LogInjector(stmtIndex)
        new_tree = injector.visit(ast.parse(source))

        importNode = ast.parse("from LoggingHelper import adli").body[0]
        new_tree.body.insert(0, importNode)

        with open("./output/instrumented_" + os.path.basename(package[file]["name"]), "w") as instrumented_file:
            instrumented_file.write(ast.unparse(new_tree))