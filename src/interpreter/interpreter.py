from typing import List
from scanner import Token, TokenType
from parser.expr import (
    Expr,
    Binary,
    Grouping,
    Unary,
    Literal,
    Assign,
    Logical,
    Visitor as ExprVisitor,
)
from parser.stmt import (
    Stmt,
    Print,
    Expression,
    Block,
    Var,
    If,
    While,
    Visitor as StmtVisitor,
)
from environment import Environment
from error import RuntimeError


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, pylox):
        self.pylox = pylox
        self.environment = Environment()

    def interpret(self, statements: List[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as e:
            self.pylox.runtime_error(e)
            return None

    def stringify(self, value: object):
        if value is None:
            return "nil"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        return stmt.accept(self)

    def execute_block(self, statements: List[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_stmt(self, stmt: Expression):
        self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var_stmt(self, stmt: Var):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_while_stmt(self, stmt: While):
        while self.evaluate(stmt.condition):
            self.execute(stmt.body)

    def visit_if_stmt(self, stmt: If):
        if self.evaluate(stmt.condition):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)

    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_logical_expr(self, expr: Logical):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if left:
                return left
        else:
            if not left:
                return left
        return self.evaluate(expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right
        if expr.operator.type == TokenType.BANG:
            return not right

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        if expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(
                expr.operator, "Operands must be two numbers or two strings."
            )
        if expr.operator.type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return left / right
        if expr.operator.type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        if expr.operator.type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        if expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        if expr.operator.type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        if expr.operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        if expr.operator.type == TokenType.BANG_EQUAL:
            return left != right
        if expr.operator.type == TokenType.EQUAL_EQUAL:
            return left == right

    def check_number_operands(self, operator: Token, left: object, right: object):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def check_number_operand(self, operator: Token, operand: object):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")
