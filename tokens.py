from token_type import TokenType

class Token:

   def __init__(self, type: TokenType, lexeme: str, literal: any, line: int) -> None:
      self.type = type
      self.lexeme = lexeme
      self.literal = literal
      self.line = line

   def __str__(self) -> str:
      return self.type + " " + self.lexeme + " " + str(self.literal)