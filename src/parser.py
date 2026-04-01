
import sys, os, ast, uuid, json
from pathlib import Path

NO_MAP = (
    "FunctionDef",
    "AsyncFunctionDef",
    "ClassDef"
)

def iterate_statements(node):
    '''
        Structured traversal of AST nodes to yield statements in the
        order they appear in the source code. This is used to
        generate a mapping of statements for visual representation.
    '''
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.stmt):
            yield child
        yield from iterate_statements(child)

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

    try:
        with open(source_path, "r") as source_file:
            source_code = source_file.read()
    except FileNotFoundError:
        print(f"Source file not found: {source_path}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Error reading source file: {e}", file=sys.stderr)
        return

    mapping = []
    lines = source_code.splitlines()
    tree = ast.parse(source_code)

    for node in iterate_statements(tree):

        if hasattr(node, "lineno") and type(node).__name__ not in NO_MAP:

            if "body" in node._fields and isinstance(node.body, list) and len(node.body) > 0:
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
                "source_path": source_path,
                "uid": str(uuid.uuid4()),
                "start_line": node.lineno,
                "end_line": endLineNo,
                "source": source,
            })
                
    # File Name
    nameWExtenstion = Path(source_path).name
    name = os.path.splitext(nameWExtenstion)[0] 

    # Output path (create folder if it doesn't exist)
    path = Path("./output")
    path.mkdir(parents=True, exist_ok=True)
    output_path = path / f"{name}_mapping.json"

    with open(output_path, "w") as mapping_file:
        json.dump(mapping, mapping_file, indent=4)

    print(f"Mapping generated for {source_path} and saved to {output_path}")