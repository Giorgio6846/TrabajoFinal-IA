import numpy as np
import random
from collections import deque
import tensorflow as tf

from Blackjack import BlackjackGame
from dataset.workspaceGame.Blackjack.Tools import SaveModel, Model

VERSION = 1
COMPLETEDVERSION = 1
VERBOSETRAIN = 1


class Test:
    def __init__(self, model):
        self.ModelClass = Model()

        self.model = model
        self.state_size = 3
        self.epsilon = 0

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

    def act(self, state):
        act_values = model.predict(state, verbose=VERBOSETRAIN)
        return np.argmax(act_values[0])

    def play(self, bet):
        game = BlackjackGame()
        game.start_game(bet)

        print("Dealer shows:", game.format_cards(game.dealer_hand[:1]))
        status = ["act", "continue"]
        print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        while status[1] == "continue":
            player_sum = game.hand_value(game.player_hand)
            usable_ace = self.has_usable_ace(game.player_hand)
            dealer_card = (
                int(game.dealer_hand[0]["number"])
                if game.dealer_hand[0]["number"] not in ["J", "Q", "K", "A"]
                else (10 if game.dealer_hand[0]["number"] != "A" else 11)
            )
            state = np.array([player_sum, dealer_card, usable_ace])
            state = np.reshape(state, [1, self.state_size])
            action = self.act(state)
            action_str = ["hit", "stay", "double"][action]
            status = game.player_action(action_str)

            if action_str == "stay":
                break

            print(
                game.format_cards(game.player_hand), game.hand_value(game.player_hand)
            )

        if status[1] == "continue":
            print(
                "Dealer has:",
                game.format_cards(game.dealer_hand),
                game.hand_value(game.dealer_hand),
            )
            game.dealer_action()

        final_result = game.game_result()
        return final_result


if __name__ == "__main__":
    save = SaveModel()
    model = save.loadModel(VERSION, COMPLETEDVERSION)

    TestClass = Test(model)

    # Evaluate the agent
    test_games = 10000
    wins, losses, draws = 0, 0, 0

    for index in range(1, test_games):
        print("-----")
        print(index)
        bet = 5
        result = TestClass.play(bet)
        print(result)
        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1
        elif result == "draw":
            draws += 1

    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")
