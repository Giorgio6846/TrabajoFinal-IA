import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Testing import Test

# Based on a model version it loads the starting epochs of each file
# It requires to have a model finished

# Insert version number
VERSION = 3

# It tests the model every x amount
TESTEVERY = 5

# Configurations
TESTGAMES = 1000

reportPath = "./../GameModels/v{ver}/Report/rp-{report}-epc-{epoch}.csv"
reportDir = "./../GameModels/v{ver}/Report/"

if "TERM_PROGRAM" in os.environ.keys() and os.environ["TERM_PROGRAM"] == "vscode":
    reportPath = (
        "./dataset/workspaceGame/GameModels/v{ver}/Report/rp-{report}-epc-{epoch}.csv"
    )
    reportDir = "./dataset/workspaceGame/GameModels/v{ver}/Report/"

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
        
        df = pd.concat(df, pd.DataFrame.from_records([dictValue]))
        df.reset_index(inplace=True)
        
    total_profit = budget - 1000
    print(f"Total profit: {total_profit}")
    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")
    print(f"Not Finished: {nf}")
    return df

def printStatus(dataframe, report, epoch):
    fig = plt.figure()
    fig = dataframe.plot(y="value").get_figure()
    fig.savefig(reportDir.format(ver=VERSION) + f"GS-{report}-EPC-{epoch}.png")


def printCumStatus(dataframe, report, epoch):
    fig = plt.figure()
    fig = dataframe.cumsum().plot(y="value").get_figure()
    fig.savefig(reportDir.format(ver=VERSION) + f"CS-{report}-EPC-{epoch}.png")

def saveDataframe(dataframe, report, epoch):
    dataframe.save_csv(reportPath.format(ver=VERSION, report = report, epoch = epoch))

if __name__ == "__main__":
    testClass = Test()
    cantVer = testClass.ModelClass.getFinalLatestVersion(VERSION)
    Report = 1

    for completedVersion in range(1, cantVer):

        epochs = testClass.ModelClass.getCheckpointLatestVersion(VERSION, completedVersion)
        print(f"VER:{VERSION}, cantVer:{completedVersion}, epoch: {epochs}")

        Epoch = 1
        for epoch in range(1, epochs):
            if epoch == 1 or epoch % 5 == 0:
                testClass.ModelClass.loadCheckpoint(VERSION, completedVersion, epoch)

                dfGameStatus = TestModel(testClass)
                printStatus(dfGameStatus, Report, Epoch)
                printCumStatus(dfGameStatus, Report, Epoch)
                saveDataframe(dfGameStatus, Report, Epoch)
                
                Epoch = Epoch + 1

        testClass.ModelClass.loadModel(VERSION, completedVersion)
        dfGameStatus = TestModel(testClass)
        printStatus(dfGameStatus, Report, Epoch)
        printCumStatus(dfGameStatus, Report, Epoch)
        saveDataframe(dfGameStatus, Report, Epoch)

