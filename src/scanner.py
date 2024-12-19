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


KEYWORD_MAP = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


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
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    while self.peek() and self.peek() != "\n":
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    print(f"[Line: {self.line}] Error: Unexpected character {c}")
        return

    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        text: str = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def string(self) -> None:
        while self.peek() and self.peek() != '"':
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            print(f"[Line: {self.line}] Error: Unterminated string.")
            return

        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self) -> None:
        while self.peek() and self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()

            while self.peek() and self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self) -> None:
        while self.peek() and self.peek().isalnum():
            self.advance()

        text = self.source[self.start : self.current]
        token_type = KEYWORD_MAP[text] if text in KEYWORD_MAP else TokenType.IDENTIFIER
        self.add_token(token_type)

    def advance(self) -> str:
        """Always advance cursor"""
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        """Only advance cursor if match"""
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str | None:
        """Never advance cursor"""
        if self.is_at_end():
            return None
        return self.source[self.current]

    def peek_next(self) -> str | None:
        """Never advance cursor"""
        if self.current + 1 >= len(self.source):
            return None
        return self.source[self.current + 1]
