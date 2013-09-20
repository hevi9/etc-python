#!/usr/bin/env python
## $Id: command.py,v 1.1 2003-07-28 19:38:36 hevi Exp $
## SPECIFICATION

"""
"""
__version__ = "$Revision: 1.1 $"
__todo__ = """
"""

######################################################################
## dependencies

from pytils.common import *

######################################################################
## None

class Node(object):

  def __init__(self,name,context = None):
    """
    """
    self.name = name
    self.context = context
    if self.context:
      self.context._insert_node(self)

  def name(self):
    """
    """
    return self.name

  def context(self):
    """
    """
    return self.context

  def root(self):
    """
    """
    current = self
    while not current.is_root():
      current = current.context()
    return current

  def is_root(self):
    """
    """
    return self.context == None

  def is_leaf(self):
    """
    """
    return None

  def resolve(self,nameseq):
    """ Resolve the qualified name from the tree.
    - nameseq @list(@str), path (sequence of names) to the Node
    + @Node
    = unsafe
    ? KeyError, if the name is not found
    """
    assert(is_seq(nameseq) and len(nameseq) >= 1)
    if len(nameseq) > 1:
      return self.nodes()[nameseq[0]].resolve(nameseq[1:])
    else:
      return self.nodes()[nameseq[0]]

######################################################################
## Context

class Context(Node):
  """
  """

  def __init__(self,name,context):
    Node.__init__(self,name,context)
    self._nodes = dict()

  def _insert_node(self,node):
    self._nodes[node.name()] = node

  def nodes(self):
    """
    """
    return self._nodes

######################################################################
## command

class Command(Node):
  """
  """

  def __init__(self,name,context = None):
    Node.__init__(self,name,context)

  def __call__(self,*args,**kwds):
    """
    """
    raise NotImplementedError

  def is_leaf(self):
    return True

# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

