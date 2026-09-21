
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
    
    
