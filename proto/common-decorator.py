#!/usr/bin/env python
# -*- coding: utf-8 -*-
## $Id$
## MAIN

import logging
log = logging.getLogger(__name__)
import hevi_util.main as hum

def export(func):
  """ Decorator export. Exports function name out of the module.
  """
  if not "__all__" in globals():
    global __all__
    __all__ = list()
  __all__.append(func.__name__)
  return func

@export
def test():
  pass

@export
def test2():
  pass


def run():
  log.debug(test)
  
print __all__
  
if __name__ == "__main__":
  main = hum.Main(run=run,debug=True)
  main.start()
  