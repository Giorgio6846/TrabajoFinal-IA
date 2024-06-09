# Thanks to a certain person
from multiprocess import Process, Pipe, Array
from time import sleep
import tensorflow as tf

from Blackjack.Tools import Model
from Blackjack.Agent import DQNAgent
from Blackjack.Environment import BJEnvironment
from Network.Client import Client

VERSION = 2
COMPLETEDVERSION = 1
MINIEPISODES = 50


class WorkerPC:
    def __init__(self, Num_Process=4):
        self.Procc = Num_Process
        self.batch_size = 32

        env = BJEnvironment()
        ModelClass = Model()

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
        self.workerInf = {}

        # Data sent to process
        self.modelCoordinator = dict()

        self.modelCoordinator["Model"] = ModelClass._build_model(
            env.state_size, env.action_size
        )
        self.modelCoordinator["Version"] = 0

        # Status
        # MNI - Model not Installed from coordinator
        # MNU - Model not uploaded to main coordinator after changes made with workers
        # MU  - It has the lastest version that was grabbed from the coordinator
        self.modelCoordinator["Status"] = "MNI"
        self.initWorkers()

    def initWorkers(self):
        for index in range(self.Procc):
            factoryConnection, childConnection = Pipe(duplex=True)

            self.workerInf[index] = ["Waiting", self.modelCoordinator["Status"], self.modelCoordinator["Model"].get_weights()]

            self.workersCommunication[index] = [factoryConnection, childConnection]

            self.workersHome[index] = Process(
                target=self.training,
                args=(
                    index,
                    MINIEPISODES,
                    self.batch_size,
                    self.workersCommunication[index][1],
                ),
            )

            self.workersHome[index].start()
            self.workersCommunication[index][0].send(self.workerInf[index])

    def merge_networks(self, newModel):

        # Assuming net1 and net2 have the same architecture
        newNet = tf.keras.models.clone_model(self.modelCoordinator["Model"])
        weights1 = self.modelCoordinator["Model"].get_weights()
        weights2 = newModel

        newWeights = [(w1 + w2) / 2.0 for w1, w2 in zip(weights1, weights2)]

        self.modelCoordinator["Model"].set_weights(newWeights)

    # Index: The index of the device
    # Episodes: Amount of episodes for the process to train
    # Status: To insert the status of the worker
    # Models: Where the workers store their models
    # ModelState: The state of the model of the factory to renew the model of the worker

    def training(self, Index, BatchSize, Episodes, connection):
        env = BJEnvironment()
        agent = DQNAgent(
            env.state_size, env.action_size, 0.01, BatchSize, VERSION
        )

        while True:
            if connection.poll():
                workerInf = connection.recv()

            if workerInf[0] == "Waiting":
                workerInf[0] = "Working"

                if workerInf[1] == "MU":
                    agent.model.set_weights(workerInf[2])

                connection.send(workerInf)  

                for Episode in range(Episodes):
                    print(f"Process {Index} in episode: {Episode}")
                    agent.train(env, False)

                workerInf[1] = agent.model.get_weights()
                workerInf[0] = "Finished"

            connection.send(workerInf)    
            sleep(1)

            if workerInf[0] == "Stop":
                break

    def receiveDataProcess(self):
        for index in range(self.Procc):
            if self.workersCommunication[index][0].poll():
                self.workerInf[index] = self.workersCommunication[index][0].recv()

    def sentDataProcess(self):
        for index in range(self.Procc):
            self.workersCommunication[index][0].send(self.workerInf[index])

    def factory(self):
        while True:
            self.receiveDataProcess()

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
                newModel = self.Network.sendArray(self.modelCoordinator["Model"].get_weights())
                self.updateModel(newModel)

                if workersWaiting == True:
                    for index in range(self.Procc):
                        self.workerInf[index][2] = self.modelCoordinator["Model"].get_weights()
                        self.workerInf[index][1] = "MU"

                self.modelCoordinator = "MU"

            elif self.modelCoordinator["Status"] == "MU":
                # See if the model is updated if that so
                if workersFinished == True:
                    for index in range(self.Procc):
                        self.merge_networks(self.workerInf[index][2])
                    self.modelCoordinator["Status"] = "MNU"

            self.sentDataProcess()

    def updateModel(self, newModel):
        self.modelCoordinator["Version"] = newModel["Version"]
        self.modelCoordinator["Model"].set_weights(newModel["ModelWeights"])

if __name__ == "__main__":
    worker = WorkerPC(4)
    worker.factory()
