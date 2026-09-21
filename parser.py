
def parse_column(column_text):
    column_text = column_text.strip()

    #Primary Key
    if "(pk)" in column_text.lower():
        name = column_text[:column_text.lower().index("(pk)")].strip()

        return {
            "name": name.lower(),
            "is_pk": True,
            "fk": None
        }
    

    #Foreign
    if "(fk:" in column_text.lower():
        name = column_text[:column_text.lower().index("(fk:")].strip()

        start = column_text.lower().index("(fk:") + 4
        end = column_text.index(")", start)

        ref = column_text[start:end].strip()
        ref_table, ref_col = ref.split(".")

        return{
            "name": name.lower(),
            "is_pk": False,
            "fk": {
                "table": ref_table.lower(),
                "column": ref_col.lower()
            }
        }
    
    return{
        "name": column_text.lower(),
        "is_pk": False,
        "fk": None
    }





def parse_table(line):

    line = line.strip()

    if not line:
        return None
    
    open_paren = line.find("(")
    close_paren = line.find(")")

    if open_param == -1 or close_paren == -1:
        raise ValueError(f"Invalid table definition: {line}")
    
    table_name = line[:open_paren].strip().lower()
    columns_text = line[open_paren + 1:close_paren]
    columns = []
    current = ""
    depth = 0

    for char in columns_text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        
        if char == "," and depth == 0:
            columns.append(current.strip())
            current - ""
        else:
            current += char
    
    if current.strip():
        columns.append(current.strip())
    

    parsed_columns = []
    primary_key = None
    foreign_keys = []

    for column_text in columns:
        column = parse_column(column_text)
        parsed_columns.append(column["name"])

        if column["is_pk"]:
            primary_key = column["name"]

        
        if column["fk"] is not None:
            foreign_keys.append({
                "column": column["name"],
                "ref_table": column["fk"]["table"],
                "ref_column": column["fk"]["column"]
            })

    
    return {
        "name": table_name,
        "columns": parsed_columns,
        "pk": primary_key,
        "fks": foreign_keys
    }




def parse_input_file(filename):
    tables = {}

    with open(filename,"r") as file:
        for line_number, line in enumerate(file,start=1):
            line = line.strip()

            if not line:
                continue

            try:
                table = parse_table(line)

                if table is not None:
                    tables[table["name"]] = table
            
            except Exception as error:
                print(f"Erorr on line {line_number}: {error}")
    
    return tables
