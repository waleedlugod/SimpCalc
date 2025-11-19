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
    error = ""
    state = States.NONE

    if idx < len(input_file):
        c = input_file[idx]

        while c == " " or c == "\t" or c == "\n":
            idx += 1
            c = input_file[idx]

        if c == "/" and idx + 1 < len(input_file) and input_file[idx + 1] == "/":
            while c != "\n" and idx + 1 < len(input_file):
                idx += 1
                c = input_file[idx]
            else:
                idx += 1
                return gettoken()

        error_reason = ""
        lexeme = c
        if c == ":" or c == "<" or c == ">" or c == "!":
            if input_file[idx + 1] == "=":
                lexeme += input_file[idx + 1]
                idx += 1
            elif c == "!":
                state = States.Error
                error_reason = "Illegal character/character sequence"
        elif c == "*":
            if input_file[idx + 1] == "*":
                lexeme += input_file[idx + 1]
                idx += 1
        elif c == '"':
            state = States.Error
            error_reason = "Unterminated string"
            while idx + 1 < len(input_file):
                c = input_file[idx + 1]
                if c == "\n":
                    break
                lexeme += c
                idx += 1
                if c == '"':
                    state = States.String
                    break
        elif c.isalpha() or c == "_":
            state = States.Error
            error_reason = "Illegal character/character sequence"
            while idx + 1 < len(input_file):
                c = input_file[idx + 1]
                if c.isalpha() or c.isdigit() or c == "_":
                    lexeme += c
                    idx += 1
                else:
                    state = States.Identifier
                    break
        elif lexeme not in fixed_tokens:
            state = States.Error
            error_reason = "Illegal character/character sequence"
        idx += 1

        if state == States.NONE:
            token = fixed_tokens[lexeme]
        else:
            token = state.name
            if state == States.Error:
                error = f"Lexical Error: {error_reason}"
    else:
        token = "EndOfFile"

    return {"token": token, "lexeme": lexeme, "error": error}
