import sys
import os

__all__ = list()

sys.path.insert(0, ".")

def import_file(f):
  """ import file """
  parts = f.split(os.sep)
  parts[-1] = os.path.splitext(parts[-1])[0]
  if parts[-1] == "__init__":
    del parts[-1]
  mn = ".".join(parts)
  top =  __import__(mn)
  parts.pop(0)
  while len(parts) > 0:
    top = getattr(top,parts[0])
    parts.pop(0)
  return top

__all__.append("import_file")

def module_name(f):
  """ file name to module name """
  parts = f.split(os.sep)
  parts[-1] = os.path.splitext(parts[-1])[0]
  if parts[-1] == "__init__":
    del parts[-1]
  mn = ".".join(parts)
  return mn

__all__.append("module_name")


