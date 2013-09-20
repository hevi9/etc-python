#!/usr/bin/env python
## $Id: log.py,v 1.12 2003-08-13 16:58:59 hevi Exp $
##
## PROPS
##  dlevel: 0
## 
## TODO
## - logging on interpreter
## - could dictionares used instead multiple functions ?
## - getting process session properties (dependency, this goes to dlevel 1)
## - control to log ? use: log.info() feasible ?
## - structured logs
## - one line multi logs logs
## - ansi coloring logger
##

"""
Usage:
from mod.log import log
log.info(..)
log.system(..)
log.error(..)
log.debug(..)
"""
__version__ = "$Revision: 1.12 $"

from __future__ import generators
import sys
import os
import inspect
import string
from threading import *
from pytils.spec.log import *

class Props:
  def __init__(self):
    self.debug = 0
    self.quiet = 0

props = Props()

class options(object):

  def option_debug(self,arg):
    """ Set debugging messages on"""
    #pytils.log.props.debug = 1
    props.debug = 1

  def option_quiet(self,arg):
    """ No messages"""
    #pytils.log.props.quiet = 1
    props.quiet = 1
    

######################################################################

# default implementation
class LogDefault(Messages):
  
  def __init__(self):
    self.prog = os.path.basename(sys.argv[0])
    if self.prog == None:
      self.prog = "ipr"
    self.control = None

  def msg2str(self,msg):
    def tostr(l):
      for i in l:
        yield str(i)
    return " ".join(tostr(msg))

  def info(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write("I:" + str(self.prog) + ":"
                     + str(ctx.file) + "[" + str(ctx.line) + "]"
                     + ": " + self.msg2str(msg) + "\n") 

  def debug(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write("D:" + str(self.prog) + ":"
                     + str(ctx.file) + "[" + str(ctx.line) + "]"
                     + ": " + self.msg2str(msg) + "\n") 

  def error(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write("E:" + str(self.prog) + ":"
                     + str(ctx.file) + "[" + str(ctx.line) + "]"
                     + ": " + self.msg2str(msg) + "\n") 

  def system(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write("S:" + str(self.prog) + ":"
                     + str(ctx.file) + "[" + str(ctx.line) + "]"
                     + ": " + self.msg2str(msg) + "\n") 

######################################################################

class LogSimple(Messages):
  
  def __init__(self):
    self.prog = os.path.basename(sys.argv[0])
    if self.prog == None:
      self.prog = "ipr"
    self.control = None

  def msg2str(self,msg):
    def tostr(l):
      for i in l:
        yield str(i)
    return " ".join(tostr(msg))

  def info(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(" - " + self.msg2str(msg) + "\n") 

  def debug(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(" . " + self.msg2str(msg) + "\n") 

  def error(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(" ! " + self.msg2str(msg) + "\n") 

  def system(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(" = " + self.msg2str(msg) + "\n") 

######################################################################

class LogContext: pass

class Control(Messages):
  """ Controlling chain part.
  """ 
  
  def __init__(self):
    self.writers = list()
    #self.addWriter(LogDefault())
    self.writeTime = 0
    self.writeLocation = 1
    self.lock = RLock()
    self.ctx = LogContext() # placeholder structure

  def addWriter(self,writer):
    """ setWriter(writer Log) Control.
    """
    self.writers.append(writer)
    writer.control = self # XXX
    return self

  def set_writer(self,writer):
    """
    """
    del self.writers[:]
    self.writers.append(writer)
    writer.control = self # XXX
    return self

  def remove_writer(self,writer):
    self.writers.remove(writer)

  def setWriteTime(self,onoff):
    """
    """
    self.writeTime = onoff
    return self

  def setWriteLocation(self,onoff):
    """
    """
    self.writeLocation = onoff
    return self

  def fixCtx(self):
    if self.ctx.file == None:
      self.ctx.file == ""
    if self.ctx.line == None:
      self.ctx.line == ""
    
  def info(self,*msg):
    if props.quiet == 1: return
    self.lock.acquire()
    stack = inspect.stack()
    self.ctx.file = stack[1][1]
    self.ctx.line = stack[1][2]
    self.fixCtx()
    for writer in self.writers:
      writer.info(*msg)
    self.lock.release()
    return self

  def system(self,*msg):
    if props.quiet == 1: return
    self.lock.acquire()
    stack = inspect.stack()
    self.ctx.file = stack[1][1]
    self.ctx.line = stack[1][2]
    self.fixCtx()
    for writer in self.writers:
      writer.system(*msg)
    self.lock.release()
    return self
                     
  def debug(self,*msg):
    if props.debug == 0 or props.quiet == 1: return
    self.lock.acquire()
    stack = inspect.stack()
    self.ctx.file = stack[1][1]
    self.ctx.line = stack[1][2]
    self.fixCtx()
    for writer in self.writers:
      writer.debug(*msg)
    self.lock.release()
    return self
                     
  def error(self,*msg):
    if props.quiet == 1: return
    self.lock.acquire()
    stack = inspect.stack()
    self.ctx.file = stack[1][1]
    self.ctx.line = stack[1][2]
    self.fixCtx()
    for writer in self.writers:
      writer.error(*msg)
    self.lock.release()
    return self


log = Control()
"""
"""

######################################################################

######################################################################

if __name__ == '__main__':
  log.addWriter(LogSimple())
  log.info("this is info message",1,log)
  log.debug("this is debug message",1.2345)
  log.error("this is error message",0x80)
  log.system("this is system message",sys)
  pass

# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
