from multiprocess import Process, Manager
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
    def __init__(self, Num_Process = 4):
        self.Procc = Num_Process
        self.batch_size = 32
        self.manager = Manager()

        self.Network = Client()
        self.ModelClass = Model()

        # Vector of workers
        self.workersHome = {}

        #It is going to upload the model to the main coordinator
        #Status 
        
        #NI - Model not Installed
        #MNU - Model not uploaded to main coordinator after changes made with workers
        #MU - It has the version that was grabbed from the coordinator
        
        self.modelUpdated = "NI"
        
        self.modelCoordinator = 1
        # Waiting, Working, Finished
        self.statusWorkers = self.manager.dict()
        # Dictionary in which the models are stored
        self.models = self.manager.dict()

        self.initWorkers()

    def initWorkers(self):
        for index in range(self.Procc):
            self.statusWorkers[index] = "Waiting"

            self.workersHome[index] = Process(target=self.training, args=(index, MINIEPISODES, self.modelCoordinator, self.statusWorkers, self.models))
            self.workersHome[index].start()

    def merge_networks(self, newModel):
        # Assuming net1 and net2 have the same architecture
        newNet = self.ModelClass._build_model()

        weights1 = self.model.get_weights()
        weights2 = newModel

        newWeights = [(w1 + w2) / 2.0 for w1, w2 in zip(weights1, weights2)]
        newNet.set_weights(newWeights)

        self.modelCoordinator = newNet

    # Index: The index of the device
    # Episodes: Amount of episodes for the process to train
    # Model: The model to use to train
    # Status: To insert the status of work
    # Models: To store the model

    def training(self, Index, Episodes, Model, Status, Models):        

        while True:
            if Status[Index] == "Waiting":
                Status[Index] = "Working"

                env = BJEnvironment()
                agent = DQNAgent(env.state_size, env.action_size, 0.01, Episodes, self.batch_size, "./models/v{VERSION}/logs".format(VERSION=VERSION))

                # agent.model = Model

                for Episode in range(Episodes):
                    print("Process {Process} in episode: {Episode}".format(Process=Index, Episode=Episode))
                    agent.train(env, False)

                Models[Index] = agent.model
                Status[Index] = "Finished"

            sleep(1)

            if Status[Index] == "Stop":
                break

    def factory(self):
        workersFinished = False

        while True:

            for index in range(self.Procc):
                if self.statusWorkers[index] == "Finished":
                    print("Process {index} has finished".format(index= index))
                    print(self.models[index].get_weights())
            sleep(1)
            
            workersFinished = True
            for index in range(self.Procc):
                if self.statusWorkers[index] == "Working":
                    workersFinished = False
            
            if self.modelUpdated == "NI":
                #DownloadModelFromCoord
                newMod = Client.receiveArray(self.modelCoordinator.get_weights())
                self.modelCoordinator = newMod
                
            elif self.modelUpdated == "MNU":
                #See if all the workers have finished
                #Upload model
                newMod = Client.sendArray()
                self.modelCoordinator = newMod

            elif self.modelUpdated == "MU":
                #See if the model is updated if that so
                if workersFinished == True:
                    for index in range(self.Procc):
                        self.merge_networks(self.models[index])
            
if __name__ == "__main__": 
    worker = WorkerPC(4)
    worker.factory()
