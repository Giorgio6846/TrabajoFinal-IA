import gymnasium as gym
from gymnasium import spaces
import numpy as np

from .Blackjack import BlackjackGame

class BJEnvironment(gym.Env):
    def __init__(self):
        self.game = BlackjackGame()
        self.deck_min_len = 109

        # player_sum, dealer_sum, usable_ace, has_double, prob_21, game_state
        # game_state = 0 normal, 1 split, 2 double
        self.state_size = 6
        # Hit, Stand, Split, Double
        self.action_size = 2
        self.observation_space = spaces.Box(low=np.array([4,4,0,0,0,0]), high=np.array([30,30,1,1,9,2]), shape=(self.state_size,), dtype=np.uint8)
        self.action_space = spaces.Discrete(self.action_size)

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

    def get_badmove(self):
        return self.game.badMove

    def set_deck_per_game(self, deck):
        self.used_carts = np.copy(deck)

    def get_final_result(self):
        final_result = self.game.game_result()
        return final_result

    def step(self, action):
        act_string = ["hit", "stay", "split", "double"][action]
        state = self.get_obs()
        bet = self.game.bet_game
        status = self.game.player_action(act_string)

        reward = 0
        done = 0

        bet = self.game.return_bounty(self.bet, act_string)

        if done or self.game.badMove:
            self.set_deck_per_game()

        if status[1] == "continue":

            if self.game.badMove:
                reward = -5
                done = True

            return state, action, reward, self.get_obs(), done

        # Si cuando el jugador o el dealer tienen 21 en la primera no obtiene recompensa
        if self.game.firstTurn:
            reward = 0
        else:
            if status[1] == "win":
                reward = bet / self.game.bet_game

            if status[1] == "loss":
                reward = -bet/self.game.bet_game

        if status[1] == "draw":
            reward = 0

        print(self.game.game_result())

        # print("END")

        # print("Player Cards:")
        # rint(self.game.format_cards(self.game.player_hand), "   ", self.game.hand_value(self.game.player_hand))

        # print("Dealer Cards:")
        # print(self.game.format_cards(self.game.dealer_hand), "   ", self.game.hand_value(self.game.dealer_hand))
        return state, action, reward, self.get_obs(), True

    def get_obs(self):
        # player_sum, dealer_sum, usable_ace, split_pos, double_pos, prob_21, game_state
        player_sum = self.game.hand_value(self.game.player_hand)
        dealer_card = self.game.hand_value(self.game.dealer_hand)
        if self.game.firstTurn:
            dealer_card = self.game.hand_value(self.game.dealer_hand[:1])
        usable_ace = self.has_usable_ace(self.game.player_hand)
        #has_split = (
        #    len(self.game.player_hand) == 2
        #    and self.game.player_hand[0]["number"] == self.game.player_hand[1]["number"]
        #)
        has_double = self.game.firstTurn
        prob_21 = self.game.get_prob_of_bust(self.used_carts)
        game_state = self.game.status

        if game_state == 1 and player_sum > 21:
            player_sum = self.game.hand_value(self.game.splitted_hands[1])

        state = np.array(
            [
                player_sum,
                dealer_card,
                usable_ace,
                #has_split,
                has_double,
                prob_21,
                game_state,
            ]
        )
        state = state.astype(np.uint8)
        state = np.reshape(state, [1, self.state_size])
        return state

    def reset(self, bet):

        self.bet = bet
        
        if(len(self.game.get_deck()) == 312):
            self.set_deck_per_game(self.game.get_deck())

        if (len(self.game.get_deck()) <= self.deck_min_len):
            self.game.regenerate_deck()

        self.game.start_game(self.bet)

        self.status = ["act", "continue"]

        return self.get_obs(), {}
