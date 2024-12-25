from scanner import Token


class ParseError(Exception):
    pass


class RuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        super().__init__(message)
