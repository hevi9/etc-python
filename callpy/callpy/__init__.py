import argparse
import logging
import os
import re
from fnmatch import fnmatch
from pathlib import Path


log = logging.getLogger(__name__)
D = log.debug


def discover_files(top, file_match, text_match):
    text_re = re.compile(text_match)
    for root, dirs, files in os.walk(top):
        for file in files:
            if fnmatch(file, file_match):
                path = os.path.join(root, file)
                with open(path) as fo:
                    text = fo.read()
                mo = text_re.search(text)
                if mo:
                    yield Path(path)


def path_to_module_name(path):
    pathto = [p.name for p in path.parents if p.name]
    pathto.reverse()
    return ".".join(pathto) + ("" if path.stem in (
        "__init__", "__main__") else "." + path.stem)


def import_end(module_name):
    # D(module_name)
    parts = module_name.split(".")
    parts.reverse()
    module = __import__(module_name)
    parts.pop()
    while parts:
        module = getattr(module, parts[-1])
        parts.pop()
    return module


ARGS = argparse.ArgumentParser()
ARGS.add_argument("name", nargs=1,
                  help="name of callable to run")
ARGS.add_argument("arg", nargs="*",
                  help="argument passed to callable")

import inspect

class Call:

    def __init__(self, name, callobj, module):
        self.name = name
        self.callobj = callobj
        self.module = module

def find_callables(module, match):
    for name, obj in inspect.getmembers(module, callable):
        # D("%s=%r", name, obj)
        if name.find(match) == 0:
            yield Call(name, obj, module)

def main():
    args = ARGS.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    args.name = args.name[0]

    module_names = [path_to_module_name(path) for path in
                    discover_files(".", "*.py", args.name)]
    modules = [import_end(module_name) for module_name in module_names]
    # D(modules)
    calls = []
    for module in modules:
        for call in find_callables(module, args.name):
            calls.append(call)
    if len(calls) > 1:
        print("%r call not unique, cannot call, availbele calls:" % args.name)
        for call in calls:
            print(" * %s in %s" % (call.name, call.module.__file__))
        return 1
    if len(calls) == 0:
        print("no callables found for %r, nothing to call" % args.name)
        return 1
    call = calls[0]
    print("->", call.callobj(*args.arg))