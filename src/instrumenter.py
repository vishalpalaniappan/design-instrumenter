import ast


class LogInjector(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        name = node.name
        args = [arg.arg for arg in node.args.args]

        print("\nName:", name)
        print("args:", args)
        return self.generic_visit(node)

def instrument_semantic_information(source, stream = False):

    with open(source, "r") as source_file:
        source_code = source_file.read()

    injector = LogInjector()
    injector.visit(ast.parse(source_code))