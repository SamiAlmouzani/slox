import sys
from pathlib import Path

def define_ast(output_dir: str, base_name: str, types: list[str]):
    path: str = output_dir + "/" + base_name + ".py"
    
    with open(path, "w", encoding="utf-8") as f:
        f.write("class " + base_name + ":\n")
        f.write("   " + "pass\n\n")
        for type in types:
            class_name: str = type.split(":")[0].strip()
            fields: str = type.split(":")[1].strip()
            define_type(f, base_name, class_name, fields)

def define_type(f, base_name: str, class_name: str, field_list: str):
    f.write("class " + class_name + "(" + base_name + "):\n")
    f.write("   " + "def __init__(self, " + field_list + "):\n")
    fields: list[str] = field_list.split(", ") 
    for field in fields:
        f.write("      " + "self." + field + " = " + field + "\n")
    f.write("\n")

# Main Code    
if len(sys.argv) != 2:
    sys.stderr("Usage: generate_ast <output directory>")
    sys.exit()
output_dir: str = sys.argv[1]
define_ast(output_dir, "Expr", [
    "Binary   : left, operator, right",
    "Grouping : expression",
    "Literal  : value",
    "Unary    : operator, right"
])
