from Blackjack.Agent import DQNAgent
from Blackjack.Environment import BJEnvironment
from Blackjack.Tools import Model

VERSION = 8
COMPLETEDVERSION = 1
SAVEEVERY = 250

SAVETOTENSORBOARD = False

if __name__ == "__main__":
    EPISODES = 2000

    batch_size = 128

    env = BJEnvironment()
    agent = DQNAgent(env.state_size, env.action_size, 0.01, batch_size, VERSION)

    COMPLETEDVERSION = agent.ModelClass.getCheckpointLatestVersion(VERSION)
    
    if COMPLETEDVERSION > 1:
        agent.ModelClass.loadCheckpoint(VERSION, COMPLETEDVERSION-1)
        
    for ep in range(EPISODES):
        if ep % 10 == 0:        
            print(ep)
            agent.train(env, SAVETOTENSORBOARD)
        else:
            print(ep)
            agent.train(env, False)

        if ep % SAVEEVERY == 0 and ep != 0:
            agent.ModelClass.saveCheckpoint(agent.model, VERSION, COMPLETEDVERSION)
            COMPLETEDVERSION = COMPLETEDVERSION + 1

    agent.ModelClass.saveModel(agent.model, VERSION, COMPLETEDVERSION)