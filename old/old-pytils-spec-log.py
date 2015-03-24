#!/usr/bin/env python
## $Id: log.py,v 1.1 2003-07-08 21:12:12 hevi Exp $
## SPECIFICATION

"""

Usage::
  from pytils.log import log
  log.info(..)
  log.system(..)
  log.warn(..)
  log.error(..)
  log.debug(..)

Related systems:
 * logging module
   - http://www.red-dove.com/python_logging.html
 * syslog
   - man syslog
 

"""

"""

Target Writer
Loggers Each Logger instance represents "an area" of the application.
Formatter
Log levels
Handler StreamHandler FileHandler RotatingFileHandler SocketHandler
  DatagramHandler SMTPHandler SysLogHandler MemoryHandler NTEventLogHandler
  HTTPHandler
Formatters
Filters
Configuration

"""

__version__ = "$Revision: 1.1 $"

class Messages:
  """
  Logging messages.

  The system implementing this interface may not made any other action
  that report the message into target. On error, critical or emergency
  the implementor may not exit system. It's other module responsibility
  to decide action on that kind of cituation.

  """
  def info(self,*msg):
    """ 
    Informative messages. Helps user to understand how program
    behaves. Same as notice or announce.
    - *msg@object
    + self
    = logfunction
    See::
      --quiet options should deactivate these.
    """
    raise NotImplementedError

  def system(self,*msg):
    """
    Inform a action that changes system.
    - *msg@object
    + self
    = logfunction
    See::
      --quiet option should deactivate these.
    """
    raise NotImplementedError

  def warn(self,*msg):
    """
    Warning messages.
    - *msg@object
    + self
    = logfunction
    See::
      --quiet option should deactivate these.
    """
    raise NotImplementedError
  
  def debug(self,*msg): 
    """
    Debugging messages.
    - *msg@object
    + self
    = logfunction
    See::
      --debug option should activate these.
    """
    raise NotImplementedError
  
  def error(self,*msg):
    """
    Error messages.
    - *msg@object
    + self
    = logfunction
    See::
    """
    raise NotImplementedError

  def alert(self,*msg):
    """
    Alerting messages.
    - *msg@object
    + self
    = logfunction
    See::
    """
    raise NotImplementedError

  def critical(self,*msg):
    """
    Critical condition messages. These are not supposed to use directly,
    but in a exception handling to report condition. Use exeception
    to report conditions at first hand software internally.
    - *msg@object
    + self
    = logfunction
    See::
    """
    raise NotImplementedError

  def emergency(self,*msg):
    """
    Emergency condition messages. These are not supposed to use directly,
    but in a exception handling to report condition. Use exeception
    to report conditions at first hand software internally. Same as
    fatal. This is usually last message the system makes.
    - *msg@object
    + self
    = logfunction
    See::
    """
    raise NotImplementedError



# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
