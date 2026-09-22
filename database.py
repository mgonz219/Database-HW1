import psycopg2



def connect_database():
    try:
        conn = psycopg2.connect(
            dbname = "cosc3380",
            user="dbs18",
            password = "9bCjEmfPXloXXP",
            host="52.22.24.16"
        )

        return conn

    except Exception as error:
        print(f"Database connection failed: {error}")
        return None


def table_exists(conn, table_name):
    query = """
        SELECT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
            AND table_name = %s
            AND table_name = %s
        );
        """
    # might have to chane schema
    
    with conn.cursor() as cursor:
        cursor.execute(query,(table_name,column_name))
        return cursor.fetchone()[0]
    

def validate_database_schema(conn, tables):
    valid_tables = {}

    for table_name, table in tables.items():
        if not table_exists(conn,table_name):
            print(f"Error: table {table_name} does not exist in database")
            continue

        valid = True
    
    for column in table["columns"]:
        if not column_exists(conn, table_name, column):
            print(
                f"Error: column {column} does not exist in table {table_name}"
            )
            valid = False
        
        if valid:
            valid_tables[table_name] = table
        
    return valid_tables