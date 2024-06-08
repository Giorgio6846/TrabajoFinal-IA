import socket
from multiprocess import Process, Manager
from time import sleep
from Environment import BJEnvironment
from Agent import DQNAgent

VERSION = 2
COMPLETEDVERSION = 1
MINIEPISODES = 50

class WorkerPC:
    def __init__(self, Num_Process = 4):
        self.Procc = 4
        self.state_size = 3
        self.action_size = 3
        self.batch_size = 32
        self.manager = Manager()

        #Vector of workers
        self.workersHome = {}

        self.modelCoordinator = 1
        #Waiting, Working, Finished
        self.statusWorkers = self.manager.dict()
        #Dictionary in which the models are stored     
        self.models = self.manager.dict()

        self.initWorkers()

    def initWorkers(self):
        for index in range(self.Procc):
            self.statusWorkers[index] = "Waiting"
            
            self.workersHome[index] = Process(target=self.training, args=(index, MINIEPISODES, self.modelCoordinator, self.statusWorkers, self.models))
            self.workersHome[index].start()
            
    #Index: The index of the device
    #Episodes: Amount of episodes for the process to train
    #Model: The model to use to train
    #Status: To insert the status of work
    #Models: To store the model
    
    def training(self, Index, Episodes, Model, Status, Models):        
        if Status[Index] == "Waiting":
            Status[Index] = "Working"
            
            agent = DQNAgent(self.state_size, self.action_size, 0.01, Episodes, self.batch_size, "./models/v{VERSION}/logs".format(VERSION=VERSION))
            env = BJEnvironment()

            #agent.model = Model
            
            for ep in range(Episodes):
                print(ep)
                agent.train(env, False)

            Models[Index] = agent.model
            Status[Index] = "Finished"
        
    def factory(self):
        while True:
            
            for index in range(self.Procc):
                if self.statusWorkers[index] == "Finished":
                    print("Process {index} has finished".format(index= index))
                    print(self.models[index].get_weights())
            sleep(1)
            
if __name__ == "__main__": 
    worker = WorkerPC(4)
    worker.factory()