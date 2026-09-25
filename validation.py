def validate_tables(tables):
    valid_tables = {}

    for table_name, table in tables.items():

        # Every table must have a primary key
        if table["pk"] is None:
            print(
                f"Error: table {table_name} "
                f"has no primary key"
            )
            continue

        # PK must actually appear in the listed columns
        if table["pk"] not in table["columns"]:
            print(
                f"Error: primary key "
                f"{table['pk']} not found "
                f"in {table_name}"
            )
            continue

        valid = True

        for fk in table["fks"]:

            # FK column must exist locally
            if fk["column"] not in table["columns"]:
                print(
                    f"Error: foreign key column "
                    f"{fk['column']} not found "
                    f"in table {table_name}"
                )

                valid = False
                continue

            ref_table = fk["ref_table"]
            ref_column = fk["ref_column"]

            # Referenced table must exist
            if ref_table not in tables:
                print(
                    f"Error: referenced table "
                    f"{ref_table} does not exist "
                    f"for foreign key "
                    f"{table_name}.{fk['column']}"
                )

                valid = False
                continue

            # Referenced column must exist
            if (
                ref_column
                not in tables[ref_table]["columns"]
            ):
                print(
                    f"Error: referenced column "
                    f"{ref_column} does not exist "
                    f"in table {ref_table}"
                )

                valid = False

        if valid:
            valid_tables[
                table_name
            ] = table

    return valid_tables