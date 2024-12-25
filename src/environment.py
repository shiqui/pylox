from typing import Dict
from scanner import Token
from error import RuntimeError


class Environment:
    def __init__(self):
        self.values: Dict[str, object] = dict()

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise RuntimeError(name, f"Undefined Variable '{name.lexeme}'.")
