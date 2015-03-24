#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: test_import_01.py,v 1.5 2005-02-09 17:10:02 hevi Exp $
## UNITTEST

"""
test just importing
"""

######################################################################
## dependencies

import unittest

from pyutil.globals import *
#print dir()

######################################################################
## tests

class TestImports(unittest.TestCase):
  """ test just plain importing """

  def test_importing(self):
    """ test plain imports """
    import pyutil
    import pyutil.common
    import pyutil.cvs
    import pyutil.dag
    import pyutil.exceptions
    import pyutil.module
    import pyutil.multirun
    import pyutil.script
    import pyutil.tree
    ##
    import pyutil.globals

  def test_published(self):
    """ test published objects """
    

######################################################################
## running

if __name__ == '__main__':
  unittest.main()

######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
