import scanner

current = None
input_filename = ""
output_file = ""


def setup(filename):
    global input_filename
    global output_file
    scanner.setup(filename)
    input_filename = filename
    output_file = open(filename.replace("input", "output_parse"), "w")


# Gets the next token based on the given input.
def next_token():
    global current
    current = scanner.gettoken()


# writes out respective errors if token does not match.
def match(expected):
    global current
    if current["token"] == expected:
        next_token()
    else:
        raise Exception(f"Parse Error: {expected} expected.")


# Grammar rules
def Prg():
    global input_filename
    global current
    current = scanner.gettoken()
    try:
        Blk()
        if current["token"] != "EndofFile":
            raise Exception("Parse Error: Unexpected token.")
        else:
            output_file.write(
                f"{input_filename.split('/')[-1]} is a valid SimpCalc program"
            )
    except Exception as e:
        output_file.write(str(e))
        while current["token"] != "EndofFile":
            next_token()


def Blk():
    while current["token"] in ["Identifier", "Print", "If"]:
        Stm()


def Stm():
    if current["token"] == "Identifier":
        next_token()
        match("Assign")
        Exp()
        match("Semicolon")
        output_file.write("Assignment Statement Recognized\n")

    elif current["token"] == "Print":
        next_token()
        match("LeftParen")
        Arg()
        Argfollow()
        match("RightParen")
        match("Semicolon")
        output_file.write("Print Statement Recognized\n")

    elif current["token"] == "If":
        output_file.write("If Statement Begins\n")
        next_token()
        Cnd()
        match("Colon")
        Blk()
        Iffollow()
        output_file.write("If Statement Ends\n")

    else:
        raise Exception(f"Parse Error: Unexpected token.")


def Arg():
    if current["token"] == "String":
        next_token()
    else:
        Exp()


def Argfollow():
    while current["token"] == "Comma":
        match("Comma")
        Arg()


def Iffollow():
    if current["token"] == "Endif":
        match("Endif")
        match("Semicolon")
    elif current["token"] == "Else":
        match("Else")
        Blk()
        match("Endif")
        match("Semicolon")
    else:
        while current["token"] not in ["Endif", "EndofFile"]:
            next_token()
        raise Exception("Parse Error: Incomplete if Statement")


def Cnd():
    Exp()
    if current["token"] not in [
        "LessThan",
        "Equal",
        "GreaterThan",
        "LTEqual",
        "GTEqual",
        "NotEqual",
    ]:
        raise Exception("Parse Error: Missing operator.")
    next_token()
    Exp()


def Exp():
    Trm()
    while current["token"] in ["Plus", "Minus"]:
        next_token()
        Trm()


def Trm():
    Fac()
    while current["token"] in ["Multiply", "Divide"]:
        next_token()
        Fac()


def Fac():
    Lit()
    while current["token"] == "Raise":
        next_token()
        Lit()


def Lit():
    if current["token"] == "Minus":
        next_token()
    Val()


def Val():
    if current["token"] in ["Identifier", "Number"]:
        next_token()
    elif current["token"] == "Sqrt":
        next_token()
        match("LeftParen")
        Exp()
        match("RightParen")
    elif current["token"] == "LeftParen":
        match("LeftParen")
        Exp()
        match("RightParen")
    else:
        raise Exception(f"Parse Error: Unexpected token.")
