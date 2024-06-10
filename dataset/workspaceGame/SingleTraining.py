from Blackjack.Agent import DQNAgent
from Blackjack.Environment import BJEnvironment
from Blackjack.Tools import SaveModel

VERSION = 2
COMPLETEDVERSION = 1
SAVEEVERY = 100

if __name__ == "__main__":
    EPISODES = 2600

    batch_size = 32

    env = BJEnvironment()
    agent = DQNAgent(env.state_size, env.action_size, 0.01, batch_size, VERSION)
    save = SaveModel()

    COMPLETEDVERSION = save.latestModel(VERSION)
    
    if COMPLETEDVERSION > 1:
        agent.model = save.loadModel(VERSION, COMPLETEDVERSION-1)
        
    for ep in range(EPISODES):
        if ep % 10 == 0:        
            print(ep)
            agent.train(env, True)
        else:
            print(ep)
            agent.train(env, False)

        if ep % SAVEEVERY == 0 and ep != 0:
            save.saveModel(agent.model, VERSION, COMPLETEDVERSION)
            COMPLETEDVERSION = COMPLETEDVERSION + 1

    save.saveModel(agent.model, VERSION, COMPLETEDVERSION)
