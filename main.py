import sys
import os
import scanner


def write_to_scan_file(out, scan_file):
    if out["token"] == "EndofFile":
        scan_file.write(f"{out['token']}")
    elif out["token"] == "Error":
        scan_file.write(f"{out['error']} \nError\n")
    else:
        scan_file.write(f"{out['token']:<17}{out['lexeme']}\n")


def scanner_parser(input_file):
    scan_file = open(input_file.replace("input", "output_scan"), "w")
    parse_file = open(input_file.replace("input", "output_parse"), "w")

    scanner.setup(input_file)

    while True:  # scan file
        out = scanner.gettoken()
        write_to_scan_file(out, scan_file)

        # parse token from `out`
        # end parse

        if out["token"] == "EndofFile":
            break


if os.path.isdir(sys.argv[1]):  # scan and parse all files in directory
    for file in os.listdir(sys.argv[1]):
        scanner_parser(f"{sys.argv[1]}/{file}")
else:  # scan and parse file
    scanner_parser(sys.argv[1])
