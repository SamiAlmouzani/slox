from expr import Expr, Visitor, Binary, Grouping, Literal, Unary
from tokens import Token
from token_type import TokenType

class AstPrinter(Visitor):
    
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, 
                                 expr.left,
                                 expr.right) 

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", 
                                 expr.expression) 


    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value == None: 
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme,
                                  expr.right) 


    def parenthesize(self, name: str, *exprs: Expr) ->  str:
        out_str = f"({name}"
        for expr in exprs:
            out_str += " "
            out_str += expr.accept(self) 
        out_str += ")"
        return out_str


# testing code
'''
expression: Expr = Binary(
    Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(123)        
    ),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(
        Literal(45.67)
    )
)
print(AstPrinter().print(expression))
'''