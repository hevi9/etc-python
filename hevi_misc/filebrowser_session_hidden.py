#!/usr/bin/env python
# -*- coding: utf-8 -*-
## $Id$
## MODULE

class Session(object):
  
  def __init__(self):
    pass
  
  def hidden_files(self):
    """ Fnmatch patterns to hide files.
    @return: list of fnmatch pattern strings
    """
    return [".*",]