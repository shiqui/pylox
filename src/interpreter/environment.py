from typing import Dict
from scanner import Token
from interpreter.error import RuntimeError


class Environment:
    def __init__(self, enclosing: "Environment" = None):
        self.enclosing = enclosing
        self.values: Dict[str, object] = dict()

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeError(name, f"Undefined Variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(name, f"Undefined Variable '{name.lexeme}'.")
