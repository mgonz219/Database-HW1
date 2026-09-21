from parser import parse_input_file

tables = parse_input_file("testcases/testcase1.txt") 
#place holder path ^ 


for name, table in tables.items():
    print(name, table)