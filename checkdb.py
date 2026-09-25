import sys

from parser import parse_input_file
from validation import validate_tables
from database import connect_database, validate_database_schema


def main():
    if len(sys.argv) < 2:
        print("Usage: python checkdb.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]

    # Parse the input 
    tables = parse_input_file(filename)

    # Validate the information from the input file
    tables = validate_tables(tables)

    # Connect to database
    conn = connect_database()

    if conn is None:
        sys.exit(1)

    try:
        tables = validate_database_schema(conn, tables)

        # Temporary output while building/testing
        for name, table in tables.items():
            print(name, table)

    finally:
        conn.close()


if __name__ == "__main__":
    main()