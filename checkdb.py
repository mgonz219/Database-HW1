import os
import sys

from parser import parse_input_file
from validation import validate_tables
from database import connect_database, validate_database_schema
from referential import check_referential_integrity
from normalization import checkNorm

def writeOutput(filename, ri_results, norm_results):
    input_name = os.path.basename(filename)
    input_stem = os.path.splittext(input_name)[0]

    output_name = f"refintnorm-{input_stem}.txt"

    dbRIValid = all(
        res == "Y" for res in ri_results.values()
    )

    dbNormValid = all(
        res == "Y" for res in norm_results.values()
    )

    allSorted = sorted(set(ri_results.keys()) | set(norm_results.keys()))

    with open(output_name, "w") as file:
        file.write(f"{'':<8}{'ref.integrity':<16}{'normalized':<10}\n")
        for table_name in allSorted:
            ri = ri_results.get(table_name, "N")
            norm = norm_results.get(table_name, "N")

            file.write(f"{table_name:<8}{ri:^13}{norm:^16}\n")
        file.write("\n")
        file.write(f"DB referential integrity: {'Y' if dbRIValid else 'N'}\n")
        file.write(f"DB normalized: {'Y' if dbNormValid else 'N'}\n")

    return output_name


def write_ri_output(filename, ri_results):
    input_name = os.path.basename(filename)
    input_stem = os.path.splitext(input_name)[0]

    output_name = f"refint-{input_stem}.txt"

    db_valid = all(
        result == "Y"
        for result in ri_results.values()
    )

    with open(output_name, "w") as file:
        file.write("referential integrity\n")

        for table_name in sorted(ri_results):
            file.write(
                f"{table_name} {ri_results[table_name]}\n"
            )

        file.write(
            f"\nDB referential integrity: "
            f"{'Y' if db_valid else 'N'}\n"
        )

    return output_name


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 checkdb.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]

    tables = parse_input_file(filename)
    tables = validate_tables(tables)

    conn = connect_database()

    if conn is None:
        sys.exit(1)

    try:
        tables = validate_database_schema(
            conn,
            tables
        )

        with open("checkdb.sql", "w") as file:
            file.write(
                f"-- Input file: {filename}\n\n"
            )

        ri_results = check_referential_integrity(
            conn,
            tables
        )

        norm_results = checkNorm(
            conn,
            tables
        )

        output_file = writeOutput(
            filename,
            ri_results,
            norm_results
        )

        # output_file = write_ri_output(
        #     filename,
        #     ri_results
        # )

        print(
            f"Output written to {output_file}"
        )

    finally:
        conn.close()


if __name__ == "__main__":
    main()