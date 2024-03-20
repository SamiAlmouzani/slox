import sys

def define_ast(output_dir: str, base_name: str, types: list[str]):
    path: str = output_dir + "/" + base_name.lower() + ".py"
    
    with open(path, "w", encoding="utf-8") as f:
        f.write("from abc import ABC, abstractmethod\n")
        f.write("from tokens import Token\n\n")
        f.write("class " + base_name + "(ABC):\n")
        
        f.write("   @abstractmethod\n" + 
                "   def accept(self, visitor) -> None:\n" + 
                "       pass\n\n")

        # AST classes
        for type in types:
            class_name: str = type.split(":")[0].strip()
            print(f"type: {type}")
            fields_list: str = type.split(":", maxsplit=1)[1].strip()
            print(fields_list)
            # fields: str = type.split(",")[1].strip()
            define_type(f, base_name, class_name, fields_list)


        define_visitor(f, base_name, types)

def define_visitor(f, base_name, types):
    f.write("class Visitor(ABC):\n")
    for type in types:
        type_name: str = type.split(":")[0].strip()
        f.write("   @abstractmethod\n")
        f.write("   def visit_" + type_name.lower() + "_" +  base_name.lower() + "(self, " + base_name.lower() + ") -> str:\n")
        f.write("      pass\n")
    f.write("\n")

def define_type(f, base_name: str, class_name: str, field_list: str):
    f.write("class " + class_name + "(" + base_name + "):\n")
    f.write("   def __init__(self, " + field_list + "):\n")
    fields: list[str] = field_list.split(", ") 

    for field in fields:
        f.write("      self." + field + " = " + field.split(":")[0] + "\n")
    f.write("\n")

    f.write("   def accept(self, visitor):\n")
    f.write("       return visitor.visit_" + class_name.lower() + "_" + base_name.lower() + "(self)\n")
    f.write("\n")


# Main Code    
if len(sys.argv) != 2:
    sys.stderr("Usage: generate_ast <output directory>")
    sys.exit()
output_dir: str = sys.argv[1]
define_ast(output_dir, "Expr", [
    "Binary   : left: Expr, operator: Token, right: Expr",
    "Grouping : expression: Expr",
    "Literal  : value",
    "Unary    : operator: Token, right: Expr"
])
