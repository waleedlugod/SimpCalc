import sys
import os
import parser


def scanner_parser(input_file):
    parser.setup(input_file)
    parser.Prg()


if os.path.isdir(sys.argv[1]):  # is input a directory?
    # scan and parse all input files
    for file in os.listdir(sys.argv[1]):
        if "input" in file:
            scanner_parser(f"{sys.argv[1]}/{file}")
elif "input" in sys.argv[1]:  # is input a file?
    scanner_parser(sys.argv[1])
