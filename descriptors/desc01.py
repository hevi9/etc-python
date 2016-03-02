
from inspect import isclass
from pprint import pprint


class Prop:

    def __init__(self):
        print("__init__", self)

    def __set__(self, instance, value):
        print("__set__", self, instance, value)

    def __get__(self, instance, owner):
        print("__get__", instance, owner)
        return 0


class Schema:

    def __init__(self):
        self.__index = {}
        for attr, obj in self.__class__.__dict__.items():
            if isinstance(obj, Prop):
                self.__index[attr] = obj
            if isclass(obj) and issubclass(obj, Schema):
                self.__index[attr] = obj()

    def _index(self):
        return self.__index


class CFG(Schema):
    debug = Prop()
    test = Prop()

    class sub(Schema):
        includes = Prop()

cfg = CFG()
pprint(cfg._index())
print(cfg.sub.includes)
