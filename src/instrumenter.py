import os
import json
import ast

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
            return node
            
        self.generic_visit(node) 
        return node


def instrument_semantic_information(source, mapping):
    with open(source, "r") as source_file:
        source_code = source_file.read()

    with open(mapping, "r") as mapping_file:
        mapping_data = json.load(mapping_file)


    tree = ast.parse(source_code)
    instrumenter = SourceInstrumenter(mapping_data)
    instrumented_tree = instrumenter.visit(tree)
    instrumented_code = ast.unparse(instrumented_tree)

    filename = os.path.basename(source)
    with open("./output/instrumented_" + filename, "w") as instrumented_file:
        instrumented_file.write(instrumented_code)
