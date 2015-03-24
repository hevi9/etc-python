#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: task.py,v 1.2 2004-01-05 11:52:56 hevi Exp $
## SPECIFICATION

"""

"""
__version__ = "$Revision: 1.2 $"
__todo__ = """
"""

#from __future__ import generators

######################################################################
## dependencies

#import sys
#import os
from pytils.common import *

######################################################################
## task

class Task(object):
  """
  """

  def run(self):
    """
    + Void
    """
    pass

  def is_complete(self):
    """
    + @bool
    """
    pass

  def load(self):
    """
    """
    pass

  def is_running(self): # thread
    """
    + @bool
    """
    pass

  def is_partial(self):
    """
    """
    pass

  def cancel(self): # thread
    """
    """
    pass

  def parent(self,parent = Void):
    """
    + @Task
    """
    pass


  def priority(self):
    """
    + @int, zero = normal, plus = higher, negative = lower 
    """
    pass


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

