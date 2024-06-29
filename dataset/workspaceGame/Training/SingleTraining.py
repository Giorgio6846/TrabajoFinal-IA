import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.Model.Agent import DQNAgent
from lib.Game.Environment import BJEnvironment
from lib.Model.Tools import LAYERS

VERSION = 2
COMPLETEDVERSION = 1
EPOCH = 12

SAVEEVERY = 250

SAVETOTENSORBOARD = False

if __name__ == "__main__":
    EPISODES = 16000
    
    env = BJEnvironment()
    agent = DQNAgent(env.state_size, env.action_size, VERSION)
    configDict = agent.getHyperparameters()
    configDict["layers"] = LAYERS
    agent.ModelClass.saveConfigModel(configDict, VERSION)

    COMPLETEDVERSION = agent.ModelClass.getFinalLatestVersion(VERSION)
    print(COMPLETEDVERSION)
    
    if COMPLETEDVERSION != 1:
        agent.ModelClass.loadModel(VERSION, COMPLETEDVERSION-1)
        
    agent.ModelClass.saveStatus(1, VERSION)
    for ep in range(EPISODES):
        if ep % 10 == 0:        
            print(ep)
            agent.train(env, SAVETOTENSORBOARD)
        else:
            print(ep)
            agent.train(env, False)

        if ep % SAVEEVERY == 0 and ep != 0:
            agent.ModelClass.saveCheckpoint(VERSION, COMPLETEDVERSION, EPOCH)
            EPOCH = EPOCH + 1

    agent.ModelClass.saveModel(VERSION, COMPLETEDVERSION)
