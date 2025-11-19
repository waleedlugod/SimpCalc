from enum import Enum

idx = 0
input_file = ""

fixed_tokens = {
    ":=": "Assign",
    ";": "Semicolon",
    ":": "Colon",
    ",": "Comma",
    "(": "LeftParen",
    ")": "RightParen",
    "+": "Plus",
    "-": "Minus",
    "*": "Multiply",
    "/": "Divide",
    "**": "Raise",
    "<": "LessThan",
    "=": "Equal",
    ">": "GreaterThan",
    "<=": "LTEqual",
    ">=": "GTEqual",
    "!=": "NotEqual",
    "PRINT": "Print",
    "IF": "If",
    "ELSE": "Else",
    "ENDIF": "EndIf",
    "SQRT": "Sqrt",
    "AND": "And",
    "OR": "Or",
    "NOT": "Not",
}


class States(Enum):
    NONE = 0
    Error = 1
    Identifier = 2
    Number = 3
    String = 4
    Comment = 5


def setup(filename):
    global input_file
    global idx
    input_file = open(filename).read()
    idx = 0


def gettoken():
    global idx
    token = ""
    lexeme = ""
    build = ""
    state = States.NONE

    if idx < len(input_file):
        c = input_file[idx]
        while c == " " or c == "\t" or c == "\n":
            idx += 1
            c = input_file[idx]
        lexeme = c
        if c == ":" or c == "<" or c == ">" or c == "!":
            if input_file[idx + 1] == "=":
                lexeme += input_file[idx + 1]
                idx += 1
            elif c == "!":
                state = States.Error
        elif c == "*":
            if input_file[idx + 1] == "*":
                lexeme += input_file[idx + 1]
                idx += 1
        elif lexeme not in fixed_tokens:
            state = States.Error

        if state == States.Error:
            token = States.Error.name
        elif state == States.NONE:
            token = fixed_tokens[lexeme]
    else:
        token = "EndOfFile"

    idx += 1
    return {"token": token, "lexeme": lexeme}
