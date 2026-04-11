import os
import json
import ast
from src.instrumentation.LogInjector import LogInjector

class SourceInstrumenter(ast.NodeTransformer):
    def __init__(self, mapping_data):
        '''
            Initialize the SourceInstrumenter with the mapping data.
        '''
        self.mapping_data = mapping_data

    def getEntryForNode(self, node):
        '''
            Get the mapping entry for a given AST node.
        '''
        for entry in self.mapping_data:
            if (hasattr(node, "lineno") and hasattr(node, "end_lineno") and 
                node.lineno == entry["start_line"] and node.end_lineno == entry["end_line"]):
                return entry
            
        return None

    def visit(self, node):
        '''
            Override the visit method to inject instrumentation code based on the mapping data.
        '''
        entry = self.getEntryForNode(node)
        if entry:
            print(entry["uid"], type(node).__name__, entry["type"])
            
        self.generic_visit(node) 
        return node

def instrument_semantic_information(source):
    with open(source, "r") as source_file:
        source_code = source_file.read()

    package = json.loads(source_code)

    for file in package:
        stmtIndex = package[file]["statementIndex"]
        source = package[file]["content"]
        injector = LogInjector(stmtIndex)
        new_tree = injector.visit(ast.parse(source))

        with open("./output/instrumented_" + os.path.basename(package[file]["name"]), "w") as instrumented_file:
            instrumented_file.write(ast.unparse(new_tree))