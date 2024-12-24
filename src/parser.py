from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List
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


class Parser:
    tokens: List[Token]
    current: int = 0

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def match(self, *types: TokenType):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def check(self, type: TokenType):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens.get(self.current)

    def previous(self):
        return self.tokens.get(self.current - 1)

    def comparison(self):
        expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        raise self.error(self.peek(), "Expect expression.")

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        print(f"[line {token.line}] Error: {message}")
        return ParseError()


class ParseError(Exception):
    pass
