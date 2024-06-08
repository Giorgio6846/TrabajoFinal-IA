import socket
import threading 
import json

class Server:
    def __init__(self, model, version):

       

        self.model = model
        self.version = version

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
            try:
                data_json = json.loads(data.decode())
                
            self.execute_request(client_socket,data_json)

    def getData(self, client_socket):
        client_socket.settimeout(3)
        
        try:
            data = client_socket.recv(self.buffer_size)
        except socket.timeout:
            data = b''
            
        return data
    
    def send_response(self, client_socket, response):
        response_json = json.dumps(response)
        client_socket.send(response_json.encode())
        
    def execute_request(self, client_socket, method_funciotns)