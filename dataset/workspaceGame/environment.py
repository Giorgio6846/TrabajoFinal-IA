import gymnasium as gym
from gymnasium import spaces
from AItools import *
from game import GameAI
import numpy as np

class BJEnvironment(gym.Env):
    def __init__(self):
        self.Blackjack = GameAI(200000)

        #4 actions in which the AI can do, corresponding to "Split", "Double", "Hit", "Stand"
        self.action_space = spaces.Discrete(4)

        #Observation space for "AI cards", "Dealer cards", "sum dealer cards", "sum ai cards"
        self.observation_space = spaces.Tuple((
            spaces.Box(low=0, high=6, shape=(13,), dtype=np.int32),
            spaces.Box(low=0, high=6, shape=(13,), dtype=np.int32),
            spaces.Discrete(32),
            spaces.Discrete(32),
        ))
    
    def step(self, action):
        if self.Blackjack.getGameState() == 1:
            self.Blackjack.setOutputPlayer(action)
            self.Blackjack.__game()
            
        elif self.Blackjack.getGameState() == 2:
            self.Blackjack.setOutputPlayer(action)
            self.Blackjack.__game()
        
        cardsAI = translateArray(self.Blackjack.getCardsAI())
        cardsDealer = translateArray(self.Blackjack.getCardsDealer())
        sumCardsAI = countCards(cardsAI)
        sumCardsDealer = countCards(cardsDealer)
        
        if self.Blackjack.getGameState() == 6:
            if gameWin() == 0:
               reward = 1
            elif gameWin() == 1:
               reward = 0
            elif gameWin() == 2:
               reward = -1

        # observation, reward, done, info
        return (cardsAI, cardsDealer, sumCardsAI, sumCardsDealer), reward, self.Blackjack.getGameState() == 6, {}
    
    def reset(self):
        self.Blackjack.__reset()
        if self.Blackjack.getGameState() == 0:
            self.Blackjack.setApuesta(50)
            self.Blackjack.setReady(True)
            self.Blackjack.__game()

        cardsAI = translateArray(self.Blackjack.getCardsAI())
        cardsDealer = translateArray(self.Blackjack.getCardsDealer())
        sumCardsAI = countCards(cardsAI)
        sumCardsDealer = countCards(cardsDealer)

        return (cardsAI, cardsDealer, sumCardsAI, sumCardsDealer)

    
            
