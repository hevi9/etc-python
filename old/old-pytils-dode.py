#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: dode.py,v 1.8 2004-01-05 11:52:56 hevi Exp $

"""
Dependency node.

Roles
-----

 - supplier provides something
 - client uses (depends) something
 - client depends on supplier
 - supplier supports client

"""
__version__ = "$Revision: 1.8 $"

from __future__ import generators

if __name__ == '__main__':
  import pytils.dode
  import sys
  sys.exit(pytils.dode.check())

######################################################################
## dependencies

from pytils.spec.exc import *

######################################################################
## graph visitor

class Visitor(object):
  def visit(self,dode):
    pass
  def depthFirst(self):
    pass

class CycleCheckVisitor(Visitor):
  def __init__(this,dode):
    this._dode = dode
  def visit(this,dode):
    if dode == this._dode:
      raise LoopError("cycle detectyed on dependency graph",dode)
  def depthFirst(this):
    return 0

######################################################################
## Dode

class Dode(object):
  """ Dependency Node. Combines subject and observer.
  """

  def __init__(this):
    this._supports = {}   # XXX
    this._depends = {}    # XXX

  def supports(this):
    """
    """
    return this._supports

  def depends(this):
    """
    """
    return this._depends
  
  def update(this,supplier):
    """ Update this dode to reflect changes of supplier.
    """
    raise NotImplementedError
    return this
  
  def notify(this):
    """ Notify clients of this dode that something has been changed.
    """
    for client in this.supports():
      client.update(this)
    return this

  def accept(this,visitor):
    """
    """
    if visitor.depthFirst():  # depth first
      this.subaccept(visitor)
      visitor.visit(this)
    else:                     # wide first
      visitor.visit(this)
      this.subaccept(visitor)

  def subaccept(this,visitor):
    for supplier in this.depends():
      supplier.accept(visitor)
  
  def support(this,client):
    """
    """
    if client in this._supports: return this
    this._supports[client] = client
    client.depend(this)
    return this
  
  def unsupport(this,client):
    """
    """
    if client not in this._supports: return this
    del this._supports[client]
    client.undepend(this)
    return this
  
  def depend(this,supplier):
    """
    """
    if supplier in this._depends: return this
    this._depends[supplier] = supplier
    supplier.accept(CycleCheckVisitor(this)) # check cycles
    supplier.support(this)
    return this

  def undepend(this,supplier):
    """
    """
    if supplier not in this._depends: return this
    del this._depends[supplier] # XXX does this delete ref or object ?
    supplier.unsupport(this)
    return this


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

