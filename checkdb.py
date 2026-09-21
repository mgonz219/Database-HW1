import sys

from parser import parse_input_file
from validation import validate_tables

filename = sys.argv[1]
tables = parse_input_file(filename) 

tables = validate_tables(tables)

for name, table in tables.items():
    print(name, table)