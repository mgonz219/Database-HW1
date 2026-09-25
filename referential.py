def log_sql(query):
    with open("checkdb.sql", "a") as file:
        file.write(query.strip())
        file.write("\n\n")


def check_foreign_key(conn, table_name):
    ...

    