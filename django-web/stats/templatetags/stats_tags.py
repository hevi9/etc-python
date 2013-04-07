#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2009 Petri Heinilä, License LGPL 2.1
__tags__      = "module"
__version__   = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__   = "$Release$"
__docformat__ = "epytext"
"""
"""

##############################################################################
## Uses
#import sys
#import os
import logging
log = logging.getLogger(__name__)
from django import template

register = template.Library()

#############################################################################
## tags

@register.filter
def mib(n):
  return "%0.1fMiB" % (n / (1024.0*1024))

@register.filter
def kib(n):
  return "%0.1fKiB" % (n / (1024.0))



