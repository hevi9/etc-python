from bottle import route, run
from time import sleep

@route('/')
def iter():
  for i in range(0,100):
    yield "STEP"
    sleep(1)
    

run(host='localhost', port=8080)
