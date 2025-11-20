import sys
import os
import scanner
import parser


def scanner_parser(input_file):
    scanner.setup(input_file)

    while True:  # scan file
        out = scanner.gettoken()

        # parse token from `out`
        # end parse

        if out["token"] == "EndofFile":
            break


if os.path.isdir(sys.argv[1]):  # scan and parse all files in directory
    for file in os.listdir(sys.argv[1]):
        scanner_parser(f"{sys.argv[1]}/{file}")
else:  # scan and parse file
    scanner_parser(sys.argv[1])
