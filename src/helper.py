import ast

def getBehaviorLogStmt(behaviorName):
    return ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="adli", ctx=ast.Load()),
                attr="logBehavior",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=behaviorName)
            ],
            keywords=[]
        )
    )


def getParticipantLogStmt(behaviorName, participantName):
    return ast.Expr(
        value = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="adli", ctx=ast.Load()),
                attr="logParticipant",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=behaviorName),
                ast.Constant(value=participantName),
                ast.Name(id=participantName, ctx=ast.Load())
            ],
            keywords=[]
        )
    )


def injectTryExcept(nodeBody, behaviorName):
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
            ast.Constant(value=behaviorName)
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

    return ast.Try(
        body=nodeBody,
        handlers=[handler],
        orelse=[],
        finalbody=[]
    )