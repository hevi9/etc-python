import sys
import os

from etc.util import *

sys.path.insert(0, ".")

docs = list()

for f in sys.argv[1:]:
  m = import_file(f)
  #print(m)
  if m.__doc__:
    docs.append(m.__doc__)
  
print("\n\n".join(docs))