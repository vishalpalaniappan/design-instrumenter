import json, ast

class SourceInstrumenter(ast.NodeTransformer):
    def __init__(self, mapping_data):
        self.mapping_data = mapping_data

    def visit(self, node):
        for entry in self.mapping_data:
            if (hasattr(node, "lineno") and hasattr(node, "end_lineno") and 
                node.lineno == entry["start_line"] and node.end_lineno == entry["end_line"]):
                print_stmt = f'print("Executing statement: {entry["uid"]}")'
                print(print_stmt)
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
