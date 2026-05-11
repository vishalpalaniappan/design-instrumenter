# Design Instrumentor

This tool instruments a python program to log the semantic information needed for the computable semantic module to determine the semantic validity of the design. 

## Usage

Updates coming soon.

## Background

The semantic information and the chosen convention is as follows:

|   | Type        | Convention           | Description                      | Example                          |
|---|-------------|----------------------|----------------------------------|----------------------------------|
| A | Behavior    | b_`<behavior>`         | The behavior being exhibited.    | def b_acceptName():              |
| B | Argument    | p_arg_`<argument>`     | The arguments into the behavior. | p_arg_name = name                |
| C | Participant | p_pre_`<participant>`  | The pre behavior world state.    | p_pre_basket = basket            |
| D | Participant | p_post_`<participant>` | The post behavior world state.   | p_post_firstLetter = firstLetter |

Example using accept name behavior (argument as input from environment):
```
def b_acceptName():
    name = input("Enter Book Name: ")
    p_arg_name = name
    p_post_name = name
    return name
```

Example using add book to basket behavior:
```
def b_addBookToBasket(book, basket):
    p_pre_book = book
    p_pre_basket = basket
    basket.insert(0, book)
    p_post_basket = basket
    return basket
```

When seen from the design playground in the workbench, this information populates the following fields (I'm using this commit https://github.com/vishalpalaniappan/design-workbench/pull/35/commits/71c82d03ce8e573c2a97ab9f7ccfaafd47b6d73e):

<img width="1282" height="637" alt="image" src="https://github.com/user-attachments/assets/eb4bbe60-5251-4fbd-8ffa-a2e4e0556182" />


Using this information, the engine can compute the post world state using the behavioral script in the semantic model. It then compares the output of the semantic model to the post behavior participant states and determines the semantic validity of the implementation. In addition, through invariants defined in the behavioral script for the participants, the engine is able to identify in what way the world is semantically invalid and use it to predict downstream failures.
