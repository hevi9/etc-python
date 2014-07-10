#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1

"""
setups - setup.py utilities
===========================
"""

import os
j = os.path.join
from hevi_lib.modules import module_name, import_file
from hevi_lib.files import find_tree_match
import sys
import logging
log = logging.getLogger(__name__)
D = log.debug

def is_ignore(f):
  """ Is file or directory to be ignored. Monkey patch this function for
  own ignore matching. 
  """
  if f == "__pycache__": return True
  if f == ".gitignore": return True
  if f == ".git": return True
  if f == ".svn": return True
  if f == ".hg": return True
  return True

def is_python(f):
  """ Is a python file ?"""
  if f.endswith(".py"): return True
  return False

def package_data(pkg):
  """ All files inside python package, except python and ingnored files. """
  result = list()
  for path, dirs, files in os.walk(pkg):
    ## remove ignores
    for dir in dirs:
      if is_ignore(dir): dirs.remove(dir)
    for file in files:
      if is_ignore(file): files.remove(file)
    ## remove python
    for file in files:
      if is_python(file): files.remove(file)
    ## add to results
    result.append(j(path,file))
  return result

# TODO: use package name on main() if file is __init__
def console_scripts(pkg):
  """ Find out console script entries from a python package. Entry is a
  regular function that is **main()** or prefixed by **main_**. Return list of 
  str by console_script format. """
  D("console_scripts() pkg={}".format(pkg))
  result = list()
  files = find_tree_match(pkg, "*.py")
  if len(files) == 0:
    print("No files found from pkg={}".format(pkg))
    return result
  for file in files:
    globals = dict()
    with open(file,"rb") as fd:
      exec(compile(fd.read(), file, "exec"), globals)
    for id in globals:
      if id.startswith("main") and callable(globals[id]):
        if id == "main":
          program = os.path.basename(os.path.splitext(file)[0])
        elif id.startswith("main_") and len(id) > len("main_"):
          program = id[len("main_"):]
        else:
          print("ignoring console_script entry {}:{}".format(file,id))
          continue
        program = "-".join(program.split("_"))
        entry = "{} = {}:{}".format(program,module_name(file),id)
        print("found entry: {}".format(entry))
        result.append(entry)
  return result
  
def main_doccat():
  """ A program (console_script) entry. Concatenate python module 
  docstring into one output.  
  """
  sys.path.insert(0, ".")
  docs = list()
  for f in sys.argv[1:]:
    m = import_file(f)
    #log.debug(m)
    if m.__doc__:
      docs.append(m.__doc__)
  print("\n\n".join(docs))


