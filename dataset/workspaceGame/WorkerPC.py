import tensorflow as tf
import socket
from multiprocessing import Process, Queue
import time
import numpy as np

from Tools import SaveModel
from Environment import BJEnvironment
from Agent import DQNAgent

VERSION = 2
COMPLETEDVERSION = 1

class WorkerPC:
    def __init__(self):
        self.Procc = 4
        self.state_size = 3
        self.action_size = 3
        self.batch_size = 32
        self.models = {}
    def workers(self):
        q = [(Queue()) for index in range(self.Procc)]
        doneArray = np.zeros(self.Procc)
        
        work = [Process(target=self.test, args=(50,q[index], doneArray, index)) for index in range(self.Procc)]
        
        while True:            
            for worker in work:
                if not worker.is_alive():
                   worker.start()
            time.sleep(1)
            
            for index in range(self.Procc):
                if doneArray[index] == 1:
                    print(q[index].get())
            
        
    def test(self, EPISODES, model, array, index):
        agent = DQNAgent(self.state_size, self.action_size, 0.01, EPISODES, self.batch_size, "./models/v{VERSION}/logs".format(VERSION=VERSION))
        env = BJEnvironment()
        
        for ep in range(EPISODES):
            print(ep)
            agent.train(env, False)

        array[index] = 1
        model.put({agent.model, 1})
       
if __name__ == "__main__": 
    worker = WorkerPC()
    worker.workers()