import logging
log = logging.getLogger(__name__)

class With():
  
  def __init__(self):
    log.debug("__init__")

  def __enter__(self):
    log.debug("__enter__ => int")
    return int()
  
  def __exit__(self,type,value,traceback):
    log.debug("__exit__")

w2 = With()

def main():
  with With() as w:
    str()
  with w2:
    str()
    
with target("wayland"):
  need("juuei")
  get("repo")
  cd("joo")
  autoconf("")
  make()
  make_install()
  
with target("clean"):
  rm("-rf","build")
  
with target("actions"):
  def f1():
    pass
  fed(f1)


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  main()