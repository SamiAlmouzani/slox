"""
Main file for executing things
"""
import sys

class Scanner:
    def __init__(self, source) -> None:
        self.source = source

def run(source: str) -> None:
    print(source)

def run_file(path: str) -> None:
    """Gets File Data and Runs"""
    with open(path, "rb") as f:
        file_content: bytes = f.read()
    run(file_content.decode(sys.getdefaultencoding()))

def run_prompt() -> None:
    while(True):
        print("> ", end="")
        line: str = str(input())
        if line is None:
            break
        run(line)
if len(sys.argv) > 2:
    print("Usage lox [script]")
    sys.exit()
elif len(sys.argv) == 2:
    run_file(sys.argv[1])
else:
    run_prompt()
    # TODO: run_prompt should go here
    # print("This should run_prompt, however it hasn't been implemented yet")
    
