import json
import inspect

_processors = []


def setup(*processors):
    global _processors
    _processors = processors


def process(data):
    for processor in _processors:
        data = processor(data)
    return data


class Log:
    def __init__(self):
        pass

    def __call__(self, lvl: int, *args, **kwargs):
        data = {}
        data["level"] = lvl
        if len(args):
            data["msg"] = " ".join(str(arg) for arg in args)
        data["vars"] = kwargs
        process(data)
        return self


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


def main1():
    setup(
        add_location,
        target_console,
        # target_console_json,
    )
    log(9, "Items are", 99)
    for index in range(5):
        log(0, index=index)
    log(8, "done")


if __name__ == "__main__":
    main1()
