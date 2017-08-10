import json
import inspect

_processors = []

INF = 10
STP = 5
DBG = -10


def setup(*processors):
    global _processors
    _processors = processors


def process(data):
    for processor in _processors:
        data = processor(data)
    return data


class Log:
    def __init__(self):
        self._log_stack = []
        pass

    def __call__(self, lvl: int, *args, **kwargs):
        data = {
            "level": lvl,
            "vars": kwargs,
        }
        if len(args):
            data["msg"] = " ".join(str(arg) for arg in args)
        data["vars"] = kwargs
        process(data)
        return self

    # enter()
    def scope(self, **kwargs):
        pass

        # leave


log = Log()


################################################################################
## processors

def target_console(data):
    print(" ".join("{!s}={!r}".format(k, v) for k, v in data.items()))
    return data


def target_console_json(data):
    print(json.dumps(data))
    return data


def add_location(data):
    data["package"] = __package__
    data["file"] = __file__
    data["frame"] = inspect.getframeinfo(inspect.currentframe())
    return data


################################################################################
## app

import random


def main1():
    setup(
        add_location,
        target_console,
        # target_console_json,
    )
    log(INF, "Items are", 99)
    for index in range(5):
        log(STP, "Round", index, result=random.random())
    log(INF, "done")


if __name__ == "__main__":
    main1()
