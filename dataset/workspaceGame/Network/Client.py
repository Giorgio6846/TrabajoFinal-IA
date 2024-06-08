# Import socket module
import socket
import json

VERSIONUPDATE = 0

# Types of JSON CLIENT
# Type:
# 1 - Receive new array
# 2 - Send array
# Arr:
# Sends the weights of the array

class Client():
    def __init__(self):
        self.port = 40674
        self.address = "10.0.0.105"

    def sendArray(self,array):
        inf = {"Type:": 2, "Arr": array}
        ServerInf = json.dumps(inf)

        response = self.connectServer(ServerInf)
        return response

    def receiveArray(self):
        inf = {"Type:": 1}
        ServerInf = json.dumps(inf)

        response = self.connectServer(ServerInf)
        return response

    def connectServer(self,jsonServer):    
        s = socket.socket()

        s.connect((self.address, self.port))

        s.send(json.dumps(jsonServer).encode())

        buffer = b''
        while True:
            response = s.recv(1024)  
            if not response:
                break
            buffer += response

        res: dict
        try:
            res = json.loads(buffer.decode())
        except:
            raise ConnectionError(
                f"Invalid JSON recived from server")

        s.close()

        return res
