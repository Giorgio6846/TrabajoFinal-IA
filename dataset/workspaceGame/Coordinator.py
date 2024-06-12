from multiprocess import Process, Manager
import tensorflow as tf
import socket
import threading
import json
import numpy as np

from Blackjack.Tools import Model
from Blackjack.Environment import BJEnvironment

# Types of JSON Coordinator to Send
# Version:
#  Send the actual version of the array
# ModelWeights:
#  Sends the weights of the array

# From self.model Dict
# {Version: Version of the model}
# {ModelWeights: The weights of the model}

VERSION = 4
COMPLETEDVERSION = 1

SAVEMODELAMOUNT = 2

class Coordinator:
    def __init__(self):
        env = BJEnvironment()
        self.ModelClass = Model(env.state_size, env.action_size)

        self.host = ""
        self.buffer_size = 30_000_000
        self.port = 40674

        self.model = dict()

        self.model["Model"] = tf.keras.models.clone_model(self.ModelClass.model)
        self.model["Version"] = 0

        # Create socket for connections
        self.serverSocket = socket.socket()
        self.serverSocket.bind(("", self.port))

        print("socket binded to %s" % (self.port))
        self.serverSocket.listen(10)
        print("[INFO] Server started on {}".format(self.host, self.port))

    # Server Functions
    def startServer(self):
        while True:
            client_socket, client_address = self.serverSocket.accept()
            print(
                "[INFO] Connected to {}:{}".format(client_address[0], client_address[1])
            )
            client_thread = threading.Thread(target = self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            data = self.getData(client_socket)

            data_json = json.loads(data.decode())

            self.executeRequest(client_socket,data_json)
            break

        client_socket.close()
        print("[INFO] Disconnected from client, request succeded")

    def start(self):
        server_thread = threading.Thread(target = self.startServer)
        server_thread.start()

        while True:
            try:
                pass
            except KeyboardInterrupt:
                break

        print("Stopping the server")
        server_thread.join()
        print("Server Stopped")

    def getData(self, client_socket):
        client_socket.settimeout(3)

        try:
            data = client_socket.recv(self.buffer_size)
        except socket.timeout:
            data = b''

        return data

    def executeRequest(self, client_socket, data_json):
        dataDict = json.loads(data_json)
        print(dataDict)

        valDict = 1
        for key, value in dataDict.items():
            if key == "Type":
                if value == 1:
                    valDict = 1
                    print("Sent model")
                    self.sendModel(client_socket)    

                elif value == 2:
                    valDict = 2

            if key == "Model":
                if valDict == 2:
                    print("Merged model")

                    self.merge_networks(value[1])

                    self.sendModel(client_socket) 

    def sendModel(self, client_socket):
        response = dict()
        response["Version"] = self.model["Version"]
        arrayToList = [weight.tolist() for weight in self.model["Model"].get_weights()]
        response["ModelWeights"] = arrayToList
        response_json = json.dumps(response)

        self.send_response(client_socket, response_json)

    def send_response(self, client_socket, response):
        response_json = json.dumps(response)
        client_socket.send(response_json.encode())

    def merge_networks(self, workerModelWeights):
        # Assuming net1 and net2 have the same architecture
        if self.model["Version"] % SAVEMODELAMOUNT == 0 and self.model["Version"] != 0:
            self.saveMainModel()

        weights1 = self.model["Model"].get_weights()
        weights2 = workerModelWeights

        newWeights = [(w1 + w2) / 2.0 for w1, w2 in zip(weights1, weights2)]

        self.model["Model"].set_weights(newWeights)
        self.model["Version"] = self.model["Version"] + 1

    def saveMainModel(self):
        self.saveModel.saveModel(self.model, VERSION, COMPLETEDVERSION)
        COMPLETEDVERSION = COMPLETEDVERSION + 1

if __name__ == "__main__":
    Coord = Coordinator()
    Coord.start()
