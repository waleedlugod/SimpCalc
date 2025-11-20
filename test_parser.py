import scanner
import parser

scanner.setup("samples/sample_input_9.txt")
parser.next_token()
try:
    parser.Prg()
except Exception as e:
    print(e) 
