from abc import ABC, abstractmethod
from dataclasses import dataclass
from parser.expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor"):
        pass


@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_expression_stmt(self)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_print_stmt(self)


class Visitor(ABC):
    @abstractmethod
    def visit_expression_stmt(self, stmt: "Expression"):
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: "Print"):
        pass
