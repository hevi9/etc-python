import re
from logging import debug as D
from enum import Enum


class Stack(list):

    push = list.append

    def __call__(self):
        return self[-1]


class Para:
    pass


class Txt(Para):
    pass


# print(re.findall(r'^\s*$|^@@|\n', text, re.MULTILINE))

NOM = "nomatch"

state_start = {
    "nl": r'\n',
    "txt": r'^@@',
    "li": r'^ *\*',
    "empty": r'^\s*?$',
    "link_start": r'\[\[',
    "number": r'[ \t]*(\d+\.)+',
    NOM: None
}

state_link = {
    "nl": r'\n',
    "link_end": r'\]\]',
    NOM: None
}


class YaParser:

    def __init__(self):
        #
        self.stack = Stack()

        #
        self.pos_start = 0
        self.pos_end = 0

        # construt re
        patterns = []
        self.p2f = {}
        for pattern, name in rules:
            c = "(?P<{}>{})".format(name, pattern)
            patterns.append(c)
            f = getattr(self, name)
            self.p2f[name] = f
        self.patterns = "|".join(patterns)
        # self.re = re.compile(self.patterns, re.MULTILINE | re.DEBUG)
        self.re = re.compile(self.patterns, re.MULTILINE)

    def parse_text(self, text):
        while True:
            # guard if next end_pos excess text
            if self.pos_end > len(text):
                # D("==> end, match over text <==")
                break

            # D("search %r-%r => %r", self.pos_start, self.pos_end, len(text))
            mo = self.re.search(text, self.pos_end)
            if mo:
                # D("==> nomatch(%r-%r) %r <==", self.pos_end, mo.start(), mo)
                #
                if mo.start() > self.pos_end:
                    self.nomatch(text[self.pos_end:mo.start()])
                #
                self.p2f[mo.lastgroup](mo)
                if len(mo.group()) == 0:  # empty match
                    self.pos_end += 1
                    self.pos_start = self.pos_end
                else:
                    self.pos_start = mo.start()
                    self.pos_end = mo.end()
            else:
                # D("==> end <==")
                self.nomatch(text[self.pos_end:])
                break

        # signal end of text
        self.eot()

    def nl(self, mo):
        # D("nl %r", mo)
        pass

    def txt(self, mo):
        D("txt %r", mo)
        self.stack.push(Txt())

    def li(self, mo):
        D("li %r", mo)
        self.stack.push(Para())

    def number(self, mo):
        D("number %r", mo)
        self.stack.push(Para())

    def empty(self, mo):
        D("empty %r", mo)
        self.stack.pop()

    def link_start(self, mo):
        D("link_start %r", mo)

    def link_end(self, mo):
        D("link_end %r", mo)

    def nomatch(self, text):
        D("nomatch %r", text)

    def eot(self):
        D("eot")

import logging
logging.basicConfig(level=logging.DEBUG)
p = YaParser()
p.parse_text(text3)
