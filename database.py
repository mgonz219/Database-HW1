import psycopg2

from db_config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


def connect_database():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        return conn

    except Exception as error:
        print(f"Database connection failed: {error}")
        return None


def table_exists(conn, table_name):
    query = """
SELECT EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name = %s
);
"""

    with conn.cursor() as cursor:
        cursor.execute(query, (table_name,))
        result = cursor.fetchone()

    return result[0]


def column_exists(conn, table_name, column_name):
    query = """
SELECT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = %s
      AND column_name = %s
);
"""

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (table_name, column_name)
        )

        result = cursor.fetchone()

    return result[0]


def validate_database_schema(conn, tables):
    valid_tables = {}

    for table_name, table in tables.items():

        if not table_exists(conn, table_name):
            print(
                f"Error: table {table_name} "
                f"does not exist in database"
            )
            continue

        valid = True

        for column in table["columns"]:

            if not column_exists(
                conn,
                table_name,
                column
            ):
                print(
                    f"Error: column {column} "
                    f"does not exist in table {table_name}"
                )

                valid = False

        if valid:
            valid_tables[table_name] = table

    return valid_tables