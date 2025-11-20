import sys
import os
import parser


def scanner_parser(input_file):
    parser.setup(input_file)
    parser.Prg()


if os.path.isdir(sys.argv[1]):  # scan and parse all files in directory
    for file in os.listdir(sys.argv[1]):
        if "input" in file:
            scanner_parser(f"{sys.argv[1]}/{file}")
elif "input" in sys.argv[1]:  # scan and parse file
    scanner_parser(sys.argv[1])
