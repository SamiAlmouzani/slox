from abc import ABC, abstractmethod
from tokens import Token

class Expr(ABC):
   @abstractmethod
   def accept(self, visitor) -> None:
       pass

class Binary(Expr):
   def __init__(self, left: Expr, operator: Token, right: Expr):
      self.left: Expr = left
      self.operator: Token = operator
      self.right: Expr = right

   def accept(self, visitor):
       return visitor.visit_binary_expr(self)

class Grouping(Expr):
   def __init__(self, expression: Expr):
      self.expression: Expr = expression

   def accept(self, visitor):
       return visitor.visit_grouping_expr(self)

class Literal(Expr):
   def __init__(self, value):
      self.value = value

   def accept(self, visitor):
       return visitor.visit_literal_expr(self)

class Unary(Expr):
   def __init__(self, operator: Token, right: Expr):
      self.operator: Token = operator
      self.right: Expr = right

   def accept(self, visitor):
       return visitor.visit_unary_expr(self)

class Visitor(ABC):
   @abstractmethod
   def visit_binary_expr(self, expr) -> str:
      pass
   @abstractmethod
   def visit_grouping_expr(self, expr) -> str:
      pass
   @abstractmethod
   def visit_literal_expr(self, expr) -> str:
      pass
   @abstractmethod
   def visit_unary_expr(self, expr) -> str:
      pass

