import os
import base64
import time
from sympy import proper_divisor_count
import zmq
import json

import server.CardDetection.model as cardModel
import server.GamePrediction.model as gameModel

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

file_path = os.path.join(os.path.dirname(__file__), "screenshots", "received_image.png")

class Server:
    def __init__(self):
        pass
        
    def parseJSON(self, message):
        try:
            if "image" in message:
                self.process_image(message["image"])
                file_path = os.path.join(os.path.dirname(__file__), "screenshots", "received_image.png")

                cardsDealer, cardsPlayer = cardModel.detectCards(file_path)
                prediction = gameModel.gamePrediction(cardsDealer,cardsPlayer)

                predictionArray = ["hit", "stay", "split", "double"][prediction]

                socket.send_string(json.dumps({"response": "image processed"}))
            else:
                socket.send_string(json.dumps({"response": "unknown type"}))
        except Exception as e:
            socket.send_string(json.dumps({"error": str(e)}))

    def process_image(self, base64_string):
        try:
            image_data = base64.b64decode(base64_string)
            with open(file_path, "wb") as f:
                f.write(image_data)
            return True
        except Exception as e:
        # Maneja errores en la decodificación o escritura de la imagen
            print(f"Error processing image: {str(e)}")
            return False
        
server = Server()

print("Server ready")

while True:
    try:
        message = socket.recv_json()
        print("Received request: %s" % type(message))
        server.parseJSON(message)
        print("Message Sent")
    except zmq.ZMQError as e:
        print("ZMQ Error:", e)
    except Exception as e:
        print("General Error:", e)