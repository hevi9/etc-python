import sys
import os

sys.path.insert(0, ".")

docs = list()

def import_file(f):
  """ file name to module name """
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

for f in sys.argv[1:]:
  m = import_file(f)
  #print(m)
  if m.__doc__:
    docs.append(m.__doc__)
  
print("\n\n".join(docs))