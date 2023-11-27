"""
Main file for executing things
"""
import sys

def run(source: str) -> None:
    print(source)
def run_file(path: str) -> None:
    """Gets File Data and Runs"""
    with open(path, "rb") as f:
        file_content: bytes = f.read()
    run(file_content.decode(sys.getdefaultencoding()))

if len(sys.argv) > 2:
    print("Usage lox [script]")
    sys.exit()
elif len(sys.argv) == 2:
    run_file(sys.argv[1])
else:
    # TODO: run_prompt should go here
    print("This should run_prompt, however it hasn't been implemented yet")