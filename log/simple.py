# time - created
# name
# msg
# args ?
# levelName
# levelNo
# pathname
# filename
# module
# exc_info
# exc_name
# stack_info
# lineno
# funcName
# msecs
# relativeCreated
# thread
# threadName
# processName
# process


import logging
from pprint import pprint
import json

_processors = None


def processors(*args):
    global _processors
    _processors = args


def process(data):
    for processor in _processors:
        data = processor(data)
        if data is None:
            break
    return data


class Log:
    def __init__(self, name=""):
        self.name = name

    def scope(self, name):
        return Log(name)

    def __call__(self, *args, **kwargs):
        data = kwargs
        data["@name"] = self.name
        data["@args"] = " ".join(args)
        data["@level"] = 0
        process(data)
        return self


def jsondump(data):
    print(json.dumps(data, sort_keys=True))
    return data


def case1():
    log = Log()
    log("test")
    log = log.scope("sub")
    log("1", "2")


def case2():
    processors(
        jsondump,
    )
    log = Log()
    log(a=1, b=2)
    log = log.scope("test")("testing", test=100)


if __name__ == "__main__":
    case2()
