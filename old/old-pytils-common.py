#!/usr/bin/env python
## $Id: common.py,v 1.12 2004-02-10 21:53:15 hevi Exp $

""" Common utility objects.
Usage:
from pytils.common import *
= import_all_safe

Making nothing
--------------

Inheritance should be in object systems::

  Void
    None
      Object
        Null
        Class


"""
__version__ = "$Revision: 1.12 $"

######################################################################
## dependencies, keep minimal
import os

######################################################################
## exceptions
## - provide exceptions in this way too

from pytils.spec.exc import *
import threading

######################################################################
## relpath
## - XXX move out of here, to file or path

def relpath(frm,to):
  """ relpath(frm@string,to@string) @string, raises ValueError:
  Constructs relative path from frm to to.
           to=abs   to=rel
  frm=abs  ok       to returned
  frm=rel  error    frm + to
  """
  if not os.path.isabs(frm):
    if os.path.isabs(to):
      raise ValueError("cannot create relative path from " + frm + " to " + to)
    return os.path.join(frm,to)
  if not os.path.isabs(to):
    return to
  # frm is abs, to is abs
  frm = os.path.normpath(frm).split(os.sep)[1:]
  to = os.path.normpath(to).split(os.sep)[1:]
  result = []
  while len(frm) and len(to) and frm[0] == to[0]: 
    frm.pop(0); to.pop(0)
  while len(frm) > 0:
    frm.pop(0); result.append("..")
  result = os.sep.join(result + to)
  return result

######################################################################
## isseq

def is_seq(object):
  """ isseq(object) @boolean:
  Return true if objects is sequence type. Commonly tuple or
  list.
  """
  return isinstance(object,tuple) or isinstance(object,list)

######################################################################
## gcd


######################################################################
## Void


######################################################################
## Null
## - from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/68205
## 
## This is a sample implementation of the 'Null Object' design pattern.
## 
## Roughly, the goal with Null objects is to provide an 'intelligent'
## replacement for the often used primitive data type None in Python or
## Null (or Null pointers) in other languages. These are used for many
## purposes including the important case where one member of some group 
## of otherwise similar elements is special for whatever reason. Most 
## often this results in conditional statements to distinguish between
## ordinary elements and the primitive Null value.
## 
## Among the advantages of using Null objects are the following:
## 
##   - Superfluous conditional statements can be avoided 
##     by providing a first class object alternative for 
##     the primitive value None.
## 
##   - Code readability is improved.
## 
##   - Null objects can act as a placeholder for objects 
##     with behaviour that is not yet implemented.
## 
##   - Null objects can be replaced for any other class.
## 
##   - Null objects are very predictable at what they do.
## 
## To cope with the disadvantage of creating large numbers of passive 
## objects that do nothing but occupy memory space Null objects are 
## often combined with the Singleton pattern.
## 
## For more information use any internet search engine and look for 
## combinations of these words: Null, object, design and pattern.
## 
## Dinu C. Gherman,
## August 2001

class Null(object):
  """A class for implementing Null objects.
  
  This class ignores all parameters passed when constructing or 
  calling instances and traps all attribute and method requests. 
  Instances of it always (and reliably) do 'nothing'.

  The code might benefit from implementing some further special 
  Python methods depending on the context in which its instances 
  are used. Especially when comparing and coercing Null objects
  the respective methods' implementation will depend very much
  on the environment and, hence, these special methods are not
  provided here.
  """

  # object constructing
    
  def __init__(self, *args, **kwargs):
    "Ignore parameters."
    return None

  # object calling

  def __call__(self, *args, **kwargs):
    "Ignore method calls."
    return self

  # attribute handling

  def __getattr__(self, mname):
    "Ignore attribute requests."
    return self

  def __setattr__(self, name, value):
    "Ignore attribute setting."
    return self

  def __delattr__(self, name):
    "Ignore deleting attributes."
    return self

  # misc.

  def __repr__(self):
    "Return a string representation."
    return "<Null>"

  def __str__(self):
    "Convert to a string and return it."
    return "Null"

  def __len__(self):
    return 0

  def __nonzero__(self):
    return 0

  def __iter__(self):
    class NoIter:
      def __iter__(self):
        return self
      def next(self):
        raise StopIteration
    return NoIter()

Null = Null()

######################################################################
## Singleton
## singleton types:
## new
## - N name to 1 object to 1 state
## - from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66531 at end
## - this dont work as aimed, calls __init__ multiple times
## borg
## - from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66531
## - N name to N object to 1 state
## name
## - 1 name to 1 object to 1 state
## - uniform: no, access to object module.Class not module.Class()
## meta
## - used here
## - http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/102187
##

class Singleton(type):
  """ Ensures the class is created and initialized only once. Class constructor
  works as global access point for further object accessing.

  Usage:
  class OnlyOne:
    __metaclass__ = Singleton
    ..
    
  Remarks:
  - N name to 1 object to 1 state model
  - from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/102187
  - calls objects __init__ only once
  - object __call__ works
  - supports inheritance from singletons, every class gets own single instance
  object.
  """
  def __init__(self,name,bases,dict):   # initializes a class
    self._instance = None               # per class based instance
    type.__init__(self,name,bases,dict) 
  def __call__(self,*args,**kwds):      # from class to object
    if self._instance == None:
      self._instance = type.__call__(self,*args,**kwds)
    return self._instance

class SingletonBase(object):
  """ Same functionality as in Singleton, but can be inherited.
  Usage:
  class OnlyOne(SingletonBase):
    ..
  """
  __metaclass__ = Singleton

######################################################################
## correct inheritable Property

class Property(object): 
  """
  Property member decorator with inheritable get,set,del.
  """
 
  def __init__(self, fget=None, fset=None, fdel=None, doc=None):
    """
    - fget @function
    - fset @function
    - fdel @function
    - doc @str
    """
    self._get = fget 
    self._set = fset 
    self._del = fdel 
    self.__doc__ = doc
 
  def __get__(self, obj, objtype=None):
    if obj is None: 
      return self          
    if self._get is None: 
      raise AttributeError("non-read property")
    return getattr(obj,self._get.__name__)()
 
  def __set__(self, obj, value): 
    if self._set is None: 
      raise AttributeError("non-write property")
    getattr(obj,self._set.__name__)(value)
 
  def __delete__(self, obj): 
    if self._del is None: 
      raise AttributeError("non-removeable property")
    getattr(obj,self._del.__name__)()

# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

