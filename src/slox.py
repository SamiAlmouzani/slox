import sys
from scanner import Scanner
from typing import List
from tokens import Token
from Parser import Parser
from expr import Expr
from ast_printer import AstPrinter
from interpreter import Interpreter

class Slox:

    had_error: bool = False
    had_runtime_error: bool = False

    interpreter: Interpreter = Interpreter()
    
    def run(self, source: str) -> None:
        scanner: Scanner = Scanner(source)
        toks: List[Token] = scanner.scan_tokens()
        parser: Parser = Parser(toks)        
        expr: Expr = parser.parse()

        if self.had_error: return

        self.interpreter.interpret(expr)
        # print(AstPrinter().print(expr))

    def run_file(self, path: str) -> None:
        with open(path, "rb") as f:
            file_content: bytes = f.read()
        self.run(file_content.decode(sys.getdefaultencoding()))
        if self.had_error:         sys.exit(65)
        if self.had_runtime_error: sys.exit(70)
        

    def run_prompt(self) -> None:
        """runs interactive prompt"""
        while True:
            print("> ", end="")
            line: str = str(input())
            if line is None:
                break
            self.run(line)
            self.had_error = False

