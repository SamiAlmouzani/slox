from tokens import Token
from typing import List
from token_type import TokenType
from logger import Logger

class Scanner:

    tokens: List[tokens] = []

    start: int = 0
    current: int = 0
    line: int = 1

    keywords: dict[str, TokenType] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }
    '''
  static {
    keywords = new HashMap<>();
    keywords.put("and",    AND);
    keywords.put("class",  CLASS);
    keywords.put("else",   ELSE);
    keywords.put("false",  FALSE);
    keywords.put("for",    FOR);
    keywords.put("fun",    FUN);
    keywords.put("if",     IF);
    keywords.put("nil",    NIL);
    keywords.put("or",     OR);
    keywords.put("print",  PRINT);
    keywords.put("return", RETURN);
    keywords.put("super",  SUPER);
    keywords.put("this",   THIS);
    keywords.put("true",   TRUE);
    keywords.put("var",    VAR);
    keywords.put("while",  WHILE);
  }
    '''
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
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                Logger.error(Logger(), self.line, "Unexpected Character.")

    def identifier(self) -> None:
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text: str = self.source[self.start : self.current]
        type: TokenType = self.keywords.get(text)
        if type == None:
            type = TokenType.IDENTIFIER

        self.add_token(type)
    
    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        '''Look for fractional part''' 
        if self.peek() == "." and self.is_digit(self.peek_next()):
            '''Consume the "."'''
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token_helper(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def string(self) -> None:
        while self.peek() != '"' and (not self.is_at_end()):
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            Logger.error(self.line, "Unterminated string.")
            return

        '''the closing ".''' 
        self.advance()
        
        '''Trim the surrounding quotes'''
        value: str = self.source[self.start + 1 : self.current - 1]
        self.add_token_helper(TokenType.STRING, value)

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
    
    def peek_next(self) -> str:
        if (self.current + 1) >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
    
    def is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or (c == "_")
    
    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)
        
    def is_digit(self, c: str) -> bool:
        return c >= "0" and c <= "9" 

    def advance(self) -> str:
        temp = self.current
        self.current += 1
        return self.source[temp]

    def add_token(self, type: TokenType) -> None:
        self.add_token_helper(type, None)
    
    def add_token_helper(self, type: TokenType, literal: any) -> None:
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))
