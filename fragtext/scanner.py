import re
import logging


log = logging.getLogger()
D = log.debug


class Scanner:

    def __init__(self, lexicon, flags=0):

        self._lexicon = lexicon
        self._id_to_action = {}  # on match call action by given id

        # collect patterns with action id
        rpatterns = []
        for pattern, action in lexicon:
            aid = "ID" + str(id(pattern))  # action id by pattern
            # D("id %r", aid)
            self._id_to_action[aid] = action
            rpatterns.append("(?P<%s>%s)" % (aid, pattern))

        # combine
        fpattern = "|".join(rpatterns)
        D("fpattern %r", fpattern)
        self._reo = re.compile(fpattern, flags)

    def scan(self, text, pos=0):
        mo = self._reo.search(text, pos)
        if mo:
            assert mo.lastgroup
            action = self._id_to_action[mo.lastgroup]
            # D("MATCH %r call %r", mo.group(), action)
            # action(mo)
            return mo, action
        else:
            # D("NO MATCH")
            return None, None

    def __repr__(self):
        return "Scanner %s" % pformat(self._rules)
