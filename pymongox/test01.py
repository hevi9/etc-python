from pymongo import MongoClient
import time

connection = c = MongoClient()

print("Connect to", c.host,
      "port", c.port, 
      "alive" if c.alive() else "dead")
for k, v in c.server_info().items():
  print(" *",k,"=",v)

col = connection.MEGATEST5.things

N = 10*1000000

time_insert_start = time.time()

for i in range(0,N):
  if not i % 10000: print(i)
  col.insert({"nro": i})

time_insert_end = time.time()


time_find_start = time.time()

print(col)
for i, item in enumerate(col.find()):
  if not i % 10000: print(i, item)
  
time_find_end = time.time()

connection.close()

print("Insert ", time_insert_end - time_insert_start)
print("Find ", time_find_end - time_find_start)
