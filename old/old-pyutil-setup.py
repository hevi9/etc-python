#!/usr/bin/env python
## $Id: setup.py,v 1.3 2005-12-05 15:52:05 hevi Exp $
## INSTALL

######################################################################
## dependencies

from distutils.core import setup
import os
p = os.path
import shutil as sh

def nosetup(**kwds): pass

tmpdir = p.join("build","tmp")

def bin_files():
  files = list()
  try:
    os.makedirs(tmpdir)
  except:
    pass
  for file in os.listdir("bin"):
    name,ext = p.splitext(file)
    if ext == ".py":
      sh.copy(p.join("bin",file),p.join(tmpdir,name))
      files.append(p.join(tmpdir,name))
  return files

def version():
  rs = open("VERSION")
  s = rs.read()
  rs.close()
  s.strip()
  return s

######################################################################
## define and run

setup(
  name = "pyutil",
  version = version(),
  package_dir = {"": "lib"},
  packages = ["pyutil"],
  scripts = bin_files()
  )

######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
