import sys

from parser import parse_input_file
from validation import validate_tables
from database import connect_database, validate_database_schema

filename = sys.argv[1]
tables = parse_input_file(filename) 
tables = validate_tables(tables)

conn = connect_database()

if conn is None:
    sys.exit()

tables = validate_database_schema(conn,tables)

for name, table in tables.items():
    print(name, table)

for name, table in tables.items():
    print(name, table)

conn.close()