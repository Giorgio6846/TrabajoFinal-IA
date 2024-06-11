import time
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

class Server:
    def __init__(self):
        pass
        
    def parseJSON(self, message):
        try:
            if message["type"] == "test":
                socket.send_string(json.dumps({"response": "true"}))
            else:
                socket.send_string(json.dumps({"response": "unknown type"}))
        except Exception as e:
            socket.send_string(json.dumps({"error": str(e)}))
        
server = Server()

print("Server ready")

while True:
    try:
        message = socket.recv_json()
        print("Received request: %s" % message)
        server.parseJSON(message)
        print("Message Sent")
    except zmq.ZMQError as e:
        print("ZMQ Error:", e)
    except Exception as e:
        print("General Error:", e)
    time.sleep(1)