import logging

import re
from scanner import Scanner

log = logging.getLogger()
D = log.debug

logging.basicConfig(level=logging.DEBUG)


def test_01():
    text_XX = """
@@ aa
"""

    def callback(mo):
        D("callback %r", mo)

    scanner = Scanner((
        (r'^@@', callback),
        (r'aaa', callback),
    ), re.MULTILINE)
    scanner.scan(text_XX)

if __name__ == "__main__":
    test_01()