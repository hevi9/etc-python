
import logging
log = logging.getLogger(__name__)
D = log.debug

def main():
  a = 10
  b = "jeejee"
  D("main a=%(a)s b=%(b)s",locals())
  
def main2():
  d = {
    "a": 10,
    "b": "jeejee"
  }
  D("main a=%(a)d b=%(b)s",d)
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  main()
  main2()