from dataclasses import dataclass
from abc import ABC, abstractmethod
from scanner import Token, TokenType

# Any operation (interpret, resolve, analyze) can apply to any expression (Unary, Binary, etc)
# This is a double dispatch problem: the outcome depends on operation and expression


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor"):
        pass


class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: "Binary"):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: "Grouping"):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: "Literal"):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: "Unary"):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor: Visitor):
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expr(self)


# Concrete visitors
class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary):
        return (
            f"({expr.operator.lexeme} {self.print(expr.left)} {self.print(expr.right)})"
        )

    def visit_grouping_expr(self, expr: Grouping):
        return f"(group {self.print(expr.expression)})"

    def visit_literal_expr(self, expr: Literal):
        return str(expr.value) if expr.value else "nil"

    def visit_unary_expr(self, expr: Unary):
        return f"({expr.operator.lexeme} {self.print(expr.right)})"


e = Binary(
    Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(Literal(45.67)),
)

printer = AstPrinter()
print(printer.print(e))
