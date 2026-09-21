def validate_tables(tables):
    valid_tables = {}

    for table_name, table  in tables.items():

        if table["pk"] is None:
            print(f"Error: table {table_name} has no primary key")
            continue

        if table["pk"] not in table["columns"]:
            print(f"Erorr: primary key {table['pk']} not found in {table_name}")
            continue
            
        valid = True

        for fk in table["fks"]:

            # Local FK column must exist
            if fk["column"] not in table["columns"]:
                print(
                    f"Error: foreign key column {fk['column']} "
                    f"not found in table {table_name}"
                )
                valid = False
                continue

            ref_table = fk["ref_table"]
            ref_column = fk["ref_column"]

            # Referenced table must exist
            if ref_table not in tables:
                print(
                    f"Error: referenced table {ref_table} "
                    f"does not exist for foreign key "
                    f"{table_name}.{fk['column']}"
                )
                valid = False
                continue

            # Referenced column must exist
            if ref_column not in tables[ref_table]["columns"]:
                print(
                    f"Error: referenced column {ref_column} "
                    f"does not exist in table {ref_table}"
                )
                valid = False

        if valid:
            valid_tables[table_name] = table

    return valid_tables