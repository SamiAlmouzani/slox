import sys
from tokens import Token
from token_type import TokenType
from runterror import RunTError

class Logger:
    had_runtime_error: bool = False
    def __init__(self) -> None:
        pass
    def report(self, line: int, where: str, message: str) -> None:
        sys.stderr.write(f"[line {str(line)}] Error {where}: {message}")

    def error_token(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)

    def error_int(self, line: int, message: str) -> None:
        self.report(line, "", message)
    
    def runtime_error(error: RunTError):
        sys.stderr.write(f"{str(error)}\n[line {error.TOKEN.line}]\n")
        had_runtime_error = True

