import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.Model.Agent import DQNAgent
from lib.Game.Environment import BJEnvironment
from lib.Model.Tools import LAYERS

#Based on a csv file it trains the model with the hyperparameters set on the csv file

SAVEEVERY = 250

SAVETOTENSORBOARD = False
EPISODES = 10000

if __name__ == "__main__":

    if("TERM_PROGRAM" in os.environ.keys() and os.environ["TERM_PROGRAM"] == "vscode"):
        BatchesQueue = pd.read_csv("dataset/workspaceGame/Training/testModels.csv")
    else:
        BatchesQueue = pd.read_csv("./testModels.csv")
        
    BatchesDict = BatchesQueue.to_dict(orient='records')

    for batch in BatchesDict:
        epoch = 1
        env = BJEnvironment()
        agent = DQNAgent(env.state_size, env.action_size, batch)
        agent.setHyperparameters(batch)
        batch["layers"] = LAYERS
        agent.ModelClass.saveConfigModel(batch, batch["VERSION"])
        

        batch["COMVER"] = agent.ModelClass.getFinalLatestVersion(batch["VERSION"])
        print(batch["COMVER"])

        if batch["COMVER"] != 1:
            agent.ModelClass.loadModel(batch["VERSION"], batch["COMVER"] - 1)

        agent.ModelClass.saveStatus(1, batch["VERSION"])
        for ep in range(1, EPISODES + 1):
            if ep % 10 == 0:
                print(ep)
                agent.train(env, SAVETOTENSORBOARD)
            else:
                print(ep)
                agent.train(env, False)

            if ep % SAVEEVERY == 0 and ep != 0:
                agent.ModelClass.saveCheckpoint(
                    batch["VERSION"], batch["COMVER"], epoch
                )
                epoch = epoch + 1

        agent.ModelClass.saveModel(batch["VERSION"], batch["COMVER"])

        env = 1
        agent = 1
