#!/usr/bin/env python3

import logging # http://docs.python.org/3.2/library/logging.html
log = logging.getLogger(__name__)
import asyncore # http://docs.python.org/3.2/library/asyncore.html

##

class EchoServer(asyncore.dispatcher_with_send):
  
  def __init__(self):
    super().__init__()

##
logging.basicConfig(format="[%(name)s|%(thread)d] %(message)s",level=logging.DEBUG)
server = EchoServer()

log.debug("loop enter")
asyncore.loop(1.0)
log.debug("loop leave")

logging.