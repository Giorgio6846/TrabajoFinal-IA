import pandas as pd 
import os
import numpy as np 
import sys
from sklearn.model_selection import ParameterSampler
from multiprocessing import Manager, Process
from scipy.stats import uniform
from sympy import evaluate

from dataset.workspaceGame.Testing.BatchTest import TestModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Testing.SingleTesting import Test, TestClass
from lib.Model.Agent import DQNAgent
from lib.Game.Environment import BJEnvironment

SAVEEVERY = 250
TESTGAMES = 1000

df = pd.DataFrame()

if("TERM_PROGRAM" in os.environ.keys() and os.environ["TERM_PROGRAM"] == "vscode"):
    BatchesQueue = pd.read_csv("dataset/workspaceGame/Training/testModels.csv")
else:
    BatchesQueue = pd.read_csv("./testModels.csv")

hyperparameter_space = {
    "batchSize":     np.arange(8   ,33   ,8),
    "gamma":         np.arange(80 ,100 ,1)/100,
    "epsilon":       np.arange(80 ,100 ,1)/100,
    "epsilonMin":    np.arange(10 ,21  ,1)/100,
    "annelingSteps": np.arange(6000,16001,500),
    "learningRate":  uniform(1e-5, 1e-2),
}

def summaryDataframes(arrayDataframe):
    df = pd.DataFrame()
    chkpnt = 1

    for dataframe in arrayDataframe:
        dictValue = {
            "ckpnt": chkpnt,
            "loss": (dataframe["status"] == "loss").sum(),
            "win": (dataframe["status"] == "win").sum(),
            "draw": (dataframe["status"] == "draw").sum(),
        }
        chkpnt = chkpnt + 1
        df = pd.concat([df, pd.DataFrame.from_records([dictValue])], ignore_index=True)
    return df

def TestModel(testClass):
    df = pd.DataFrame()
    wins, losses, draws, nf, win_double = 0, 0, 0, 0, 0
    budget = 1000
    
    for index in range(1, TESTGAMES):
        print("-----")
        print(index)
        bet = 5
        result = testClass.play(bet)
        print(result)
        if result == "win":
            wins += 1
            budget += 5
            dictValue = {"value": 5, "status": "win"}
        elif result == "loss":
            losses += 1
            budget -= 5
            dictValue = {"value": -5, "status": "loss"}
        elif result == "draw":
            draws += 1
            dictValue = {"value": 0, "status": "draw"}
        elif result == "win_double":
            win_double += 1
            budget += 10
            dictValue = {"value": 10, "status": "win_double"}
        elif result == "badmove":
            nf += 1
            dictValue = {"value": -10, "status": "badMove"}
        
        df = pd.concat([df, pd.DataFrame.from_records([dictValue])], ignore_index=True)
    df.reset_index(inplace=True)
        
    total_profit = budget - 1000
    print(f"Total profit: {total_profit}")
    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")
    print(f"Not Finished: {nf}")
    return df

# If it returns 1 it means that this hyperparameter has already been
# explored whoever with diferent annelingSteps
def isIndf(df, parameters):
    if len(df) == 0:
        return 0
    
    pos = df.loc[
        (df["annelingSteps"] == parameters["annelingSteps"])
        & (df["batchSize"] == parameters["batchSize"])
        & (df["epsilon"] == parameters["epsilon"])
        & (df["epsilonMin"] == parameters["epsilonMin"])
        & (df["gamma"] == parameters["gamma"])
        & (df["learningRate"] == parameters["learningRate"])
    ]

    return len(pos)>= 1

# If it has already been found a similar hyperparameter it searches if it has similar information
def getAnnelingStepsFromDF(df, parameters):
    pos = df.loc[
        (df["annelingSteps"] == parameters["annelingSteps"])
        & (df["batchSize"] == parameters["batchSize"])
        & (df["epsilon"] == parameters["epsilon"])
        & (df["epsilonMin"] == parameters["epsilonMin"])
        & (df["gamma"] == parameters["gamma"])
        & (df["learningRate"] == parameters["learningRate"])
    ]

    return (
        pos["annelingSteps"].max(),
        df.loc[(df["annelingSteps"] == df["annelingSteps"].max())]["VERSION"],
        df.loc[(df["annelingSteps"] == df["annelingSteps"].max())]["COMVER"],
    )

