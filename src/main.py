from sys import argv
from scanner import Scanner, TokenType, Token
from parser import Parser, AstPrinter


class Pylox:
    def __init__(self):
        self.had_error = False

    def run(self, source: str) -> None:
        scanner = Scanner(self, source)
        tokens = scanner.scan_tokens()
        parser = Parser(self, tokens)
        expression = parser.parse()
        if self.had_error:
            return
        print(AstPrinter().print(expression))

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

    def scanner_error(self, line: int, message: str) -> None:
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True

    def parser_error(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)


if __name__ == "__main__":
    pylox = Pylox()
    if len(argv) == 1:
        pylox.run_prompt()
    elif len(argv) == 2:
        pylox.run_file(argv[1])
    else:
        print("Usage: python3 src/main [script]")
