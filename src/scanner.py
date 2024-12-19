from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()

    GREATER = auto()
    GREATER_EQUAL = auto()

    LESS = auto()
    LESS_EQUAL = auto()

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()

    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c: str = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case _:
                print(f"Unexpected character: {c}")
        return

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
