from pprint import pformat
import logging
import re

log = logging.getLogger()
D = log.debug

logging.basicConfig(level=logging.DEBUG)


class _Rule:

    def __init__(self, respec, call, state):
        self.respec = respec
        self.call = call
        self.state = state

    def __repr__(self):
        return "_Rule({respec!r},{call!r},{state!r})".format(**self.__dict__)

    @property
    def id(self):
        # sre needs python identifier as id name
        return "ID" + str(id(self))


class Scanner:

    def __init__(self):
        self._rules = {}  # {state : [spec, ..]}
        self._rules_dirty = False
        self._rules_exe = None
        self._state = []
        self._id_to_rule = {}
        self._text_buf = ""

    def rule(self, respec, call, state="#root"):
        """ """
        self._rules_dirty = True
        rule = _Rule(respec, call, state)
        self._rules.setdefault(rule.state, []).append(rule)
        self._id_to_rule[rule.id] = rule
        return self

    def write(self, text):
        if self._rules_dirty:
            self._rules_make()

        self._text_buf += text

        pos = 0
        while self._text_buf[pos:]:
            reo = self._rules_exe[self._state[-1]]
            mo = reo.match(self._text_buf, pos)
            if mo:
                assert mo.lastgroup
                rule = self._id_to_rule[mo.lastgroup]
                D("MATCH %r call %r", mo.group(), rule)
                rule.call(mo.group())
                pos = mo.end()
            else:
                D("NO MATCH %r", self._text_buf[pos:])
                break

        self._text_buf = self._text_buf[pos:]

    def close(self):
        pass

    def _rules_make(self):
        self._rules_dirty = False
        self._rules_exe = {}

        def part(rule):
            return "(?P<%s>%s)" % (rule.id, rule.respec)

        for state in self._rules:
            pattern = "|".join([part(i) for i in self._rules[state]])
            D("%s %s", state, pattern)
            reo = re.compile(pattern)
            self._rules_exe[state] = reo

        # set default state if none
        if not self._state:
            self._state.append("#root")

    def __repr__(self):
        return "Scanner %s" % pformat(self._rules)


def callback(text):
    D("CALL %r", text)

s = Scanner()
s.rule(r'{{{', callback)
s.rule(r'##', callback)
s.rule(r'\s+', callback)
s.rule(r'\S+', callback)
s.rule(r'}}}', callback, "extra")
s.write("{{{  {{")
s.write("{ss##")

print(s)
