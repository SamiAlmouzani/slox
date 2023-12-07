import sys
from slox import Slox

if __name__ == "__main__":
    prog = Slox()
    if len(sys.argv) > 2:
        sys.stderr("Usage lox [script]")
        sys.exit()
    elif len(sys.argv) == 2:
        print("run_file mode")
        prog.run_file(sys.argv[1])
    else:
        prog.run_prompt()
