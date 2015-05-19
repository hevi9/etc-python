import logging
from collections import deque
log = logging.getLogger(__name__)
D = log.debug
LOGFORMAT = "[%(levelname)s|%(filename)s:%(lineno)s|%(funcName)s] %(message)s"
logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)


class Manipulator:

    def apply(self, value):
        pass


class doc(Manipulator):

    def __init__(self, text):
        self.text = text

    def apply(self, value):
        value.text = self.text


class Base:

    def __init__(self, up, name):
        self.__up = up
        self.__name = name

    def __str__(self):
        return ".".join(self._path())

    def _path(self):
        return self.__up._path() + [self.__name] if self.__up is not None else []

    def is_group(self):
        return False

    @property
    def name(self):
        return self.__name


class Value(Base):

    def __init__(self, up, name, value):
        super().__init__(up, name)
        self.value = value


class Group(Base):

    def __init__(self, up=None, name=None):
        self.__data = dict()  # have to be first or recursion death
        super().__init__(up, name)

    def __getattr__(self, key):
        # D(key)
        if key in self.__data:
            # D("exists %s", key)
            obj = self.__data[key]
            if isinstance(obj, Value):
                return obj.value
            else:
                return obj
        else:
            # D("new %s", key)
            return self.__data.setdefault(key, Group(self, key))

    def __setattr__(self, key, value):
        if key.startswith("_"):
            self.__dict__[key] = value
        else:
            if key in self.__data:
                obj = self.__data[key]
                if isinstance(obj, Value):
                    if isinstance(value, Manipulator):
                        # D("apply manipulator")
                        value.apply(obj)
                    else:
                        obj.value = value
                        # D("%s=%s", obj, value)
                else:
                    if isinstance(obj, Group) and len(obj.__data) == 0:
                        obj = Value(self, key, value)
                        self.__data[key] = obj
                        D("%s=%s", obj, value)
                    else:
                        raise RuntimeError(
                            "%s is %s, cannot assign value %s" %
                            (obj, type(obj), value))
            else:
                obj = Value(self, key, value)
                self.__data[key] = obj
                # D("%s=%s", obj, value)

    def __iter__(self):
        return iter(self.__data.values())

    def is_group(self):
        return True


cfg = Group()


def run2():
    cfg.a.b.c = 2
    cfg.a.b.c = 10
    cfg.a.b.c = doc("testing value int")
    D("cfg.a.b.c=%s", cfg.a.b.c)


def run1():
    D(cfg.x)
    cfg.x = 1
    D(cfg.x)
    # cfg.x.y
    D(cfg.y.a)
    D(cfg.y)
    cfg.y = 2
    D(cfg.y)
    #cfg.y.a = 3


def run3():
    cfg.x  # volatile empty group here
    D(cfg.x)
    cfg.x = 1
    D(cfg.x)


def run4():
    cfg.a
    cfg.a.b
    cfg.a.x = 1
    cfg.a.b.y = 2

    def walk(node):
        for i in node:
            if i.is_group():
                print(i)
                walk(i)
            else:
                print(i, i.value)
    walk(cfg)

import json


def tods(top):
    def walk(node):
        d = {}
        for i in node:
            if i.is_group():
                d[i.name] = walk(i)
            else:
                d[i.name] = i.value
        return d
    return walk(cfg)

import yaml


def run5():
    cfg.a
    cfg.a.b
    cfg.a.x = 1
    cfg.a.b.y = 2
    cfg.a.b.z = [1, 2, 3]
    print(json.dumps(tods(cfg)))
    print(yaml.dump(tods(cfg)))


run5()
