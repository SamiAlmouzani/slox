from tokens import Token
from typing import List
from token_type import TokenType
from logger import Logger

class Scanner:

    tokens: List[tokens] = []

    start: int = 0
    current: int = 0
    line: int = 1

    def __init__(self, source: str) -> None:
        self.source = source

    def scan_tokens(self) -> List[tokens]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c: str = self.advance()
        if c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif c == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
        elif c == "/":
            if self.match("/"):
                '''A comment goes until the end of the line.'''
                while (self.peek() != "\n") and (not self.is_at_end()):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == " " or c == "\r" or c == "\t":
            pass
        elif c == "\n":
            self.line += 1
        else:
            Logger.error(Logger(), self.line, "Unexpected Character.")
    
    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def advance(self) -> str:
        temp = self.current
        self.current += 1
        return self.source[temp]

    def add_token(self, type: TokenType) -> None:
        self.add_token_helper(type, None)
    
    def add_token_helper(self, type: TokenType, literal: any) -> None:
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))
