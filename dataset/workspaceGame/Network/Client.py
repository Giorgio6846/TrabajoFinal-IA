import socket
import numpy as np
import pickle

VERSIONUPDATE = 0

# Types of JSON CLIENT
# Type:
# 1 - Receive new array
# 2 - Send array
# ModelWeights:
# Sends the weights of the array

class Client():
    def __init__(self):
        self.port = 40674
        # self.address = "10.142.81.104"
        # self.address = "10.0.0.103"
        self.address = "172.20.10.3"

    def sendArray(self, arrayWeights, Version):
        # Message Sent
        inf = {"Type": 2, "Model": [Version, arrayWeights]}
        ServerInf = pickle.dumps(inf)

        # Message Received
        responseServer = self.connectServer(ServerInf)
        response = self.decodeMessage(responseServer)

        return response

    def receiveArray(self):
        # Message Sent
        inf = {"Type": 1}
        ServerInf = pickle.dumps(inf)

        # Message Received
        responseServer = self.connectServer(ServerInf)
        response = self.decodeMessage(responseServer)

        return response

    def connectServer(self,pickleInf):    
        s = socket.socket()

        s.connect((self.address, self.port))

        s.send((pickleInf))

        buffer = b''
        while True:
            response = s.recv(1024)  
            if not response:
                break
            buffer += response

        res: dict
        try:
            res = pickle.loads(buffer)
        except:
            raise ConnectionError(
                f"Invalid JSON recived from server")

        s.close()

        return res

    def decodeMessage(self, response):
        responseServer = dict()        

        for key, value in response.items():
            if key == "ModelWeights":
                weights = [np.array(weight) for weight in value]
                responseServer["ModelWeights"] = weights
            elif key == "Version":
                responseServer["Version"] = value

        return responseServer
