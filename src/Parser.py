from tokens import Token
from expr import Expr, Binary, Unary, Literal, Grouping
from token_type import TokenType
from logger import Logger

class Parser:
    class ParseError(RuntimeError): pass

    tokens: list[Token] = None
    current: int = 0

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def parse(self) -> Expr:
        try:
            return self.expression()
        except RuntimeError:
            return None
            
    def expression(self) -> Expr:
        return self.equality()
    
    def equality(self) -> Expr:
        expr: Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr: Expr = Binary(expr, operator, right)
        
        return expr
   
    def comparison(self) -> Expr:
        expr: Expr =  self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr: Expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr: Expr =  self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr: Expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr: Expr =  self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr: Expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE): return Literal(False) 
        if self.match(TokenType.TRUE): return Literal(True) 
        if self.match(TokenType.NIL): return Literal(None) 

        if self.match(TokenType.NUMBER, TokenType.STRING): return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect Expression.")


    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type): return self.advance()
        raise self.error(self.peek(), message)


    def check(self, type: TokenType) -> bool:
        if self.is_at_end(): return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end(): self.current += 1
        return self.previous()
        
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def error(self, token: Token, message: str) -> ParseError:
        Logger.error(token, message)
        return self.ParseError()
    
    def synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            t: TokenType = TokenType()

            if self.previous().type == t.SEMICOLON: return

            ttype: TokenType = self.peek().type

            if   ttype == t.CLASS: return 
            elif ttype == t.FUN: return 
            elif ttype == t.VAR: return 
            elif ttype == t.IF: return 
            elif ttype == t.WHILE: return 
            elif ttype == t.PRINT: return 
            elif ttype == t.RETURN: return 

        self.advance()