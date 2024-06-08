import threading
from time import sleep
import tensorflow as tf

from Blackjack.Tools import Model
from Blackjack.Agent import DQNAgent
from Blackjack.Environment import BJEnvironment
from Network.Client import Client

VERSION = 2
COMPLETEDVERSION = 1
MINIEPISODES = 50

# Global Variables
workersHome = {}
modelUpdated = "MNI"
model_updated_lock = threading.Lock()

modelCoordinator = {}
statusWorkers = {}
models = {}


class WorkerPC:
    def __init__(self, Num_Process=4):
        self.Procc = Num_Process
        self.batch_size = 32

        env = BJEnvironment()
        ModelClass = Model()

        # Handle Network Operations with Coordinator
        self.Network = Client()

        modelCoordinator["Model"] = ModelClass._build_model(
            env.state_size, env.action_size
        )
        modelCoordinator["Version"] = 0

        self.initWorkers()

    def initWorkers(self):
        for index in range(self.Procc):
            statusWorkers[index] = "Waiting"
            models[index] = 1

            workersHome[index] = threading.Thread(
                target=self.training, args=(index, MINIEPISODES)
            )
            workersHome[index].start()

    def merge_networks(self, newModel):
        global modelCoordinator
        newNet = tf.keras.models.clone_model(modelCoordinator["Model"])
        weights1 = newNet.get_weights()
        weights2 = newModel.get_weights()

        newWeights = [(w1 + w2) / 2.0 for w1, w2 in zip(weights1, weights2)]
        newNet.set_weights(newWeights)

        modelCoordinator["Model"] = newNet

    def training(self, Index, Episodes):
        global modelUpdated
        env = BJEnvironment()
        agent = DQNAgent(
            env.state_size, env.action_size, 0.01, self.batch_size, VERSION
        )

        while True:
            with model_updated_lock:
                if modelUpdated == "MU":
                    agent.model.set_weights(modelCoordinator["Model"].get_weights())

            statusWorkers[Index] = "Working"
            for Episode in range(Episodes):
                print(f"Process {Index} in episode: {Episode}")
                agent.train(env, False)

            models[Index] = agent.model
            statusWorkers[Index] = "Finished"

            sleep(1)
            if statusWorkers[Index] == "Stop":
                break

    def factory(self):
        global modelUpdated
        while True:
            workersFinished = all(
                status == "Finished" for status in statusWorkers.values()
            )

            for index in range(self.Procc):
                if statusWorkers[index] == "Finished":
                    print(f"Process {index} has finished")
                    print(models[index].get_weights())

            sleep(1)

            with model_updated_lock:
                if modelUpdated == "MNI":
                    newMod = self.Network.receiveArray()
                    modelCoordinator["Version"] = newMod["Version"]
                    modelCoordinator["Model"].set_weights(newMod["ModelWeights"])
                    modelUpdated = "MU"

                elif modelUpdated == "MNU":
                    newMod = self.Network.sendArray(
                        modelCoordinator["Model"].get_weights()
                    )
                    modelCoordinator["Version"] = newMod["Version"]
                    modelCoordinator["Model"].set_weights(newMod["ModelWeights"])
                    modelUpdated = "MU"

                elif modelUpdated == "MU" and workersFinished:
                    for index in range(self.Procc):
                        self.merge_networks(models[index])
                    modelUpdated = "MNU"


if __name__ == "__main__":
    worker = WorkerPC(4)
    worker.factory()
