import sys

class Logger:

    def report(self, line: int, where: str, message: str) -> None:
        sys.stderr.write("[line " + str(line) + "] Error" + where + ": " + message)

    def error(self, line: int, message: str) -> None:
        self.report(line, "", message)

