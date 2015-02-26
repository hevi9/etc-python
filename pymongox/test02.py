from pymongo import MongoClient
import time

connection = c = MongoClient()

print("Connect to", c.host,
      "port", c.port, 
      "alive" if c.alive() else "dead")
for k, v in c.server_info().items():
  print(" *",k,"=",v)

col = connection.MEGATEST6.things

data = "X" * (15*1024*1024)

print(len(data))

time_insert_start = time.time()

col.insert({"data": data})

time_insert_end = time.time()


time_find_start = time.time()

print(col)

res = col.find()
  
time_find_end = time.time()

connection.close()

print("Insert ", time_insert_end - time_insert_start)
print("Find ", time_find_end - time_find_start)
