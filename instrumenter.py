import ast, sys, argparse
from src.parser import parse_source_file

def verify_python_compatibility():
    if not hasattr(ast, 'unparse'):
        raise RuntimeError("This program requires Python 3.9+ (ast.unparse not available)")

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
        "--mode",
        type=str,
        help="Mode of operation (currently only parser, instrumenter in future)"
    )

    args_parser.add_argument(
        "source",
        type=str,
        help="Path to source file"
    )

    args = args_parser.parse_args(argv[1:])
    mode = args.mode

    if (mode == "parser"):
        parse_source_file(args.source, stream=False)
    elif (mode == "parser_stream"):
        parse_source_file(args.source, stream=True)
    else:
        print(f"Unknown or missing mode: {mode}. Supported modes: parser and parser_stream", file=sys.stderr)
        return 1
        
    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))