from tokens import Token

class RunTError(RuntimeError):

    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.TOKEN = token