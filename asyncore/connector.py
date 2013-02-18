import socket
import select
import asyncore

class Connector(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.debug = True
        self.buffer = bytes("hi","ascii")
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Connector.connect(({},{}))".format(host,port))
        self.connect((host, port))

    def handle_connect(self):
        print("handle_connect()") # not called <------------------

    def handle_read(self):
        print("handle_read()")
        self.recv(4096)
        self.close()

    def writable(self):
        print("writable()")
        return len(self.buffer) > 0 # remember RETURN

    def handle_write(self):
        print("handle_write()")
        sent = self.send(self.buffer)
        print("send({})".format(self.buffer[0:sent]))
        self.buffer = self.buffer[sent:]

    def handle_close(self):
        print("handle_close()")
        self.close()


connector = Connector("localhost", 12000) #  Handler()
print("asyncore.loop() enter")
asyncore.loop() 
print("asyncore.loop() leave")