import ast, sys, argparse, json, uuid

def verify_python_compatibility():
    if not hasattr(ast, 'unparse'):
        raise RuntimeError("This program requires Python 3.9+ (ast.unparse not available)")

def parse_source_file(source_path):
    '''
        Parses the source file and generates a mapping of all statements to their line numbers.
        This is used for visual mapping of the design onto the implementation.

        Each statement is represented as a dictionary with the following keys:
        - type: The type of the AST node (e.g., If, For, FunctionDef, etc.)
        - uid: A unique identifier for the statement (used for mapping)
        - start_line: The line number where the statement starts
        - end_line: The line number where the statement ends
        - source: The source code of the statement (for debugging purposes)

        For nodes with a body (e.g., If, For, FuncDef), the line number of the first child
        is used to determine the end line of the parent statement, since the parent statement
        may span multiple lines. Then the parent statement is processed to remove any new lines
        that may be present in the source code, and the end line is adjusted accordingly.

        Example:
        1. def run(
        2.     self
        3. ):
        4.
        5. 
        6.
        7.     exampleFunctionCall()

        In this case, the function definition starts at line 1 and the first node in the body starts
        at line 7. So it first identifies lines 1 to 6 as the source of the function def, and then it
        starts at line 6 and works backwards to remove new lines until the first non-empty line is reached.
        This then isolates the line numbers as lines 1 to 3 and this is used by the visual mapping.

        Using these sections, the UI maps the design onto the implementation visually. Specific statements
        are also highlighted to indicate the variables that they need to log and those variables are
        mapped onto participants. Then this information is used to instrument the code resulting in a
        execution trace that can be transformed into the behavior of the design.
    '''
    with open(source_path, "r") as source_file:
        source_code = source_file.read()

    lines = source_code.splitlines()
    
    mapping = []

    for node in ast.walk(ast.parse(source_code)):
        source = ""
        if hasattr(node, "lineno") and isinstance(node, ast.stmt):
            if "body" in node._fields and isinstance(node.body, list) and len(node.body) > 0:
                # Start at line of first node in body and work backwards to remove new lines
                # until first non-empty line is reached.
                endLine = node.body[0].lineno - 1
                for count in range(endLine, node.lineno, -1):
                    if lines[count - 1].strip() != "":
                        break
                    else:
                        endLine -= 1
                source = lines[node.lineno - 1: endLine]
                endLineNo = endLine
            elif isinstance(node, ast.stmt):
                source = ast.get_source_segment(source_code, node)
                endLineNo = node.end_lineno 

            mapping.append({
                "type": type(node).__name__,
                "uid": str(uuid.uuid4()),
                "start_line": node.lineno,
                "end_line": endLineNo,
                "source": source,
            })
                
    with open("mapping.json", "w") as mapping_file:
        json.dump(mapping, mapping_file, indent=4)
    

def main(argv):
    '''
        Main entry point for the program. Parses command line arguments and 
        initiates the source file parsing.
    '''
    verify_python_compatibility()

    args_parser = argparse.ArgumentParser(
        description="Generates a mapping of all statements to their line numbers in a Python source file for visual mapping."
    )

    args_parser.add_argument(
        "source",
        type=str,
        help="Path to source file"
    )

    args = args_parser.parse_args(argv[1:])
    source_path = args.source
    parse_source_file(source_path)


if "__main__" == __name__:
    sys.exit(main(sys.argv))