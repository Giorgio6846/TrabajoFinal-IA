import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.Model.A3CAgent import Agent
from lib.Game.Environment import BJEnvironment
from lib.Model.Tools import LAYERS

VERSION = 1
COMPLETEDVERSION = 1
EPOCH = 1

SAVEEVERY = 250

SAVETOTENSORBOARD = False

if __name__ == "__main__":
    EPISODES = 16000
    
    agent = Agent()
    agent.train(2000)
