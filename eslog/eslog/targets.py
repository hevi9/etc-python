import json
from pprint import pprint


def target_console(data):
    print(
        data["msg"],
        " ".join("{!s}={!r}".format(k, v) for k, v in data["vars"].items())
    )
    return data


def target_console_json(data):
    print(json.dumps(data, indent=2))
    return data


def target_pprint(data):
    pprint(data)
    return data
