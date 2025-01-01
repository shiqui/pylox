from abc import ABC, abstractmethod
from time import time_ns

from environment import Environment
from parser.stmt import Function


class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments):
        return time_ns() / 1e6

    def __str__(self):
        return "<native fn>"


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        interpreter.execute_block(self.declaration.body, environment)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
