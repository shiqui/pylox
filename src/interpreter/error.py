from scanner import Token


class RuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        super().__init__(message)


class Return(RuntimeError):
    def __init__(self, value):
        self.value = value
        super().__init__(None, None)
