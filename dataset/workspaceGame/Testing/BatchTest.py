import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Testing import Test

#Based on a model version it loads the starting epochs of each file
#It requires to have a model finished

#Insert version number
VERSION = 2

#It tests the model every x amount
TESTEVERY = 5

#Configurations
TESTGAMES = 1000

def TestModel(testClass):
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
            elif result == "loss":
                losses += 1
                budget -= 5
            elif result == "draw":
                draws += 1
            elif result == "win_double":
                win_double += 1
                budget += 10
            elif result == "badmove":
                nf += 1
    total_profit = budget - 1000
    print(f"Total profit: {total_profit}")
    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")
    print(f"Not Finished: {nf}")

if __name__ == "__main__":
    testClass = Test()
    cantVer = testClass.ModelClass.getFinalLatestVersion(VERSION)
    
    for completedVersion in range(1, cantVer):
        epochs = testClass.ModelClass.getCheckpointLatestVersion(VERSION, completedVersion)
        print(f"VER:{VERSION}, cantVer:{completedVersion}, epoch: {epochs}")
    
        for epoch in range(1, epochs):
            if epoch == 1 or epoch % 5 == 0:
                testClass.ModelClass.loadCheckpoint(VERSION, completedVersion, epoch)
                                
        testClass.ModelClass.loadModel(VERSION, completedVersion)