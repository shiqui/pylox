from sys import argv
from scanner import Scanner, TokenType, Token
from parser import Parser
from interpreter import Interpreter
from error import RuntimeError


class Pylox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = Interpreter(self)

    def run(self, source: str) -> None:
        # Scan
        scanner = Scanner(self, source)
        tokens = scanner.scan_tokens()
        # for token in tokens:
        #     print(token)
        # Parse
        parser = Parser(self, tokens)
        statements = parser.parse()
        if self.had_error:
            return
        # Interpret
        self.interpreter.interpret(statements)

    def run_prompt(self) -> None:
        while True:
            line = input(">> ")
            if not line:
                break
            self.run(line)
            self.had_error = False

    def run_file(self, filename: str) -> None:
        with open(filename) as file:
            self.run(file.read())
        if self.had_error:
            exit(65)
        if self.had_runtime_error:
            exit(70)

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True

    def scanner_error(self, line: int, message: str) -> None:
        self.report(line, "", message)

    def parser_error(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def runtime_error(self, error: RuntimeError) -> None:
        print(f"{error.message}\n[line {error.token.line}]")
        self.had_runtime_error = True


if __name__ == "__main__":
    pylox = Pylox()
    if len(argv) == 1:
        pylox.run_prompt()
    elif len(argv) == 2:
        pylox.run_file(argv[1])
    else:
        print("Usage: python3 src/main [script]")
