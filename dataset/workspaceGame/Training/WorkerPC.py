# Thanks to a certain person
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from multiprocessing import set_start_method
from multiprocess import Process, Manager
from time import sleep
import tensorflow as tf
import threading
import numpy as np

from lib.Model.Tools import Model
from lib.Model.Agent import DQNAgent
from lib.Game.Environment import BJEnvironment
from lib.Network.Client import Client

VERSION = 8
MINIEPISODES = 200

class WorkerPC:
    def __init__(self, Num_Process=4):
        self.Procc = Num_Process
        self.batch_size = 32

        env = BJEnvironment()
        self.ModelClass = Model(env.state_size, env.action_size)

        # Handle Network Operations with Coordinator
        self.Network = Client()

        # Dictionary of workers process
        self.workersHome = {}
        self.workersCommunication = {}

        # Dictionary of the workers information
        # Status of the worker
        # Waiting, Working, Finished
        # Status of the model from the worker
        # MNI - Model not Installed from coordinator
        # MNU - Model not uploaded to main coordinator after changes made with workers
        # MU  - It has the lastest version that was grabbed from the coordinator
        # Weights of the model from the worker
        # self.workerInf = {}

        # Data sent to process
        self.modelCoordinator = dict()

        self.modelCoordinator["Model"] = tf.keras.models.clone_model(self.ModelClass.model)
        self.modelCoordinator["Version"] = 0

        # Status
        # MNI - Model not Installed from coordinator
        # MNU - Model not uploaded to main coordinator after changes made with workers
        # MU  - It has the lastest version that was grabbed from the coordinator
        self.modelCoordinator["Status"] = "MNI"
        self.managerWorker = Manager()

        set_start_method("spawn", force = True)

        self.initWorkers()

    def start(self):
        factoryThread = threading.Thread(target = self.factory)
        factoryThread.start()

    def initWorkers(self):
        self.workerInf = self.managerWorker.dict()
        for index in range(self.Procc):
            self.workerInf[index] = ["Waiting", self.modelCoordinator["Status"], self.modelCoordinator["Model"].get_weights()]

            self.workersHome[index] = Process(
                target=self.training,
                args=(
                    index,
                    self.batch_size,
                    MINIEPISODES,
                    self.workerInf,
                    VERSION
                ),
            )

    def merge_networks(self):
        # Assuming net1 and net2 have the same architecture
        modelCord = self.modelCoordinator["Model"].get_weights()

        newModels = []
        for index in range(self.Procc):
            newModels.append(self.workerInf[index][2])

        modelWorkers = np.mean([w1 for w1 in zip(newModels)], axis=0)

        newWeights = [(w1 + w2) / 2.0 for w1, w2 in zip(modelCord, modelWorkers)]

        self.modelCoordinator["Model"].set_weights(newWeights)

    # Index: The index of the device
    # Episodes: Amount of episodes for the process to train
    # Status: To insert the status of the worker
    # Models: Where the workers store their models
    # ModelState: The state of the model of the factory to renew the model of the worker

    def training(self, Index, Episodes, WorkerInf, VERSION):           
        from Blackjack.Agent import DQNAgent
        from Blackjack.Environment import BJEnvironment

        env = BJEnvironment()
        agent = DQNAgent(
            env.state_size, env.action_size, VERSION
        )

        while True:
            Array = WorkerInf[Index]

            if Array[0] == "Waiting":
                Array[0] = "Working"

                if Array[1] == "MU":
                    agent.ModelClass.model.set_weights(Array[2])

                for Episode in range(Episodes):
                    print(f"Process {Index} in episode: {Episode}")
                    agent.train(env, False)

                Array[1] = agent.ModelClass.model.get_weights()
                Array[0] = "Finished"
                print(Array[0], "Worker {index} finished".format(index = Index))

            WorkerInf[Index] = Array

            if Array[0] == "Stop":
                break

    def factory(self):      
        modelModifiedFromCoord = False

        for index in range(self.Procc):
            self.workersHome[index].start()

        while True:
            for index in range(self.Procc):
                if self.workerInf[index][0] == "Finished":
                    print(f"Process {index} has finished")
                    print(self.workerInf[index][2])
            sleep(1)

            workersFinished = all(self.workerInf[index][0] == "Finished" for index in range(self.Procc))
            workersWaiting = all(
                self.workerInf[index][0] == "Waiting" for index in range(self.Procc)
            )

            if self.modelCoordinator["Status"] == "MNI":
                # DownloadModelFromCoord
                newModel = self.Network.receiveArray()
                self.updateModel(newModel)

                self.modelCoordinator["Status"] = "MU"

            elif self.modelCoordinator["Status"] == "MNU":   
                if modelModifiedFromCoord:             
                    newModel = self.Network.sendArray(self.modelCoordinator["Model"].get_weights(), self.modelCoordinator["Version"])
                    self.updateModel(newModel)

                if workersWaiting == True:
                    for index in range(self.Procc):
                        Array = self.workerInf[index]

                        Array[2] = self.modelCoordinator["Model"].get_weights()
                        Array[1] = "MU"

                        self.workerInf[index] = Array

                modelModifiedFromCoord = False
                self.modelCoordinator["Status"] = "MU"

            elif self.modelCoordinator["Status"] == "MU":
                # See if the model is updated if that so
                if workersFinished == True:
                    for index in range(self.Procc):
                        Array = self.workerInf[index]

                        self.merge_networks(Array[2])
                        modelModifiedFromCoord = True
                        Array[0] = "Waiting"

                        self.workerInf[index] = Array

                    self.modelCoordinator["Status"] = "MNU"

    def updateModel(self, newModel):
        self.modelCoordinator["Version"] = newModel["Version"]
        self.modelCoordinator["Model"].set_weights(newModel["ModelWeights"])

if __name__ == '__main__':
    worker = WorkerPC(6)
    worker.start()
