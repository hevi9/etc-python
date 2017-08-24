import json
import inspect


def target_console(data):
    print(data["msg"],
          " ".join("{!s}={!r}".format(k, v) for k, v in data["vars"].items()))
    return data


def target_console_json(data):
    print(json.dumps(data))
    return data


def add_location(data):
    data["package"] = __package__
    data["file"] = __file__
    data["frame"] = inspect.getframeinfo(inspect.currentframe())
    return data
