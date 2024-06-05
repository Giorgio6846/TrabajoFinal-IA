import gymnasium as gym
import numpy as np

from blackjack import BlackjackGame

class BJEnvironment(gym.Env):
    @staticmethod
    def has_usable_ace(hand):
        """Check if the hand has a usable ace."""
        value, ace = 0, False
        for card in hand:
            card_number = card["number"]
            value += min(
                10, int(card_number) if card_number not in ["J", "Q", "K", "A"] else 11
            )
            ace |= card_number == "A"
        return int(ace and value + 10 <= 21)

    def __init__(self):
        self.game = BlackjackGame()
        self.bet = 5

        self.state_size = 3
        self.action_size = 3

    def step(self,action):
        state = self.get_obs()

        if self.status[1] == "continue":
            act_string = ["hit", "stay", "double"][action]

            bet = self.game.return_bounty(self.bet, act_string)
            status = self.game.player_action(act_string)
            reward = 0

            if status[1] == "player_blackjack":
                reward += bet
            elif status[1] == "player_bust":
                reward -= bet

            done = status[1] in ["player_blackjack", "player_bust"]

            if status[0] == "stay":
                1==1

            final_result = self.game.game_result()
            final_reward = (
                bet
                if final_result == "win"
                else (-bet if final_result == "loss" else 0)
            )

        return state, action, reward, self.get_obs(), done

    def get_obs(self):
        dealer_card = (
                int(self.game.dealer_hand[0]["number"])
                if self.game.dealer_hand[0]["number"] not in ["J", "Q", "K", "A"]
                else (10 if self.game.dealer_hand[0]["number"] != "A" else 11)
            )

        player_sum = self.game.hand_value(self.game.player_hand)
        usable_ace = self.has_usable_ace(self.game.player_hand)
        state = np.array([player_sum, dealer_card, usable_ace])
        state = np.reshape(state, [1, self.state_size])
        return state

    def reset(self):
        self.game = BlackjackGame()
        self.game.start_game(self.bet)

        self.status = ["act", "continue"]
