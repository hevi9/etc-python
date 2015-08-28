from re import Scanner

from pprint import pformat
import logging
import re

log = logging.getLogger()
D = log.debug

logging.basicConfig(level=logging.DEBUG)


def callback(scanner, text):
    D("CALL %r", text)


def ignore(scanner, text):
    D("IGNORE %r", text)


s = Scanner((
    (r'{{{', callback),
    (r'##', callback),
    (r'\s+', ignore),
    (r'(.+)(?=##)', callback),
))


text = "## {{{  aa##"
while text:
    D("%r", text)
    text = s.scan(text)[1]
