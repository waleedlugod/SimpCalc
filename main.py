import scanner

filename = "test_input.txt"
output_file = open(filename.replace("input", "output_scan_test"), "w")
scanner.setup(filename)
while True:
    out = scanner.gettoken()
    if out["token"] == "Error":
        output_file.write(f"{out['error']}\nError")
    else:
        output_file.write(f"{out['token']:<17}{out['lexeme']}")

    if out["token"] == "EndOfFile":
        break
    else:
        output_file.write("\n")