def dfLatestVersion(df):
    version = df.drop_duplicates("VERSION")
    return len(version) + 1

def train_evaluate_report(parameter, df):
    env = BJEnvironment()
    agent = DQNAgent(env.state_size, env.action_size, parameter["batchSize"])

    agent.setHyperparameters(parameter)

    parameter["VERSION"] = len(df.shape[0]+1)
    parameter["COMVER"] = 1

    if isIndf(df, parameter):
        annelingSteps, version, comver = getAnnelingStepsFromDF(df, parameter)

        if annelingSteps <= parameter["annelingSteps"]:
            # If it has found that annelingSteps has a lower
            # Loads the checkpoint of the model and then it saves it as a finished version
            # Then procceds to run the evaluation steps

            checkpointVer = annelingSteps / 250
            agent.ModelClass.loadCheckpoint(version, comver, checkpointVer)

            latestVer = agent.ModelClass.getFinalLatestVersion(version)
            agent.ModelClass.saveModel(version, latestVer+1)

            mean = evaluateModel(version, latestVer+1)

        else:
            # If has found that annelingSteps has an old version however
            # The parameters are higher so it run from the latest version and completes it to the latest point
            checkpoint = agent.ModelClass.getCheckpointLatestVersion(version, comver)
            latestVer = agent.ModelClass.getFinalLatestVersion(version)
            checkpoint = (checkpoint + 1) * 250

            agent.ModelClass.loadModel(version, comver)
            episodesRemaining = parameter["annelingSteps"] - checkpoint

            train(episodesRemaining, agent, env, version, latestVer)

            mean = evaluateCheckpoints(version, latestVer)
    else: 
        version = dfLatestVersion(df)
        train(parameter["annelingSteps"], agent,env, version, 1)

        mean = evaluateCheckpoints(version, latestVer)

    parameter["mean"] = mean
    
    return parameter

def getMeanPercentage(df):
    df["percentage"] = round((df["win"]*100/(df["win"]+df["loss"])),2)
    return df["percentage"].mean()

# Loads the finished model to get the mean wins and fails
def evaluateCheckpoints(version, comver):
    dfArray = []
    testClass = Test()

    epochs = testClass.ModelClass.getCheckpointLatestVersion(version, comver)

    for epoch in range(1, epochs):
        testClass.ModelClass.loadCheckpoint(version, comver, epoch)
        dfArray.append(TestModel(testClass))

    testClass.ModelClass.loadModel(version, comver)
    dfArray.append(TestModel(testClass))

    df = summaryDataframes(dfArray)
    
    mean = getMeanPercentage(df)
    return mean

# Loads the finished model to get the mean wins and fails
def evaluateModel(version, comver):
    dfArray = []
    
    testClass = Test()
    testClass.ModelClass.loadModel(version, comver)

    dfArray.append(TestModel(testClass))
    df = summaryDataframes(dfArray)

    mean = getMeanPercentage(df)
    return mean

def train(episodes, agent, env, version, comver):
    epoch = 1
    
    for ep in range(episodes + 1):
         agent.train(env, False)
         
         if ep % 250 == 0 and ep != 0:
             agent.ModelClass.saveCheckpoint(version, comver, epoch)
             epoch + 1
    
    agent.ModelClass.saveModel(version, comver)

if __name__ == "__main__":
    parameter_list = list(ParameterSampler(hyperparameter_space, n_iter = 50))

    for parameter in parameter_list:
        inf = train_evaluate_report(parameter, df)
        df = pd.concat([df, pd.DataFrame.from_records([inf])], ignore_index=True)