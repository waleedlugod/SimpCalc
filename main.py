import scanner

filename = "test_input.txt"
output_file = open(filename.replace("input", "output_scan_test"), "w")
scanner.setup(filename)
while True:
    out = scanner.gettoken()
    output_file.write(f"{out['token']:<17}{out['lexeme']}\n")
    if out["token"] == "EndOfFile":
        break
