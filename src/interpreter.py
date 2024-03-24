from expr import Visitor, Expr, Literal, Grouping, Binary, Unary
from token_type import TokenType
from runterror import RunTError
from logger import Logger

class Interpreter(Visitor):

    def visit_literal_expr(self, expr: Literal):
        return expr.value
    
    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)
    
    def visit_unary_expr(self, expr: Unary) -> str:
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG:
                return not self.is_truthy(right)
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)

        # Unreachable 
        return None

    def visit_binary_expr(self, expr: Binary) -> str:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG_EQUAL: 
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL: 
                return self.is_equal(left, right)
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(left)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)

                raise RunTError(expr.operator, "Operands must be two numbers or two strings.")

        # Unreachable 
        return None

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        
        raise RunTError(operator, "Operands must be numbers.") 

    def is_equal(a, b) -> bool:
        if a == None and b == None: 
            return True
        if a == None:
            return False
        
        return a == b

    def is_truthy(object) -> bool:
        if object == None: return False
        if isinstance(object, bool): return bool(object)

    def evaluate(self, expr: Expr):
        return expr.accept(self)
    
    def interpret(self, expr: Expr):
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except RunTError as error:
            Logger.runtime_error(error)          
    
    def stringify(self, object) -> str:
        if object == None:
            return "nil"
        
        if isinstance(object, float):
            text: str = str(object)
            if text.endswith(".0"):
                text = text[0: len(text) - 2]
            
            return text
        
        return str(object)