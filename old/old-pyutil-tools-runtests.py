#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: runtests.py,v 1.2 2004-12-28 05:20:07 hevi Exp $
## MAIN

"""

"""
__version__ = "$Revision: 1.2 $"
__todo__ = """ """

######################################################################
## dependencies
import sys
import os
import optparse as opt
import logging as log
import imp
import unittest

######################################################################
## command line interface object

class Main(object):
  """ %prog [options] """

  def __init__(self,args=sys.argv[1:]):
    parser = opt.OptionParser(Main.__doc__)
    self.specify_options(parser)
    (self.options,self.args) = parser.parse_args(args)
    log.basicConfig()
    log.getLogger().setLevel(log.INFO)
    if self.options.quiet:
      log.getLogger().setLevel(log.WARNING)
    if self.options.debug:
      log.getLogger().setLevel(log.DEBUG)

  def specify_options(self,parser):
    parser.add_option(
    "","--debug",action="store_true",default=False,dest="debug",
    help="set debug information generation on")
    parser.add_option(
    "","--quiet",action="store_true",default=False,dest="quiet",
    help="set silent information generation")

  def run(self):
    suite = unittest.TestSuite()
    n = 0 # give different module name, otherwise unittest get confused
    for arg in self.args:
      log.debug("adding tests from %s" % arg)
      fd = file(arg)
      n += 1
      module = imp.load_module("test" + str(n),fd,arg,imp.get_suffixes()[2])
      suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)  
  
if __name__ == '__main__':
  Main().run()

######################################################################
# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

