#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: run.py,v 1.1 2003-08-13 16:58:59 hevi Exp $
## UNITTEST

"""
"""
__version__ = "$Revision: 1.1 $"

######################################################################
## depends

import os
import unittest
from pytils.run import *

######################################################################
## test configuration


######################################################################
## test material


######################################################################
## test base

class TestBase(unittest.TestCase):

  def setUp(self):
    pass
    
  def tearDown(self):
    pass


######################################################################
## test program

test_signal_program = """#!/usr/bin/env python
while 1:
  pass
"""

test_stdin_program = """#!/usr/bin/env python
import sys
buf = sys.stdin.read() 
if buf == "test":
  sys.exit(0)
else:
  sys.exit(1)
"""

test_stdout_program = """#!/usr/bin/env python
import sys
sys.stdout.write("stdout test")
sys.stdout.close()
sys.exit(0)
"""

test_stderr_program = """#!/usr/bin/env python
import sys
sys.stderr.write("stderr test")
sys.stderr.close()
sys.exit(0)
"""

class Counter(object):
  make_program = 1

def make_program(text):
  name = "/tmp/run_test." + str(os.getpid()) + "." + str(Counter.make_program)
  Counter.make_program += 1
  ws = open(name,"w")
  ws.write(text)
  ws.close()
  os.chmod(name,0700)
  return name

def kill_program(name):
  os.remove(name)

class program_test(TestBase):

  def test_exit_true(self):
    prog_true = program("true")
    ps = prog_true()
    ps.wait()
    assert(ps.status() == 0)

  def test_exit_false(self):
    prog_false = program("false")
    ps = prog_false()
    ps.wait()
    assert(ps.status() != 0)

  def test_signal(self):
    prog = make_program(test_signal_program)
    child = program(prog)
    ps = child()
    ps.kill()
    ps.wait()
    assert(os.WIFSIGNALED(ps.status()))
    assert(os.WTERMSIG(ps.status()) == 15)
    kill_program(prog)

  def test_stdin(self):
    prog = make_program(test_stdin_program)
    child = program(prog)
    ps = child(program.stdin)
    ps.stdin.write("test")
    ps.stdin.flush()
    ps.stdin.close()
    ps.wait()
    assert(ps.status() == 0)
    kill_program(prog)

  def test_stdout(self):
    prog = make_program(test_stdout_program)
    child = program(prog)
    ps = child(program.stdout)
    buf = ps.stdout.read()
    ps.wait()
    assert(buf == "stdout test")
    kill_program(prog)

  def test_stderr(self):
    prog = make_program(test_stderr_program)
    child = program(prog)
    ps = child(program.stderr)
    buf = ps.stderr.read()
    ps.wait()
    assert(buf == "stderr test")
    kill_program(prog)

######################################################################
## test Thing2

class Thing2_test(TestBase):

  def test_function(self):
    """ what to test """
    assert(0)



######################################################################
## to testing system

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(program_test,'test'))
  #suite.addTest(unittest.makeSuite(Thing2_test,'test'))
  return suite

def check():
  runner = unittest.TextTestRunner(verbosity=1)
  result = runner.run(suite())
  return not result.wasSuccessful()

if __name__ == '__main__':
  check()


######################################################################
# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:




