#!/usr/bin/env python
## $Id: session.py,v 1.1 2003-07-08 19:47:53 hevi Exp $

""" Session interface.
"""
__version__ = "$Revision: 1.1 $"
__todo__ = """
9 as session is sequence of actions, the some kind of progess meter
  functionality could be possible build.
"""

class Session(object):
  """ Session object interface. Session declares object that has certain
  sequence of actions between begin() and end() "markers".
  If object can have multiple session is implementation defined. This
  case however have to be checked and reported on begin() and end().
  """

  def begin(self):
    """ begin():
    Session begins. Session object can initialize the system behind the
    session.
    """
    raise NotImplementedError
  
  def end(self):
    """ end():
    Session ends. Session object can finalize the system behing session.
    """
    raise NotImplementedError

## compability, wil be removed
session = Session

# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

