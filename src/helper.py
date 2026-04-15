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