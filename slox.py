import sys
from scanner import Scanner
from typing import List
from tokens import Token

class Slox:

    had_error: bool = False

    def run(self, source: str) -> None:
        scanner: Scanner = Scanner(source)
        tokens: List[Token] = scanner.scan_tokens()
        for token in tokens:
            print(token)

    def run_file(self, path: str) -> None:
        with open(path, "rb") as f:
            file_content: bytes = f.read()
        self.run(file_content.decode(sys.getdefaultencoding()))
        if self.had_error:
            sys.exit(1)

    def run_prompt(self) -> None:
        """runs interactive prompt"""
        while True:
            print("> ", end="")
            line: str = str(input())
            if line is None:
                break
            self.run(line)
            self.had_error = False

