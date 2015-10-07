import io
import logging
import re
from collections import deque

R = re.compile
log = logging.getLogger()
D = log.debug


class Parser2:

    def __init__(self):
        self._buf = deque()
        self._head = ""
        self._match = {
            "base": (
                (R(r"\n\s*\n"), self._on_next),
            ),
        }
        self._level = ["base"]

    def write(self, text):
        # D("'%s'", text)
        self._head += text
        self._process()

    def close(self):
        pass

    def _process(self):
        # D("buf '%s'", self._buf)

        # prepare match head
        for reo, onfn in self._match:
            mo = reo.match(self._head)
            if mo:
                # D("%s == '%s'", reo, mo.group())
                onfn(mo.group())
                self._head = self._head[len(mo.group()):]
                return
        #
        D("no match %r", self._head)

    def _on_next(self, match):
        D("_on_next %r", match)


PARA_START = "^\s*\S+\s+"
EXTRA_START = "{{{"
PARA_END = r'(\n\n)|(%s)' % EXTRA_END
EXTRA_END = "}}}"

STATE_NONE = 0
STATE_PARA = 1
STATE_EXTRA = 2


class Parser:

    def write_all(self, text):
        D("%r", text)
        reo = re.compile(r'(\n\n)|(\s+(?=\S))')

        start = 0

        while start < len(text):
            mo = reo.search(text, start)
            if mo:
                D("%r %r", mo.start(), mo.end())
                self._on_para(text[start:mo.start()])
                start = mo.end()
            else:
                break

        self._on_para(text[start:])

    def _on_para(self, text):
        D("_on_para(%r)", text)


def main2():
    logging.basicConfig(level=logging.DEBUG)

    parser = Parser()

    buf = io.StringIO(text_misc)
    text = buf.read(7)
    while text:
        parser.write(text)
        text = buf.read(7)


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = Parser()

    parser.write_all(text2)


main()
