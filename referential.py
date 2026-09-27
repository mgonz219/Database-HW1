def log_sql(query):
    with open("checkdb.sql", "a") as file:
        file.write(query.strip())
        file.write("\n\n")


def check_foreign_key(conn, table_name, fk):
    fk_column = fk["column"]
    ref_table = fk["ref_table"]
    ref_column = fk["ref_column"]

    table_count_query = f"""
SELECT COUNT(*)
FROM {table_name};
"""

    join_count_query = f"""
SELECT COUNT(*)
FROM {table_name}
JOIN {ref_table}
    ON {table_name}.{fk_column} = {ref_table}.{ref_column};
"""

    log_sql(table_count_query)
    log_sql(join_count_query)

    with conn.cursor() as cursor:
        cursor.execute(table_count_query)
        table_count = cursor.fetchone()[0]

        cursor.execute(join_count_query)
        join_count = cursor.fetchone()[0]

    return table_count == join_count


def check_referential_integrity(conn, tables):
    results = {}

    for table_name, table in tables.items():

        if not table["fks"]:
            results[table_name] = "Y"
            continue

        table_valid = True

        for fk in table["fks"]:
            fk_valid = check_foreign_key(
                conn,
                table_name,
                fk
            )

            if not fk_valid:
                table_valid = False

        if table_valid:
            results[table_name] = "Y"
        else:
            results[table_name] = "N"

    return results