from abc import ABC, abstractmethod
from dataclasses import dataclass
from parser.expr import Expr
from scanner import Token


# Interfaces
class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor"):
        pass


class Visitor(ABC):
    @abstractmethod
    def visit_expression_stmt(self, stmt: "Expression"):
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: "Print"):
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: "Var"):
        pass

    @abstractmethod
    def visit_block_stmt(self, stmt: "Block"):
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt: "If"):
        pass


# Implementations
@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_expression_stmt(self)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_print_stmt(self)


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_var_stmt(self)


@dataclass
class Block(Stmt):
    statements: list[Stmt]

    def accept(self, visitor: Visitor):
        return visitor.visit_block_stmt(self)


@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

    def accept(self, visitor: Visitor):
        return visitor.visit_if_stmt(self)
