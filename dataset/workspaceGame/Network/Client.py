# Import socket module
import socket
import json
import numpy as np

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
        #self.address = "10.142.81.104"
        self.address = "10.0.0.105"
        #self.address = "172.20.10.3"
        
    def sendArray(self, arrayWeights):
        # Message Sent
        arrayList = self.modelWeightList(arrayWeights)
        inf = {"Type": 2, "Arr": arrayList}
        ServerInf = json.dumps(inf)

        # Message Received
        responseServer = self.connectServer(ServerInf)
        response = self.decodeMessage(responseServer)

        return response

    def modelWeightList(self, arrayWeights):
        arrayToList = [
            weight.tolist() for weight in arrayWeights["Model"].get_weights()
        ]
        return arrayToList
        
    def receiveArray(self):
        # Message Sent
        inf = {"Type": 1}
        ServerInf = json.dumps(inf)

        # Message Received
        responseServer = self.connectServer(ServerInf)
        response = self.decodeMessage(responseServer)

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

    def decodeMessage(self, response):
        dataDict = json.loads(response)
        #print(dataDict)

        responseServer = dict()        

        for key, value in dataDict.items():
            if key == "ModelWeights":
                weights = [np.array(weight) for weight in value]
                responseServer["ModelWeights"] = weights
            elif key == "Version":
                responseServer["Version"] = value

        return responseServer
