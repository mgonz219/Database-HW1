def log_sql(query, comment):
    with open("checkdb.sql", "a") as file:
        file.write(f"-- {comment}\n\n")
        file.write(query.strip())
        file.write("\n\n")

def checkFDViol(conn, table_name, colB, colC, totalRows):
    #Check if B -> C forms non trivial repeating functional dependency

    fdCheckQuery = f"""
SELECT
    COUNT(DISTINCT {colB}),
    COUNT(DISTINCT ({colB}, {colC}))
FROM {table_name};
"""

    log_sql(fdCheckQuery, f"Comparing distinct {colB} count vs distinct ({colB}, {colC}) pair count")

    with conn.cursor() as cursor:
        cursor.execute(fdCheckQuery)
        distinctB, distinctBC = cursor.fetchone()

        if (distinctB == distinctBC) and (distinctB < totalRows):
            return True

        return False

def checkTableNorm(conn, table_name, table_info):
    #Y if normalized, N if non-trivial repeating FD exists
    pk = table_info["pk"]
    columns = table_info["columns"]

    nonPKCols = [
        col for col in columns if col != pk
    ]

    #0 or 1 non PK cols cannot have non PK FDs
    if len(nonPKCols) < 2:
        return "Y"

    count_query = f"""
SELECT COUNT(*)
FROM {table_name};
"""

    log_sql(count_query, f"total row count")

    try:
        with conn.cursor() as cursor:
            cursor.execute(count_query)
            totalRows = cursor.fetchone()[0]
    except Exception as error:
        conn.rollback()
        print(f"Error counting rows for {table_name}: {error}")
        return "N"

    #0 or 1 rows normalized
    if totalRows <= 1:
        return "Y"

    #Test all pairs
    for colB in nonPKCols:
        for colC in nonPKCols:
            if colB == colC:
                continue

            #check violation
            violation = checkFDViol(conn, table_name, colB, colC, totalRows)
            if violation:
                return "N"

    return "Y"
    




def checkNorm(conn, tables):
    #3NF/BCNF normalization across validiated tables
        
    results = {}

    for table_name in sorted(tables.keys()):
        table_info = tables[table_name]
        results[table_name] = checkTableNorm(conn, table_name, table_info)

    return results