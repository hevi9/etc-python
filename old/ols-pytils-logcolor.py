#!/usr/bin/env python
## $Id: logcolor.py,v 1.6 2003-07-16 14:58:11 hevi Exp $

"""
"""
__version__ = "$Revision: 1.6 $"

from __future__ import generators
import sys
import os
import pytils
from pytils.log import log
from pytils.termansi import color
import pytils.spec.log 

######################################################################

class LogColor(pytils.spec.log.Messages):
  
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
    sys.stderr.write(color(" - " + self.msg2str(msg) + "\n","blue"))

  def debug(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(color(" . " + self.msg2str(msg) + "\n","purple"))

  def error(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(color(" ! " + self.msg2str(msg) + "\n","red")) 

  def system(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(" = " + self.msg2str(msg) + "\n") 

######################################################################

class LogColorDetail(pytils.spec.log.Messages):
  
  def __init__(self):
    self.prog = os.path.basename(sys.argv[0])
    if self.prog == None:
      self.prog = "ipr"
    self.control = None

  def msg2str(self,msg):
    return " ".join(map(str,msg))

  def info(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write("I:" + str(self.prog) + ":"
                     + str(ctx.file) + "[" + str(ctx.line) + "]"
                     + ": " + self.msg2str(msg) + "\n") 

  def debug(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(
      color("D:","purple")
      + str(self.prog) + ":"
      + str(ctx.file) + "[" + str(ctx.line) + "]"
      + ": "
      + color(self.msg2str(msg),"purple")
      + "\n"
      ) 

  def error(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write(
      color("E:" + str(self.prog) + ":"
            + str(ctx.file) + "[" + str(ctx.line) + "]"
            + ": " + self.msg2str(msg) + "\n",
            "red"))

  def system(self,*msg):
    ctx = self.control.ctx
    sys.stderr.write("S:" + str(self.prog) + ":"
                     + str(ctx.file) + "[" + str(ctx.line) + "]"
                     + ": " + self.msg2str(msg) + "\n") 


def test():
  pytils.log.props.debug = 1
  log.addWriter(LogColor())
  log.addWriter(LogColorDetail())
  log.info("this is info message",1,log)
  log.debug("this is debug message",1.2345)
  log.error("this is error message",0x80)
  log.system("this is system message",sys)


if __name__ == '__main__':
  test()

# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

