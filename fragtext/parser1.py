from scanner import Scanner
import logging
import re
from texts import *

log = logging.getLogger()
D = log.debug


class Parser:

    def __init__(self):
        # define scanners
        flags = re.MULTILINE
        # flags = 0
        self.s1 = Scanner((
            (r'\n\n', self.on_nl2),
            (r'\n', self.on_nl),
            (r'@@', self.on_frag),
            (r'{{{', self.on_begin),
        ), flags)
        self.s2 = Scanner((
            (r'}}}', self.on_end),
        ), flags)

        # states
        self.scanner = self.s1
        self.linenro = 0

    def write_all(self, text):
        start_pos = 0
        while True:
            mo, action = self.scanner.scan(text, start_pos)
            if mo:
                # D("MM %r,%r", mo.start(), mo.end())
                if mo.start() > start_pos:
                    self.on_nomatch(text[start_pos:mo.start()])
                action(mo.group())
                start_pos = mo.end()
            else:
                self.on_nomatch(text[start_pos:])
                break

    def on_frag(self, text):
        D("on_frag %r", text)

    def on_emptyline(self, text):
        D("on_emptyline %r", text)

    def on_nl(self, text):
        # D("NL")
        self.linenro += 1

    def on_nl2(self, text):
        # D("NLNL")
        self.linenro += 2

    def on_begin(self, text):
        D("on_begin %r", text)
        self.scanner = self.s2

    def on_end(self, text):
        D("on_end %r", text)
        self.scanner = self.s1

    def on_nomatch(self, text):
        D("on_nomatch %r", text)


def main():
    parser = Parser()
    parser.write_all(text_01)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
