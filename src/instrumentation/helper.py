import ast

def injectTryExcept(tree):
    '''
        Injects try except structure around the given tree.
        Injects header into file and imports adli logger instance.
    '''
    handler = ast.ExceptHandler(
        type=ast.Name(id='Exception', ctx=ast.Load()),
        name='e',
        body=[
            ast.parse("adli.logException(e)"),
            ast.parse("raise"),
        ]
    )

    mainTry = ast.Try(
        body=tree.body,
        handlers=[handler],
        orelse=[],
        finalbody=[]
    )

    mod = ast.Module(body=[mainTry], type_ignores=[])
    return mod