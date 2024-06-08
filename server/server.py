import time
import zmq
import networkx as nx

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

class Server:
    def __init__(self):
        print()
        
    def parseJSON(self, message):
        if message["type"] == "test":
            socket.send_string("true")
        
classServer = Server()

print("Ready")

while True:
    message = socket.recv_json()
    print("Received request: %s" % message)
    
    classServer.parseJSON(message)
    
    print("Message Sent")
    
    time.sleep(1)