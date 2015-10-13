class MC(type):

    def __new__(cls, name, bases, dict_):
        print("Creating class %s%s with attributes %s" %
              (name, bases, dict_))
        return type.__new__(cls, name, bases, dict_)


class start(metaclass=MC):


    def __init__(self):
        pass

start()
