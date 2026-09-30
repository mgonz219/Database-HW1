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
        cursor.execute(
            query,
            (table_name,)
        )

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
            (
                table_name,
                column_name
            )
        )

        result = cursor.fetchone()

    return result[0]


def get_primary_key_columns(conn, table_name):
    query = """
SELECT kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
   AND tc.table_schema = kcu.table_schema
   AND tc.table_name = kcu.table_name
WHERE tc.constraint_type = 'PRIMARY KEY'
  AND tc.table_schema = 'public'
  AND tc.table_name = %s
ORDER BY kcu.ordinal_position;
"""

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            (table_name,)
        )

        rows = cursor.fetchall()

    return [
        row[0]
        for row in rows
    ]


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

        actual_pk = get_primary_key_columns(
            conn,
            table_name
        )

        if len(actual_pk) == 0:
            print(
                f"Error: table {table_name} "
                f"has no primary key in database"
            )
            valid = False

        elif len(actual_pk) > 1:
            print(
                f"Error: table {table_name} "
                f"has a composite primary key; "
                f"case not considered"
            )
            valid = False

        elif table["pk"] != actual_pk[0]:
            print(
                f"Error: primary key {table['pk']} "
                f"does not match database primary key "
                f"{actual_pk[0]} for table {table_name}"
            )
            valid = False

        if valid:
            valid_tables[table_name] = table

    return valid_tables
