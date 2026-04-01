# Design Instrumentor

> [!NOTE]  
> This repo is in development and currently a simple parser is implemented to enable visual mapping of the design onto the implementation.

This tool plays multiple roles in the design feedback loop. 
- It parses the source code and generates a mapping file that can be used to visually map the design onto the implementation.
- It accepts the mapping and instruments the source with the semantic information need to produce traces that can be semantically transformed. 

This program will be called from the node server and it will provide the necessary metadata to the UI to enable the mapping. It will then be called by the server again when it instruments and executes the code. The resulting execution trace will be automatically debugged by the engine. 

This process will be repeated for multiple languages and it will also be extended to instrument systems. The instrumenter will use CLP logging libraries and the mapping will be extended to include domain specific knowledge about the data to apply domain specific compression.

## Usage

To produce mapping from a python program:
```
python3 instrumenter.py --mode parser <source_path>
```

An example for one of the sample files:
```
python3 instrumenter.py --mode parser sample/FrenchTranslator.py 
```

Output will be saved in the output folder with the name <file_name>_mapping.json.
