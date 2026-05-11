# Design Instrumenter

This tool instruments a python program to log the semantic information needed for the computable semantic module to determine the semantic validity of the implementation. The implementation is structured such that the semantically relevant information is observable directly from its Abstract Syntax Tree (AST). The convention used in the implementation to mark the semantically relevant information and some examples are provided below.

In the current workflow, this tool is used by the workbench when the user executes the program in the playground. The program is instrumented, executed and the resulting log file is ingested and automaticaly debugged in the engine.

## Usage

Since this program is intended to be used by the workbench, I've added the workflow directly into this repo to use the program.

The design files are placed in the `designs` folder and the node script will load them from there.

To run the instrumenter using an engine file:
```shell
node node/instrumentationTest.js lib_man_no_invariant.dal
```

> [!NOTE]  
> The structured needed for instrumenting a python file locally exists but only `instrumenter_stream` mode is currently supported. I left the instrument mode in to give myself flexibility in the future to expand.

The node script itself invokes the `instrumenter_stream` mode using the following script:

```shell
python3 design_instrumenter.py instrumenter_stream
```

The source code is read from the design file and streamed to the instrumentation program using stdin and the output is read back through stdout.

## Background

The semantic information and the chosen convention is as follows:

|   | Type        | Convention           | Description                      | Example                          |
|---|-------------|----------------------|----------------------------------|----------------------------------|
| A | Behavior    | b_`<behavior>`         | The behavior being exhibited.    | def b_acceptName():              |
| B | Argument    | p_arg_`<argument>`     | The arguments into the behavior. | p_arg_name = name                |
| C | Participant | p_pre_`<participant>`  | The pre behavior world state.    | p_pre_basket = basket            |
| D | Participant | p_post_`<participant>` | The post behavior world state.   | p_post_firstLetter = firstLetter |

Example using accept name behavior and corresponding behavioral script:
```python
def b_acceptName():
    name = input("Enter Book Name: ")
    p_arg_name = name
    p_post_name = name
    return name
```

```
pre:
    require name input

transform:
    validate transformation

post:
    require name

next:
    select createBook
```

Example using add book to basket behavior and corresponding behavioral script:
```python
def b_addBookToBasket(book, basket):
    p_pre_book = book
    p_pre_basket = basket
    basket.insert(0, book)
    p_post_basket = basket
    return basket
```

```
pre:
    require basket
    require book

transform:
    insert book basket [] 0
    remove book
    validate transformation

post:
    require basket

next:
    select getChoice
```

When seen from the design playground in the workbench, this information populates the following fields:

<img width="1282" height="637" alt="image" src="https://github.com/user-attachments/assets/eb4bbe60-5251-4fbd-8ffa-a2e4e0556182" />

Note: The image above was gathered using this [commit][workbench-commit]. I will be making changes, so please apply the same logic to the latest version of the playground.

Using this information, the engine can compute the post world state using the behavioral script in the semantic model. It then compares the output of the semantic model to the observed post behavior world state and determines the semantic validity of the implementation. In addition, through invariants defined in the behavioral script, the engine is able to identify in what way the world state is semantically invalid and use it to predict downstream failures.

# Providing feedback

You can use GitHub issues to [report a bug][bug-report] or [request a feature][feature-req].

[bug-report]: https://github.com/vishalpalaniappan/design-instrumenter/issues
[feature-req]: https://github.com/vishalpalaniappan/design-instrumenter/issues
[workbench-commit]: https://github.com/vishalpalaniappan/design-workbench/pull/35/commits/71c82d03ce8e573c2a97ab9f7ccfaafd47b6d73e