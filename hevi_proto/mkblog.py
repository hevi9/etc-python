"""
Blog composer and publisher.

Usage::

 > mkblog

"""

import logging
log = logging.getLogger(__name__)

def collect():
  """ Returns """
  pass

def format(arg):
  pass

def publish(arg):
  pass

def main():
  logging.basicConfig(level=logging.DEBUG)
  publish(format(collect()))

if __name__ == "__main__": main()