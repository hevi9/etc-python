#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id$
## MAIN

"""

"""  

######################################################################
## dependencies
import sys
import os
import imp
import string
import inspect as ins
import optparse as opt
import logging
log = logging.getLogger(__name__)

class Element(object):
  pass

class Structure(Element):
  
  def __init__(self):
    self._members = dict()
  
  def add(self,name,element):
    self._members[name] = element

  def members(self):
    return self._members.values()

class Class(Structure):
  
  def __init__(self,**kwds):
    super(Class,self).__init__()
    self._name = kwds["name"]
    self._theobject = kwds["theobject"]

  def name(self):
    return self._name
  
  def theobject(self):
    return self._theobject

class Model(Structure):
  pass

class Function(Element):

  def __init__(self,**kwds):
    self._name = kwds["name"]
    self._theobject = kwds["theobject"]

  def name(self):
    return self._name
  
  def theobject(self):
    return self._theobject  

######################################################################
##

class Session(object):
  
  def __init__(self,**kwds):
    self._input = kwds["input"] # file name
    self._output = kwds["output"] # write stream
    self._model = Model()
    
  def start(self):
    self.run()
    
  def run(self):
    self._extract_input()
    self._generate_output()
    
  def _extract_input(self):
    log.debug(self._input)
    self._module = self._load_module(self._input)
    self._modelbase = self._build_modelbase(self._module)
    
  def _load_module(self,filename):
    desc = None
    for i in imp.get_suffixes():
      if i[2] == imp.PY_SOURCE:
        desc = i
        break
    tbl = string.maketrans("/.","__")
    name = filename.translate(tbl)
    fs = open(filename,desc[1])
    module = imp.load_module(name, fs, filename, desc)
    fs.close()
    return module

  def _build_modelbase(self,module):
    for name,object in ins.getmembers(module):
      if ins.isclass(object):
        #print type(object.__module__), id(module)
        if object.__module__ == module.__name__: # ownership, __module__ member is a str !
          newclass = Class(name=name,theobject=object)
          self._model.add(name,newclass)
    for member in self._model.members():
      theclass = member.theobject()
      #print theclass
      for name,object in theclass.__dict__.iteritems():
        if ins.isroutine(object):          
          if self._function_definition_class(name,object,theclass) == theclass:
            element = Function(name=name,theobject=object)
            member.add(name,element)
                    
  def _function_definition_class(self,fname,fobj,cclass):
    """
    :fname: function name
    :fobj: function object
    :class: current class
    """
    mroseq = list(ins.getmro(cclass))
    mroseq.reverse()
    for klass in mroseq:
      if fname in klass.__dict__:
        return klass
    return None    
    
  def _generate_output(self):
    w = self._output.write
    w(self._file_begin())
    for klass in self._model.members():
      w(self._class_begin(klass))
      for func in klass.members():
        w(self._func_body(func))
      w(self._class_end(klass))
    #
    for klass in self._model.members():
      w(self._testcase_body(klass))
    #
    w(self._file_end())


  def _file_begin(self):
    c = """#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id$
## UNITTEST

import unittest
import logging
log = logging.getLogger(__name__)

import mymodulename # TODO: set target modulename

"""
    return c

  def _file_end(self):
    c = """
if __name__ == '__main__':
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()
"""    
    return c


  def _class_begin(self,eclass): # class as element
    name = eclass.name()
    c = '''
class %(name)s_testimpl(object):
  """ Interface test for %(name)s. """
  
''' % vars()
    return c

  def _class_end(self,eclass):
    c = ""
    return c

  def _func_body(self,efunc):
    name = efunc.name()
    thefunc = efunc.theobject()
    spec = ins.getargspec(thefunc)
    args = spec[0]
    if args[0] == "self":
      args.pop(0)
    args = ",".join(args)
    c = '''  def test_%(name)s(self):
    """ """
    self.target.%(name)s(%(args)s) # TODO: call settings
    # assert rv == X, "Incorrect return values for %(name)s" # TODO: return value check
    
''' % vars()
    return c


  def _testcase_body(self,eclass): # class as element
    name = eclass.name()
    c = '''class test_%(name)s(%(name)s_testimpl,unittest.TestCase):
  """ """
  
  def setUp(self):
    unittest.TestCase.setUp(self)
    self.target = None # TODO: Add target impl object here
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    del self.target
      
''' % vars()
    return c
        

######################################################################
## command line interface object

class Main(object):
  """ %prog [options] targetmodulefile"""

  def __init__(self,args=sys.argv[1:]):
    self.parser = opt.OptionParser(usage=Main.__doc__,version="%prog 0.1.0")
    self.specify_options(self.parser)
    (self.options,self.args) = self.parser.parse_args(args)
    logging.basicConfig()
    rootlog = logging.getLogger()
    rootlog.setLevel(logging.INFO)
    if self.options.quiet:
      rootlog.setLevel(logging.WARNING)
    if self.options.debug:
      rootlog.setLevel(logging.DEBUG)

  def specify_options(self,parser):
    parser.add_option(
      "","--debug",action="store_true",default=False,dest="debug",
      help="set debug information generation on")
    parser.add_option(
      "","--quiet",action="store_true",default=False,dest="quiet",
      help="set silent information generation")

  def run(self):
    if len(self.args) < 1:
      self.parser.error("Need targetmodulefile")
    input = self.args[0]
    session = Session(input=input,output=sys.stdout)
    session.start()

if __name__ == '__main__':
  main = Main()
  main.run()
    
    

      