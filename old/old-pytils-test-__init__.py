#!/usr/bin/env python
## $Id: __init__.py,v 1.5 2004-01-05 11:52:56 hevi Exp $
## UNITTEST

"""
"""
__version__ = "$Revision: 1.5 $"

import sys
import os
import unittest

def suite():
  suite = unittest.TestSuite()

  import pytils.tests.importclean
  suite.addTest(pytils.tests.importclean.suite())

  import pytils.tests.file01
  suite.addTest(pytils.tests.file01.suite())

  import pytils.tests.log01
  suite.addTest(pytils.tests.log01.suite())

  import pytils.tests.module01
  suite.addTest(pytils.tests.module01.suite())

  import pytils.tests.singleton
  suite.addTest(pytils.tests.singleton.suite())

  import pytils.tests.termansi
  suite.addTest(pytils.tests.termansi.suite())

  import pytils.tests.common
  suite.addTest(pytils.tests.common.suite())

  import pytils.tests.run
  suite.addTest(pytils.tests.run.suite())

  import pytils.tests.dode
  suite.addTest(pytils.tests.dode.suite())

  return suite

def check():
  runner = unittest.TextTestRunner(verbosity=1)
  result = runner.run(suite())
  return not result.wasSuccessful()

if __name__ == '__main__':
  check()


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:




