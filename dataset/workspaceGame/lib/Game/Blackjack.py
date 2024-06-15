import random

class BlackjackGame:

    heart = "\u2665"
    spade = "\u2660"
    diamond = "\u2666"
    club = "\u2663"

    suits = {
        "diamonds": diamond,
        "hearts": heart,
        "spades": spade,
        "clubs": club
    }

    # inicializacion de las variables de juego
    def __init__(self):
        self.deck = self.generate_deck()
        random.shuffle(self.deck)
        self.bet_game = 0
        self.hands_splited = []
        self.current_hand_index = 0 
        self.player_hand = []
        self.dealer_hand = []
        self.status = 0

    def get_deck(self):
        return self.deck

    def set_deck(self, new_deck):
        self.deck = new_deck

    def regenerate_deck(self):
        self.deck = self.generate_deck()
        random.shuffle(self.deck)

    @staticmethod
    def generate_deck():
        numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        deck = [{'number': number, 'suit': suit} for number in numbers for suit in suits]
        deck = deck * 6
        return deck

    def deal_card(self):
        return self.deck.pop()

    # fucion para empezar el juego, donde se crean las manos de los jugadores
    def start_game(self, bet):
        self.firstTurn = True
        self.splitted_done = False
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.bet_game = bet #se incializa la variable apuesta que es introducida como un parametro
        self.splitted_hands = []  
        self.current_hand_index = 0
        self.status = 0
        self.badMove = False
        self.game_status = "continue"

        # This is only true when it has been selected split and the first maze has blown
        self.handLose = False

    # Funcion para obtener el valor de la mano del jugador.
    @staticmethod
    def hand_value(hand):
        value = 0
        aces = 0
        for card in hand:
            if card['number'] in ['J', 'Q', 'K']:
                value += 10
            elif card['number'] == 'A':
                value += 11
                aces += 1
            else:
                value += int(card['number'])

        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    # todas las acciones que puede realizar el jugador
    def player_action(self, action):
        if not (self.__checkBlackjack() or self.__checkBlowCards()):
            self.badMove = False
            self.firstTurn = False
            # "Hit" automaticamente se introduce una carta de la baraja a la mano del jugador y se borra una carta del array del mazo.
            if action == "hit":
                self.player_hand.append(self.deal_card())
            # "Double" cuando se dobla el tamaño de la apuesta, pero solo se obtiene una carta mas y la accion pasa a automaticamente a "stay"
            elif action == "double":
                self.bet_game *= 2
                self.player_hand.append(self.deal_card())
                self.status = 2
                action = "stay"
            # "Split" divide la mano del jugador en 2, doblando la apuesta (solo aplica cuando la mano del jugador cuenta con 2 cartas del mismo numero)
            elif action == "split":
                if len(self.player_hand) == 2 and self.player_hand[0]['number'] == self.player_hand[1]['number']:
                    self.splitted_hands = [[self.player_hand[0]], [self.player_hand[1]]]
                    if self.splitted_done:
                        self.player_hand = self.splitted_hands[1]
                    else:
                        self.player_hand = self.splitted_hands[0]
                        self.splitted_done = True

                    self.splitted_hands[0].append(self.deal_card())
                    self.splitted_hands[1].append(self.deal_card())
                    self.bet_game *= 2
                    self.status = 1

                else:
                    print("El split solo es permitido con 2 cartas del mismo valor en la mano")
                    self.badMove = True

            if action == "stay" and self.game_status == "continue":
                self.dealer_action()
                if self.__checkWinner():
                    return action, self.game_status

            if not self.__checkBlackjack() or self.__checkBlowCards():
                self.game_status = "continue"

        return action, self.game_status

    # funcion para retornar el valor de la apuesta, en caso de que se doble o se haga split.
    def return_bounty(self, bet, action):
        if(action == "double" or action == "split"):
            return bet*2
        return bet

    # se hace la funcion para que el dealer tome cartas en caso de que la suma de su mano sea menor a 17
    def dealer_action(self):
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())
            print("Dealer hits and has:", self.format_cards(self.dealer_hand), self.hand_value(self.dealer_hand))

    # If true it means the game has ended
    def __checkWinner(self):
        if self.__checkBlowCards():
            return True
        elif self.__checkBlackjack():
            return True
        elif self.__checkBiggerCard():
            return True

        return False

    # If true it means the game has ended
    def __checkBiggerCard(self):
        if not self.handLose:
            player_hand = self.player_hand
        else:
            player_hand = self.game.splitted_hands[1]

        if self.hand_value(player_hand) == self.hand_value(self.dealer_hand):
            self.game_status = "draw"
            return True
        elif self.hand_value(player_hand) > self.hand_value(self.dealer_hand):
            self.game_status = "win"
            return True
        elif self.hand_value(player_hand) < self.hand_value(self.dealer_hand):
            self.game_status = "loss"
            return True
        return False

    # If true it means the game has ended
    def __checkBlackjack(self):
        if not self.handLose:  
            player_hand = self.player_hand
        else:
            player_hand = self.game.splitted_hands[1]

        if (
            self.hand_value(player_hand) == 21
            and self.hand_value(self.dealer_hand) == 21
        ):
            self.game_status = "draw"
            return True
        elif self.hand_value(player_hand) == 21:
            self.game_status = "win"
            return True
        elif self.hand_value(self.dealer_hand) == 21:
            self.game_status = "loss"
            return True

        return False

    def __checkBlowCards(self):
        if not self.handLose:  
            player_hand = self.player_hand
        else:
            player_hand = self.game.splitted_hands[1]

        if (
            self.hand_value(player_hand) > 21
            and self.hand_value(self.dealer_hand) > 21
        ):
            self.game_status = "draw"
            return True
        elif self.hand_value(player_hand) > 21:
            self.game_status = "loss"
            return True
        elif self.hand_value(self.dealer_hand) > 21:
            self.game_status = "win"
            return True

        return False

    # Se obtienen los valores de las manos del dealer y del jugador y se comparan
    def game_result(self):
        return self.game_status

    # formato para imprimir cartas
    @staticmethod
    def format_cards(cards):
        result = ""
        for card in cards:
            suit = BlackjackGame.suits[card["suit"]]
            result += f"{card['number']}{suit} "

        return result.strip()

    def get_prob_of21(self):
        amountNeeded = 21 - self.hand_value(self.player_hand)
        prob = abs(100 * amountNeeded / 21)

        prob = prob / 10
        prob = round(prob, 3)

        if prob > 10:
            prob = 10

        return prob

def main():
    game = BlackjackGame()
    print("select your bet:")
    bet = int(input(("1 / 5 / 10: ")))
    game.start_game(bet)    
    print("Dealer shows:", game.format_cards(game.dealer_hand[:1]))

    status = "continue"
    while status == "continue":
        print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        action = input("Enter an action (hit/stay/split/double): ")
        action, status = game.player_action(action)

        if action == "stay":
            break

    if status == "continue":
        print("Dealer has:", game.format_cards(game.dealer_hand), game.hand_value(game.dealer_hand))
        game.dealer_action()

    game.__checkWinner()

    print(game.game_status)

if __name__ == "__main__":
    main()
