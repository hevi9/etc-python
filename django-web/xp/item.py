#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2009 Petri Heinilä, License LGPL 2.1
__tags__      = "module"
__version__   = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__   = "$Release$"
__docformat__ = "epytext"
"""
1. Names
2. Questions
2.1. Navigation items ?
"""

##############################################################################
## Uses
#import sys
#import os
import logging
log = logging.getLogger(__name__)
__all__ = list()

#############################################################################
## Item

class Item(object):
  """
  Explored and managed item.
  @see: ItemStore
  """
  def name(self): raise NotImplementedError()
  def type_str(self): return "item"
  def type_char(self): return "i"

  
__all__.append("Item")

#############################################################################
## File

class File(Item):
  """
  Item presenting file system file.
  @see: FileStore.
  @tags: abstract
  """
  def name(self): raise NotImplementedError()
  def type_str(self): return "file"
  def type_char(self): return "f"


__all__.append("File")

#############################################################################
## User

class User(Item):
  """
  Authenticated entity to do authorized actions.
  @see: UserStore.
  """
  def name(self): raise NotImplementedError()
  def type_str(self): return "user"
  def type_char(self): return "U"


__all__.append("User")


#############################################################################
## Reg

class Reg(File):
  """
  Regular file.
  """
  def name(self): raise NotImplementedError()
  def type_str(self): return "reqular"
  def type_char(self): return "R"


__all__.append("Reg")

#############################################################################
## Reg

class RegTyped(File):
  """
  Regular file.
  """
  def name(self): raise NotImplementedError()
  def type_str(self): return "typed"
  def type_char(self): return "T"


__all__.append("Reg")

#############################################################################
## Dir

class Dir(File):
  """
  Directory file. Contains files.
  """
  def name(self): raise NotImplementedError()
  def type_str(self): return "directory"
  def type_char(self): return "D"


__all__.append("Dir")


#############################################################################
## Link

class Link(File):
  """
  Link file. Symbolic link.
  """
  def name(self): raise NotImplementedError()
  def type_str(self): return "link"
  def type_char(self): return "L"

__all__.append("Link")


#############################################################################
## OtherFile

class OtherFile(File):
  """
  Other file; no regular, directory or link. Non managed. 
  """
  def name(self): raise NotImplementedError()
  def type_str(self): return "other"
  def type_char(self): return "O"


__all__.append("OtherFile")




