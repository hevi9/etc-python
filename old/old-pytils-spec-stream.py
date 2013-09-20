#!/usr/bin/env python
## $Id: stream.py,v 1.2 2003-07-09 18:34:16 hevi Exp $

"""
Write::
 ws = wstream_impl()
 ws.begin()
 for data in source:
   if ws.write_ready():
     ws.write(data)
 ws.end()
   

"""
__version__ = "$Revision: 1.2 $"

from pytils.spec.session import *

######################################################################

class stream(session):
  """
  """
  pass

class wstream(stream):
  """ Push style parser interface.
  """

  def write_ready(self):
    """ write_ready() @boolean:
    Check if stream be be written.
    Return true if write available.
    Nonblocking.
    """
    raise NotImpelmentedError
  
  def write(self,data):
    """ write(data@str) @int:
    Write data into stream.
    Returns numbers of bytes written or consumed.
    Blocking.
    """
    raise NotImpelmentedError

class rstream(stream):
  """
  """

  def read_ready(self):
    """ read_ready() @boolean:
    Check if stream can be read.
    Return true if read available.
    Nonbloking.
    """
    raise NotImpelmentedError
  
  def read(self,size):
    """ read(size@int) str:
    Blocking.
    """
    raise NotImpelmentedError


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

