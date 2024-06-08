from multiprocess import Process, Manager
import tensorflow as tf
import socket
import threading
import json

from Blackjack.Tools import SaveModel, Model

# Funcions
# - Global Coordinator
# - Center Coordinator

# Types of JSON Coordinator
# Ver:
#  Send the actual version of the array
# Arr:
#  Sends the weights of the array

# Coordinator & Server
# Are going to work at the same time in different process in which their are
# going to to be communicating via an array

# From self.model Dict
# {Version: Version of the model}
# {Model: The weights of the model}

# Mode
MODE = 1

VERSION = 2
COMPLETEDVERSION = 1

SAVEMODELAMOUNT = 10

class Coordinator:
    def __init__(self, stateSize, actionSize, episodes, batchSize):
        self.modelCreate = Model()
        self.saveModel = SaveModel()

        self.buffer_size = 30_000_000
        self.port = 40674

        self.episodes = episodes
        self.batchSize = batchSize      

        self.model["Model"] = self.ModelCreate.build_model(stateSize, actionSize)
        self.model["Version"] = 0

        # Create socket for connections
        self.serverSocket = socket.socket()
        self.serverSocket.bind(("", self.port))

        print("socket binded to %s" % (self.port))
        self.serverSocket.listen(10)
        self.print("[INFO] Server started on {}".format(self.host, self.port))

    # Server Functions
    def startServer(self):
        while True:
            client_socket, client_address = self.serverSocket.accept()
            self.print(
                "[INFO] Connected to {}:{}".format(client_address[0], client_address[1])
            )
            client_thread = threading.Thread(target = self.handle_client, arg=(client_socket,))

    def handle_client(self, client_socket):
        while True:
            data = self.getData(client_socket)

            data_json = json.loads(data.decode())

            self.execute_request(client_socket,data_json)
            break

        client_socket.close()
        print("[INFO] Disconnected from client, request succeded")

    def getData(self, client_socket):
        client_socket.settimeout(3)
        
        try:
            data = client_socket.recv(self.buffer_size)
        except socket.timeout:
            data = b''
            
        return data

    def executeRequest(self, client_socket, data_json):
        print(data_json)

    def send_response(self, client_socket, response):
        response_json = json.dumps(response)
        client_socket.send(response_json.encode())

    def merge_networks(self, newModel):
        # Assuming net1 and net2 have the same architecture
        if self.modelVersion % SAVEMODELAMOUNT == 0:
            self.saveMainModel()

        newNet = tf.keras.models.clone_model(self.model)
        newNet.build(
            self.model.inputShape
        )  # Build the model with the correct input shape

        weights1 = self.model.get_weights()
        weights2 = newModel

        newWeights = [(w1 + w2) / 2.0 for w1, w2 in zip(weights1, weights2)]
        newNet.set_weights(newWeights)

        self.model["Version"] = self.model["Version"] + 1
        self.model["Model"] = newNet

    def saveMainModel(self):
        self.saveModel.saveModel(self.model, VERSION, COMPLETEDVERSION)

if __name__ == "__main__":
    s = socket.socket()
    print("Socket successfully created")

    port = 40674

    s.bind(("", port))
    print("socket binded to %s" % (port))

    s.listen(5)
    print("socket is listening")

    while True:

        c, addr = s.accept()
        print("Got connection from", addr)

        c.send(b"Thank you for connecting")

        c.close()
