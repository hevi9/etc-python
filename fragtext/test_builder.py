import logging

from builder import Builder

log = logging.getLogger()
D = log.debug


def main():
    b = Builder()
    b.frag("title 1").para("text text").para("text")
    b.frag("title 2").para("text")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
