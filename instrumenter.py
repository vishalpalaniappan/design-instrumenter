import ast, sys, argparse
from src.parser import parse_source_file
from src.instrumenter import instrument_semantic_information

def verify_python_compatibility():
    if not hasattr(ast, 'unparse'):
        raise RuntimeError("This program requires Python 3.9+ (ast.unparse not available)")

def main(argv):
    '''
        Main entry point for the program. Parses command line arguments and 
        initiates the source file parsing.
    '''
    verify_python_compatibility()

    args_parser = argparse.ArgumentParser(description="Generates a statement mapping from a python program.")
    subparsers = args_parser.add_subparsers(
        dest="mode", 
        help="Mode of operation (currently only parser and parser_stream)",
        required=True
    )

    file_parser = subparsers.add_parser("parser")
    file_parser.add_argument(
        "--source", 
        required=True,
        help="Path to source file in parser mode."
    )

    subparsers.add_parser("parser_stream")


    file_parser = subparsers.add_parser("instrument")
    file_parser.add_argument(
        "--source",
        required=True,
        help="Path to source file in instrumenter mode."
    )
    file_parser.add_argument(
        "--mapping",
        required=True,
        help="Path to mapping file in instrumenter mode."
    )

    args = args_parser.parse_args(argv[1:])
    if (args.mode == "parser"):
        parse_source_file(args.source, stream=False)
    elif (args.mode == "parser_stream"):
        parse_source_file(None, stream=True)
    elif (args.mode == "instrument"):
        instrument_semantic_information(args.source, args.mapping)
    else:
        print(f"Unknown or missing mode: {args.mode}. Supported modes: parser, parser_stream, and instrument", file=sys.stderr)
        return 1
        
    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))