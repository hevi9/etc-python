#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: exc.py,v 1.5 2004-01-05 11:52:56 hevi Exp $

"""
Common exceptions.

System exceptions and common exceptions here. All exceptions
here are inherited from the Exception buildin class.

Specialization
--------------

Exception

 * SystemExit

 * StopIteration

 * StandardError
   * KeyboardInterrupt
   * ImportError
   * EnvironmentError
     * IOError -- I/O operation fails for an I/O-related reason
       * **BusyError**
       * **TooLargeError**
       * **NoSpaceError**
       * **InterruptError**
       * **TimeoutError**
     * OSError
       * **ExistsError**
       * **NotExistsError**
       * **SecurityError**
       * WindowsError
       * **LoopError**
       * **DeadlockError**
   * EOFError
   * RuntimeError
     * NotImplementedError
     * **NotSupportedError**
   * NameError
     * UnboundLocalError
     * NotUniqueError
   * AttributeError
   * SyntaxError
     * IndentationError
       * TabError
   * TypeError
   * AssertionError
   * LookupError
     * IndexError
     * KeyError
   * AritchmeticError
     * OverflowError
     * ZeroDivisionError
     * FloatingPointError
   * ValueError
     * UnicodeError
       * UnicodeEncodeError
       * UnicodeDecodeError
       * UnicodeTranslateError
   * ReferenceError
   * SystemError -- internal error for python
   * MemoryError

 * Warning -- just base class
   * UserWarning -- inheritance point for user
   * DeprecationWarning -- warnings about deprecated features
   * PendingDeprecationWarning -- features which will be deprecated in the
     future
   * SyntaxWarning -- warnings about dubious syntax 
   * OverflowWarning -- ???
   * RuntimeWarning -- warnings about dubious runtime behavior
   * FutureWarning -- warnings about constructs that will change
     semantically in the future

Mapping of the system errors to the default exceptions
------------------------------------------------------

IOError::
  EIO	     I/O error
  EREMOTEIO   Remote I/O error

ValueError::
  E2BIG	     Argument list too long
  EBADF	     Bad file number
  EFAULT	    Bad address
  EINVAL	    Invalid argument
  EDOM	    Math argument out of domain of func 
  ENAMETOOLONG File name too long
  ELNRNG	    Link number out of range 
  EBADR	    Invalid request descriptor
  EBADRQC	    Invalid request code 
  EBADSLT	    Invalid slot 
  EDESTADDRREQ	Destination address required 

TypeError::
  ENOEXEC	     Exec format error
  ENOTBLK	    Block device required
  ENOTDIR	    Not a directory 
  EISDIR	    Is a directory
  ENOTTY	    Not a typewriter  
  ENOMSG	    No message of desired type 
  EBFONT	    Bad font file format 
  ENOSTR	    Device not a stream 
  EBADMSG	    Not a data message
  ENOTSOCK    Socket operation on non-socket   
  EPROTOTYPE  Protocol wrong type for socket 
  ENOTNAM	    Not a XENIX named type file 
  EMEDIUMTYPE Wrong medium type 

EXDEV	    Cross-device link
ESPIPE	    Illegal seek
ERANGE	    Math result not representable 
ENOLCK	    No record locks available 
ECHRNG	    Channel number out of range 
EL2NSYNC    Level 2 not synchronized 
EL3HLT	    Level 3 halted 
EL3RST	    Level 3 reset 
EUNATCH	    Protocol driver not attached 
ENOCSI	    No CSI structure available 
EL2HLT	    Level 2 halted 
EBADE	    Invalid exchange 
EXFULL	    Exchange full 
ENONET	    Machine is not on the network 
EREMOTE	    Object is remote 
ENOLINK	    Link has been severed 
EADV	    Advertise error 
ESRMNT	    Srmount error 
ECOMM	    Communication error on send 
EPROTO	    Protocol error
EMULTIHOP   Multihop attempted 
EDOTDOT	    RFS specific error
EBADFD	    File descriptor in bad state 
EREMCHG	    Remote address changed
ELIBBAD	    Accessing a corrupted shared library 
ELIBSCN	     lib section in a.out corrupted 
EILSEQ	    Illegal byte sequence
ERESTART    Interrupted system call should be restarted 
ESTRPIPE    Streams pipe error 
EALREADY    Operation already in progress 
EINPROGRESS Operation now in progress
EUCLEAN	    Structure needs cleaning 
EISNAM	    Is a named type file 
"""

__version__ = "$Revision: 1.5 $"

######################################################################
## common exceptions

class ExistsError(OSError):
  """
  Requested operation cannot be completed, because some object
  is on it's way. Ususally on object creation, where operation would
  destroy existing object.
  EEXIST	    File exists
  -> ExistsError
  ENOTEMPTY   Directory not empty
  EADDRINUSE  Address already in use
  EISCONN	    Transport endpoint is already connected 
  """

  def __init__(self,*args,**kwds):
    OSError.__init__(self,*args,**kwds)


class NotExistError(OSError):
  """
  Requested object or resource does not exists.

  Same as: NotFound,

  System error mapping:
    * ENOMEDIUM   No medium found
    ENOPKG	    Package not installed
    -> NotExistsError
    ENOENT	     No such file or directory
    -> NotExitsError
    ESRCH	     No such process
    -> NoExitsError
    ENXIO	     No such device or address
    -> NotExitsError
    ECHILD	    No child processes
    -> NotExitsError
    ENODEV	    No such device
    -> NotExistsError
    EIDRM	    Identifier removed
    -> NotExistsError
    ENOANO	    No anode
    ENODATA	    No data available 
    ENOPROTOOPT Protocol not available
    ENOTCONN    Transport endpoint is not connected
    ESHUTDOWN   Cannot send after transport endpoint shutdown
    EHOSTDOWN   Host is down 
  """

  def __init__(self,*args,**kwds):
    OSError.__init__(self,*args,**kwds)



