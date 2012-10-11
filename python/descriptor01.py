"""

http://docs.python.org/howto/descriptor.html

http://www.ibm.com/developerworks/opensource/library/os-pythondescriptors/index.html

http://www.ibm.com/developerworks/library/l-cpdecor/index.html

"""

class Descriptor(object):

  def __init__(self):
    self._name = ''

  def __get__(self, instance, owner):
    print("__get__ self          = {0}".format(self))
    #print("        self.__name__ = {0}".format(self.__name__))
    print("        instance      = {0}".format(instance))
    print("        owner         = {0}".format(owner))
    return self._name

  def __set__(self, instance, value):
    print("__set__ self     = {0}".format(self))
    print("        instance = {0}".format(instance))
    print("        value    = {0}".format(value))
    self._name = value

  def __delete__(self, instance):
    print("__delete__ self     = {0}".format(self))
    print("           instance = {0}".format(instance))
    del self._name

class Person(object):
  name = Descriptor()

user = Person()
user.name = 'john smith'
user.name
del user.name

