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
        self.observation_space = spaces.Dict({
            "sumCardsPlayer": spaces.Discrete(32),
            "sumCardsDealer": spaces.Discrete(32),
            
            "canSplit": spaces.Discrete(2),
            "canDouble": spaces.Discrete(2),
            
            "cardsAI": spaces.Box(low=0, high=6, shape=(13,), dtype=np.int32),
            "cardsDealer": spaces.Box(low=0, high=6, shape=(13,), dtype=np.int32)
        })
    
    def step(self, action):
        if self.Blackjack.getGameState() == 1:
            self.Blackjack.setActionPlayer(action)
            self.Blackjack.game()
            
        elif self.Blackjack.getGameState() == 2:
            self.Blackjack.setActionPlayer(action)
            self.Blackjack.game()
        
        if self.Blackjack.getGameState() == 7:
            if self.Blackjack.gameWin() == 0:
               reward = 1
            elif self.Blackjack.gameWin() == 1:
               reward = 0
            elif self.Blackjack.gameWin() == 2:
               reward = -1
            return self.get_obs(), reward, self.Blackjack.hasGameFinished(), {}

        # observation, reward, done, info
        return self.get_obs(), 0, self.Blackjack.hasGameFinished(), {}
    
    def get_obs(self):
        return {
            "sumCardsPlayer": countCards(translateArray(self.Blackjack.getCardsAI())),
            "sumCardsDealer": countCards(translateArray(self.Blackjack.getCardsDealer())),
            
            "canSplit": self.Blackjack.getGameState() == 1,
            "canDouble": self.Blackjack.getGameState() == 1,
            
            "cardsAI": translateArray(self.Blackjack.getCardsAI()),
            "cardsDealer": translateArray(self.Blackjack.getCardsAI())
        }
    
    def reset(self):
        self.Blackjack.reset()
        if self.Blackjack.getGameState() == 0:
            self.Blackjack.setApuesta(50)            
            self.Blackjack.game()
        
        return self.get_obs()
        
    def preprocess_observation(self, observation):        
        flat_observation = []
        
        sumCardsPlayer = np.array([observation["sumCardsPlayer"]]).resize(13)
        sumCardsDealer = np.array([observation["sumCardsDealer"]]).resize(13)
        can_Split = np.array([observation["canSplit"]]).resize(13)
        can_Double = np.array([observation["canDouble"]]).resize(13)
        
        flat_observation = np.concatenate([
                               sumCardsPlayer, sumCardsDealer,
                               can_Split, can_Double,
                               observation["cardsAI"], 
                               observation["cardsDealer"]
                              ])
        
        return flat_observation