simeb 
=====

-- SImple MEssage Bus example by asyncio and json message coding


simeb broadcasts messages (as functions) along the bus between
processes (local or remote).

Example echo_service.py::

  import asyncio
  from simeb import get_bus
  
  bus = get_bus()
  
  @bus.register
  def echo_request(text):
    print("echo_request got", text)
    bus.echo_reply(text + " TOO")
  
  if __name__ == "__main__":
    print("looping forever ..")
    asyncio.get_event_loop().run_forever()

get_bus() initializes message broker and get default bus.

@bus.register sets function to be invoked when the "echo_message" appears on bus.

bus.echo_reply() send "echo_reply" message with parameter to the bus.
  
Example start (client) program echo_start.py::

  import asyncio
  from simeb import make_link, get_bus
  
  bus = get_bus()
  
  @bus.register
  def echo_reply(text):
    print("echo_reply got", text)
    asyncio.get_event_loop().stop()
  
  @asyncio.coroutine
  def start():
    make_link()
    yield from asyncio.sleep(1)
    bus.echo_request("HELLOOO")
  
  def main():
    asyncio.Task(start())
    asyncio.get_event_loop().run_forever()
  
  if __name__ == "__main__":
    main()
   
make_link() connects to localhost bus service. asyncio.sleep() waits till
connection is made (TODO: better sync here).  
 
