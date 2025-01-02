from typing import List
from scanner import Token
from parser.expr import (
    Call,
    Expr,
    Binary,
    Grouping,
    Unary,
    Literal,
    Assign,
    Logical,
    Variable,
    Visitor as ExprVisitor,
)
from parser.stmt import (
    Return,
    Stmt,
    Print,
    Expression,
    Block,
    Var,
    If,
    While,
    Function,
    Visitor as StmtVisitor,
)
from enum import Enum, auto


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver(ExprVisitor, StmtVisitor):
    """
    Visit all nodes int the AST and resolve all variable references.
    Resolving means finding the depth of the scope in which the variable is declared.
    This prevents dynamic scoping overwriting variables in outer scopes.
    """

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE

    def resolve(self, statements: List[Stmt]):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_function(self, function: Function, type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if not self.scopes:
            return

        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.interpreter.error(
                name, "Variable with this name already declared in this scope."
            )

        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes:
            return

        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr: Variable, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def resolve_stmt(self, stmt: Stmt):
        stmt.accept(self)

    def resolve_expr(self, expr: Expr):
        expr.accept(self)

    def visit_block_stmt(self, stmt: Block):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_expression_stmt(self, stmt: Expression):
        self.resolve_expr(stmt.expression)

    def visit_function_stmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: If):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve_stmt(stmt.else_branch)

    def visit_print_stmt(self, stmt: Print):
        self.resolve_expr(stmt.expression)

    def visit_return_stmt(self, stmt: Return):
        if self.current_function == FunctionType.NONE:
            self.interpreter.error(stmt.keyword, "Cannot return from top-level code.")
        if stmt.value is not None:
            self.resolve_expr(stmt.value)

    def visit_var_stmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)

    def visit_while_stmt(self, stmt: While):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)

    def visit_assign_expr(self, expr: Assign):
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: Binary):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_call_expr(self, expr: Call):
        self.resolve_expr(expr.callee)
        for argument in expr.arguments:
            self.resolve_expr(argument)

    def visit_grouping_expr(self, expr: Grouping):
        self.resolve_expr(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        pass

    def visit_logical_expr(self, expr: Logical):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_unary_expr(self, expr: Unary):
        self.resolve_expr(expr.right)

    def visit_variable_expr(self, expr: Variable):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            self.interpreter.pylox.resolver_error(
                expr.name, "Cannot read local variable in its own initializer."
            )
        self.resolve_local(expr, expr.name)
