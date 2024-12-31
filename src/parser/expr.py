from dataclasses import dataclass
from abc import ABC, abstractmethod
from scanner import Token


# Interfaces
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

    @abstractmethod
    def visit_variable_expr(self, expr: "Variable"):
        pass

    @abstractmethod
    def visit_assign_expr(self, expr: "Assign"):
        pass

    @abstractmethod
    def visit_logical_expr(self, expr: "Logical"):
        pass


# Implementations
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


@dataclass
class Variable(Expr):
    name: Token

    def accept(self, visitor: Visitor):
        return visitor.visit_variable_expr(self)


@dataclass
class Assign(Expr):
    name: Token
    value: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_assign_expr(self)


@dataclass
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_logical_expr(self)
