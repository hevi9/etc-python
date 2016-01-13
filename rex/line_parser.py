from texts import *
import re
from logging import debug as D


class State:

    def match_line(self, parser, line):
        raise NotImplementedError()

    def done(self, parser):
        pass

    @property
    def name(self):
        return self.__class__.__name__


class WHITE(State):

    def match_line(self, parser, line):
        if re.match(r'^\s*$', line):
            return self
        elif re.match(r'^{{{', line):
            parser.buffer += line
            return parser.EXTRA
        else:
            parser.buffer += line
            return parser.PARA


class PARA(State):

    def match_line(self, parser, line):
        if re.match(r'^\s*$', line):
            self.done(parser)
            return parser.WHITE
        elif re.match(r'^{{{', line):
            self.done(parser)
            parser.buffer += line
            return parser.EXTRA
        else:
            parser.buffer += line
            return self

    def done(self, parser):
        parser.parse_para(parser.pop())


class EXTRA(State):

    def match_line(self, parser, line):
        if re.match(r'^}}}', line):
            parser.buffer += line
            self.done(parser)
            return parser.WHITE
        else:
            parser.buffer += line
            return self

    def done(self, parser):
        parser.parse_extra(parser.pop())


class Buffer:

    def __init__(self):
        self.lines = []

    def __iadd__(self, other):
        self.lines.append(other)
        return self

    def text(self):
        return "\n".join(self.lines)


class Parser:

    WHITE = WHITE()
    PARA = PARA()
    EXTRA = EXTRA()

    def __init__(self):
        self.state = self.WHITE
        self.line_counter = 0
        self.buffer = Buffer()
        self.txt_current = None

    def parse_text(self, text):
        self.line_counter = 0
        for line in text.splitlines():
            self.parse_line(line)
        self.state.done(self)

    def parse_line(self, line):
        self.line_counter += 1
        self.state = self.state.match_line(self, line)

    def pop(self):
        """ Return collected text lines and reset/pop buffer. """
        lines = self.buffer.lines
        self.buffer = Buffer()
        return lines

    def parse_para(self, lines):
        D("PARA %r", lines)
        text = " ".join(lines)
        if re.match(r'^@@', text):
            # finish current txt if any and create new txt
            pass
        else:
            # add element to current txt
            pass

    def parse_extra(self, lines):
        D("EXTRA %r", lines)


class Txt:

    pass
