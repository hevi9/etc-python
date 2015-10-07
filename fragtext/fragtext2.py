import logging
from re import Scanner
import re
from texts import *

log = logging.getLogger()
D = log.debug

text_XX = """
@@ aa
"""


class Parser:

    def __init__(self):
        self.s1 = Scanner((
            (r'^@@', self.got),
            (r'aa', self.got),
        ))

    def write_all(self, text):
        D("scan %r", self.s1.scan(text))

    def got(self, text):
        D("GOT %r", text)


def main():
    parser = Parser()
    parser.write_all(text_XX)


logging.basicConfig(level=logging.DEBUG)
main()
