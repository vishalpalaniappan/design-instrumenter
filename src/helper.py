import ast

def getBehaviorLogStmt(behaviorName):
    '''
        Logs the execution of a behavior with the given name.
         - behaviorName: The name of the behavior to log.
         - Returns: An AST node representing the logging statement.
    '''
    return ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="semanticLogger", ctx=ast.Load()),
                attr="logBehavior",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=behaviorName)
            ],
            keywords=[]
        )
    )

def getArgumentLogStmt(behaviorName, argumentName, argumentValue):
    '''
        Logs the value of an argument for a behavior with the given name.
         - behaviorName: The name of the behavior to log.
         - argumentName: The name of the argument to log.
         - argumentValue: The value of the argument to log.
         - Returns: An AST node representing the logging statement.
    '''
    return ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="semanticLogger", ctx=ast.Load()),
                attr="logArgument",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=behaviorName),
                ast.Constant(value=argumentName),
                argumentValue
            ],
            keywords=[]
        )
    )

def getParticipantLogStmt(behaviorName, participantName, participantType, participantValue):
    '''
        Logs the value of a participant for a behavior with the given name.
         - behaviorName: The name of the behavior to log.
         - participantName: The name of the participant to log.
         - participantType: The type of the participant to log.
         - participantValue: The value of the participant to log.
         - Returns: An AST node representing the logging statement.
    '''
    return ast.Expr(
        value = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="semanticLogger", ctx=ast.Load()),
                attr="logParticipant",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=behaviorName),
                ast.Constant(value=participantName),
                ast.Constant(value=participantType),
                participantValue
            ],
            keywords=[]
        )
    )


def injectTryExcept(nodeBody, behaviorName):
    '''
        Wraps the provided node body in a try-except block to log failures.
        In this tool, this is used to inject try-except around function body.
         - nodeBody: The body of the program to wrap.
         - behaviorName: The name of the behavior to log in case of failure.
         - Returns: An AST node representing the try-except block.
    '''
    logExceptionCall=ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="semanticLogger", ctx=ast.Load()),
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