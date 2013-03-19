import sys
import os
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

sys.path.insert(0, ".")
from etc.util import *

docs = list()

log.debug("HERE")

for f in sys.argv[1:]:
  m = import_file(f)
  #log.debug(m)
  if m.__doc__:
    docs.append(m.__doc__)
  
print("\n\n".join(docs))

