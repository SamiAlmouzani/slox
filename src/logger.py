import sys
from tokens import Token
from token_type import TokenType

class Logger:

    def report(self, line: int, where: str, message: str) -> None:
        sys.stderr.write("[line " + str(line) + "] Error" + where + ": " + message)

    def error(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)
        
    def error(self, line: int, message: str) -> None:
        self.report(line, "", message)