class SecurityError(OSError):
  """
  Requester has no premission to perform a operation. It depends the
  implementation how much information is included in exception. Here
  no information in this excepotion is accepptable case.

  EPERM	     Operation not permitted
  -> SecurityError
  EACCES	    Permission denied
  -> SecurityError
  ECONNREFUSED Connection refused 
  """

  def __init__(self,*args,**kwds):
    OSError.__init__(self,*args,**kwds)


class AccessError(OSError):
  """
  The requested object is not acceesable from some reason. For example
  missing path, no floppy, disk not mounted. Missing access method.
  ELIBACC	    Can not access a needed shared library
  EHOSTUNREACH No route to host
  EROFS	    Read-only file system
  -> AccessError
  ELIBEXEC    Cannot exec a shared library directly
  ENETDOWN    Network is down 
  ENETUNREACH Network is unreachable
  EADDRNOTAVAI Cannot assign requested address 

  """

  def __init__(self,*args,**kwds):
    OSError.__init__(self,*args,**kwds)


class BusyError(IOError):
  """
  The requested object is too busy to complete operation. Wait and try again.
  EAGAIN	    Try again
   -> BusyError
  EBUSY	    Device or resource busy
  -> BusyError
  ETXTBSY	    Text file busy
  -> BusyError

  """

  def __init__(self,*args,**kwds):
    IOError.__init__(self,*args,**kwds)

class TimeoutError(IOError):
  """
  The requested operation is pending and cannot completed in certain
  time.

  The diffrence between TimeoutError and BusyError is that on BusyError
  the object alread on invocatio of operation declares it cannot complete
  operation, and on TimeoutError operation is going but nothing happens.

  ETIMEDOUT   Connection timed out
  -> TimeoutError
  ETIME	    Timer expired 

  """

  def __init__(self,*args,**kwds):
    IOError.__init__(self,*args,**kwds)


class InterruptError(IOError):
  """
  The requested operation has been interrupted.

  EINTR	     Interrupted system call
  -> InterrruptError
  EPIPE	    Broken pipe
  ENETRESET   Network dropped connection because of reset
  ECONNABORTED Software caused connection abort
  ECONNRESET  Connection reset by peer 
  """

  def __init__(self,*args,**kwds):
    IOError.__init__(self,*args,**kwds)


class TooLargeError(IOError):
  """
  The object is too large for target context, as a result for this operation.
  For example downloaded file does not fit into disc space.
  EFBIG	    File too large
  EOVERFLOW   Value too large for defined data type
  ELIBMAX	    Attempting to link in too many shared libraries
  EMSGSIZE    Message too long
  ETOOMANYREFS Too many references: cannot splice 
  """

  def __init__(self,*args,**kwds):
    IOError.__init__(self,*args,**kwds)


class NoSpaceError(IOError):
  """
  The resource has been exhausted to provide further system
  functionality. For example exhaustion of the memory.

  The difference between TooLargeError and NoSpace error is that
  on TooLagerError resource exhaustion is made by operation and
  on NoSpaceError resource exhaustio is made by external unknown
  factor.

  System mapping:
   * EDQUOT	    Quota exceeded
   ENOMEM	    Out of memory
   -> MemoryError
   ENOSPC	    No space left on device
   -> NoSpaceError
   ENFILE	    File table overflow
   EMFILE	    Too many open files
   ENOSR	    Out of streams resources
   EUSERS	    Too many users
   ENOBUFS	    No buffer space available 
  """

  def __init__(self,*args,**kwds):
    IOError.__init__(self,*args,**kwds)


class LoopError(OSError):
  """
  Loop (cycle) has been detected on graph that should be acyclic.
  EMLINK	    Too many links
 -> LoopError
 ELOOP	    Too many symbolic links encountered
 -> LoopError
 
  """

  def __init__(self,msg,node,**kwds):
    self.node = node
    OSError.__init__(self,msg,**kwds)


class DeadlockError(OSError):
  """
  Deadlock has been detected on the system.
  EDEADLK	    Resource deadlock would occur
  -> DeadlockError
  ESTALE	    Stale NFS file handle 
  """

  def __init__(self,*args,**kwds):
    OSError.__init__(self,*args,**kwds)


class LivelockError(OSError):
  """
  Livelock has been detected on the system.
  """

  def __init__(self,*args,**kwds):
    OSError.__init__(self,*args,**kwds)


class NotUniqueError(NameError):
  """
  The requested object,name or reference is not unique in context
  where unique thing is needed.
  ENOTUNIQ    Name not unique on network 
  """
  
  def __init__(self,*args,**kwds):
    NameError.__init__(self,*args,**kwds)


class NotSupportedError(RuntimeError):
  """ Requested functionality not supported.

  Difference to the RuntimeError. This is a RuntimeError specialized
  to the declaration that the requested functionality is not
  supporteed by purpose.

  Difference to the NotImplementedError. NotImplemented error is
  a "fault" in interface and implementation contract. NotSupportedError
  can be think not to be "fault". The system itself is that kind the
  functionality cannot be supported.

  EPROTONOSUPPORT	Protocol not supported 
  ESOCKTNOSUPPORT	Socket type not supported 
  EOPNOTSUPP  Operation not supported on transport endpoint
  EPFNOSUPPORT Protocol family not supported 
  EAFNOSUPPORT Address family not supported by protocol 
  ENAVAIL	    No XENIX semaphores available 
  ENOSYS	    Function not implemented  
  """

  def __init__(self,*args,**kwds):
    RuntimeError.__init__(self,*args,**kwds)


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

