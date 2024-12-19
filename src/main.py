from sys import argv
from scanner import Scanner


def run(source: str) -> None:
    scanner = Scanner(source)
    print(f"run: {source}")
    scanner.scan_tokens()


def run_prompt() -> None:
    while True:
        line = input(">> ")
        if not line:
            break
        run(line)


def run_file(filename: str) -> None:
    print(f"run_file: {filename}")
    with open(filename) as file:
        run(file.read())


if __name__ == "__main__":
    if len(argv) == 1:
        run_prompt()
    elif len(argv) == 2:
        run_file(argv[1])
    else:
        print("Usage: python3 main [script]")
