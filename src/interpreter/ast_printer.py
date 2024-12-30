from parser.expr import (
    Expr,
    Binary,
    Grouping,
    Unary,
    Literal,
    Visitor as ExprVisitor,
)


class AstPrinter(ExprVisitor):
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
