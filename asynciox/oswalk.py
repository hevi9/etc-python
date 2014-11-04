
import asyncio # https://docs.python.org/3/library/asyncio.html
import os

root_path = os.environ["HOME"]

def make_walk(root_path):
  for dir, dirs, files in os.walk(root_path):
    print(dir)

@asyncio.coroutine
def make_walk2(root_path):
  for dir, dirs, files in os.walk(root_path):
    print(dir)
    yield from asyncio.sleep(1)


@asyncio.coroutine
def make_walk3(root_path):
  for dir, dirs, files in os.walk(root_path):
    print("***",dir)
    yield from asyncio.sleep(2)

    
#   gen = os.walk(root_path)
#   dir, dirs, files = (yield from gen)
#   print(dir)
    
# loop = asyncio.get_event_loop()
# loop.run_until_complete(make_walk2(root_path))
# loop.close()
 
 
loop = asyncio.get_event_loop()

asyncio.async(make_walk2(root_path))
asyncio.async(make_walk3(root_path))
loop.run_forever()

loop.close()
 
    
#make_walk(root_path)
  
  
  
  