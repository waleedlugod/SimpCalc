from enum import Enum

idx = 0
input_file = ""
output_file = ""

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
    "ENDIF": "Endif",
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
    global output_file
    global idx
    global input_file_name
    input_file = open(filename).read()
    output_file = open(filename.replace("input", "output_scan"), "w")
    idx = 0
    input_file_name = filename


def gettoken():
    global idx
    token = ""
    lexeme = ""
    error = ""
    state = States.NONE

    if idx < len(input_file):
        c = input_file[idx]

        # ignore whitespace
        if c == " " or c == "\t" or c == "\n":
            idx += 1
            return gettoken()

        # ignore comments
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
            if idx + 1 < len(input_file) and input_file[idx + 1] == "=":
                lexeme += input_file[idx + 1]
                idx += 1
            elif c == "!":
                if idx + 1 < len(input_file):
                    lexeme += input_file[idx + 1]
                idx += 1
                state = States.Error
                error_reason = "Illegal character/character sequence"

        elif c == "*":
            if input_file[idx + 1] == "*":
                lexeme += input_file[idx + 1]
                idx += 1

        elif c == '"':  # string
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

        elif c.isalpha() or c == "_":  # identifier
            state = States.Identifier
            while idx + 1 < len(input_file):
                c = input_file[idx + 1]
                if c.isalpha() or c.isdigit() or c == "_":
                    lexeme += c
                    idx += 1
                else:
                    break

        elif c.isdigit():  # number
            num_state = 4
            state = States.Error
            error_reason = "Invalid number format"
            while idx + 1 < len(input_file):
                c = input_file[idx + 1]
                match num_state:
                    case 4:
                        if c.isdigit():
                            lexeme += c
                            idx += 1
                        elif c == ".":
                            lexeme += c
                            idx += 1
                            num_state = 5
                        elif c == "e" or c == "E":
                            lexeme += c
                            idx += 1
                            num_state = 6
                        else:
                            state = States.Number
                            break
                    case 5:
                        lexeme += c
                        idx += 1
                        if c.isdigit():
                            num_state = 9
                        else:
                            state = States.Error
                            break
                    case 6:
                        lexeme += c
                        idx += 1
                        if c.isdigit():
                            num_state = 8
                        elif c == "+" or c == "-":
                            num_state = 7
                        else:
                            state = States.Error
                            break
                    case 7:
                        lexeme += c
                        idx += 1
                        if c.isdigit():
                            num_state = 8
                        else:
                            state = States.Error
                            break
                    case 8:
                        if c.isdigit():
                            lexeme += c
                            idx += 1
                        else:
                            state = States.Number
                            break
                    case 9:
                        if c.isdigit():
                            lexeme += c
                            idx += 1
                        elif c == "e" or c == "E":
                            lexeme += c
                            idx += 1
                            num_state = 6
                        else:
                            state = States.Number
                            break
            else:  # set the correct state when end of file
                if num_state == 4 or num_state == 8 or num_state == 9:
                    state = States.Number

        elif lexeme not in fixed_tokens:  # miscallaneous first input character
            state = States.Error
            error_reason = "Illegal character/character sequence"
        idx += 1

        # format output
        if state == States.NONE:
            token = fixed_tokens[lexeme]
        else:
            token = state.name
            if state == States.Error:
                error = f"Lexical Error: {error_reason}"
            elif state == States.Identifier and lexeme in fixed_tokens:
                token = fixed_tokens[lexeme]
    else:
        token = "EndofFile"

    if token == "EndofFile":
        output_file.write(f"{token}")
    elif token == "Error":
        output_file.write(f"{error} \nError\n")
    else:
        output_file.write(f"{token:<17}{lexeme}\n")

    return {
        "token": token,
        "lexeme": lexeme,
        "error": error,
        "filename": input_file_name,
    }
