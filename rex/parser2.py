import re
from logging import debug as D

text1 = """xx@@
  
yy
@@ jj
 * jeeee
 
 xx
 * 
 
 cc
 
 text (( link 
 )) 
 
1. text 

2.1. text """

text2 = """
 * 

xx

cc"""

text3 = """

@@ testing #lotto

"""


# print(re.findall(r'^\s*$|^@@|\n', text, re.MULTILINE))

rules = (
    (r'\n', "nl"),
    (r'^@@', "txt"),
    (r'^ *\*', "li"),
    (r'^\s*?$', "empty"),
    (r'\(\(', "link_start"),
    (r'\)\)', "link_end"),
    (r'[ \t]*(\d+\.)+', "number")
)


class YaParser:

    def __init__(self):
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

    def li(self, mo):
        D("li %r", mo)

    def number(self, mo):
        D("number %r", mo)

    def empty(self, mo):
        D("empty %r", mo)

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
