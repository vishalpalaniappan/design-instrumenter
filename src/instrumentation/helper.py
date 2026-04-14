import ast

def injectTryExcept(node, entry):
    '''
        Injects try except structure around the given tree.
        Injects header into file and imports adli logger instance.
    '''
    logExceptionCall=ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="adli", ctx=ast.Load()),
            attr="logFailure",
            ctx=ast.Load()
        ),
        args=[
            ast.Constant(value=entry["_uid"]),
            ast.Constant(value=entry["_behaviorId"])
        ],
        keywords=[]
    )
    

    handler = ast.ExceptHandler(
        type=ast.Name(id='Exception', ctx=ast.Load()),
        name='e',
        body=[
            ast.Expr(value=logExceptionCall),
            ast.parse("raise"),
        ]
    )

    mainTry = ast.Try(
        body=node,
        handlers=[handler],
        orelse=[],
        finalbody=[]
    )
    
    return mainTry