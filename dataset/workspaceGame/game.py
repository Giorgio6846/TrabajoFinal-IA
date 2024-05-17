from mazo import Mazo
from mano import Mano

class GamePlayer: 
    def __init__(self):
        pass 

    def play(self):
        playing = True 
        self.presupuesto = 100
        while playing and self.presupuesto>0: 
            self.mazo = Mazo()
            self.mazo.shuffle()
            
            print("Presupuesto actual: ", self.presupuesto)
            while True:
                self.apuesta = int(input("Escoge la cantidad de tu apuesta: "))
                
                if self.apuesta <= self.presupuesto:
                    break


            self.jugador_Mano = Mano()
            self.dealer_Mano = Mano(dealer=True)

            for i in range(2):
                self.jugador_Mano.add_Carta(self.mazo.deal())
                self.dealer_Mano.add_Carta(self.mazo.deal())
            print("")
            print("Tu mazo es:")
            self.jugador_Mano.display()
            print()
            print("El mazo del dealer es: ")
            self.dealer_Mano.display()

            game_over = False

            while not game_over: 
                jugador_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()

                if jugador_has_blackjack or dealer_has_blackjack:
                    game_over = True 
                    self.show_blackjack_results(
                        jugador_has_blackjack , dealer_has_blackjack)
                    continue 
                
                choice = input("Por favor elija [Seguir / Quedarse] ").lower()
                while choice not in ["s" , "q" , "Seguir" , "Quedarse"]:
                    choice = input("Por favor elija [Seguir / Quedarse] or (S/Q)").lower()
                if choice in ['Seguir', 's']:
                    self.jugador_Mano.add_Carta(self.mazo.deal())
                    self.jugador_Mano.display()
                    if self.jugador_is_over():
                        self.presupuesto = self.presupuesto-self.apuesta
                        print("El mazo del dealer es: ")
                        self.dealer_Mano.display_all()
                        print("Usted perdió!")
                        game_over =True
                
                else:
                    jugador_Mano_valor = self.jugador_Mano.get_valor()
                    dealer_Mano_valor = self.dealer_Mano.get_valor()

                    print("Resultado Final")
                    print(self.jugador_Mano.display_all())
                    print("Tu mano es:", jugador_Mano_valor)
                    print(self.dealer_Mano.display_all())
                    print("La mano del dealer es:", dealer_Mano_valor)

                    if jugador_Mano_valor > dealer_Mano_valor:
                        self.presupuesto = self.presupuesto+self.apuesta
                        print("Usted ha ganado!")
                    elif jugador_Mano_valor == dealer_Mano_valor:
                        print("Empate!")
                    else: 
                        self.presupuesto = self.presupuesto-self.apuesta
                        print("El dealer ha ganado!")
                    game_over = True

            again = input("Jugar de nuevo?")
            while again.lower() not in ["y" , "n"]:
                 again = input("Por favor presione Y o N ") 
            if again.lower() == "n":
                print("Thanks for playing!")
                playing = False
            else:
                game_over = False

    def jugador_is_over(self):
        return self.jugador_Mano.get_valor() > 21
    
    def check_for_blackjack(self):
        jugador = False 
        dealer = False
        if self.jugador_Mano.get_valor() == 21: 
            jugador = True
        if self.dealer_Mano.get_valor() == 21:
            dealer = True 

        return jugador, dealer 
    
    def show_blackjack_results(self, jugador_has_blackjack, dealer_has_blackjack):
        if jugador_has_blackjack and dealer_has_blackjack:
            print("Mano del dealer:")
            self.dealer_Mano.display_all()
            print("Mano del jugador:")
            self.jugador_Mano.display_all()

            print("Los dos jugadores tienen blackjack! Draw!")

        elif jugador_has_blackjack:
            print("Mano del jugador:")
            self.jugador_Mano.display_all() 
            self.presupuesto = self.presupuesto + self.apuesta
            print("Usted tiene blackjack! Usted gana!")
        
        elif dealer_has_blackjack:
            print("Mano del dealer:")
            self.dealer_Mano.display_all()
            self.presupuesto = self.presupuesto - self.apuesta
            print("El dealer tiene blackjack! El dealer gana!")

class GameAI:
    def __init__(self, presupuesto):
        # Paso realizado
        # Para permitir la comunicacion entre la IA y el juego
        self.ready = False

        # Estado de juego
        # 0 = Esperando cantidad de apuesta
        # 1 = Entrega de cartas
        # 2 = Juego en proceso

        # 3 = Juego en proceso - se ha solicitado doblar
        # 4 = Juego en proceso - se ha solicitado seguro -- no siempre existe
        # 5 = Juego en proceso - se ha solicitado split

        # 6 = Juego finalizado

        self.gameState = 0

        self.isPrimerTurno = False

        # Outputs jugador
        # 0 = Quedarse
        # 1 = Seguir
        # 2 = Seguro
        # 3 = Doblar
        self.outputPlayer = 0

        # Jugador gano
        self.playerWin = False

        # Configuracion para IA
        self.presupuesto = presupuesto
        self.apuesta = 0

        # Inicio clases
        self.mazo = Mazo()
        self.manoJugador = Mano()
        self.manoDealer = Mano(dealer=True)

    def game(self):
        if self.ready == False:
            return

        if self.gameState == 0:
            self.gameState = self.gameState + 1

        elif self.gameState == 1:
            self.isPrimerTurno = True
            self.__dealInitialCards()

        elif self.gameState == 2:
            if self.outputPlayer == 0:
                self.__dealCardDealer()
            elif self.outputPlayer == 1:
                self.__dealCard(self.manoJugador)

                if self.__checkWinner():
                    self.gameState = self.gameState + 1

                self.__dealCardDealer()

                if self.__checkWinner():
                    self.gameState = self.gameState + 1

            elif self.outputPlayer == 2 & self.__checkDealerAs():
                print()

            elif self.outputPlayer == 3 & self.isPrimerTurno:
                self.apuesta = self.apuesta * 2

        elif self.gameState == 3:
            if self.outputPlayer == 0:
                self.__dealCardDealer()
                
            elif self.outputPlayer == 1:
                self.__dealCard(self.manoJugador)

                if self.__checkWinner():
                    self.gameState = 6

                self.__dealCardDealer()

                if self.__checkWinner():
                    self.gameState = 6

        elif self.gameState == 4:
            print()

        elif self.gameState == 5:
            print()

        elif self.gameState == 6:
            if self.playerWin:
                self.presupuesto = self.presupuesto + self.apuesta
            else:
                self.presupuesto = self.presupuesto - self.apuesta

    def __checkWinner(self):
        if self.__checkBlowCards():
            return True
        elif self.__checkBlackjack():
            return True
        elif self.__checkBiggerCard():
            return True

        return False

    def __checkBiggerCard(self):
        if self.manoJugador.get_valor() > self.manoDealer.get_valor():
            self.playerWin = True
        else:
            self.playerWin = False

    def __checkBlowCards(self):
        if self.manoJugador.get_valor() > 21:
            self.playerWin = False
            return True

        if self.manoDealer.get_valor() > 21:
            self.playerWin = True
            return True

        return False

    def __checkBlackjack(self):
        if self.manoJugador.get_valor() == 21:
            self.playerWin = True
            return True

        if self.manoDealer.get_valor() == 21:
            self.playerWin = False
            return True

        return False

    def __dealInitialCards(self):
        for i in range(2):
            self.__dealCard(self.manoJugador)
            self.__dealCard(self.manoDealer)

    def __dealCard(self, Hand):
        Hand.add_Carta(self.mazo.deal())

    def __dealCardDealer(self, Hand):
        if self.manoDealer.get_valor() < 17:
            self.__dealCard(self.manoDealer)

    def __getConteo(self, Hand):
        return Hand.valor        

    def __checkDealerAs(self):
        if(self.isPrimerTurno & ("A" in self.__getConteo(self.manoDealer)[1])):
            return True

    def __getCards(self, Hand):
        # NumeroTipoCarta
        cards = []

        for carta in Hand.Cartas:
            valor = carta.valor
            tipo = ""

            if carta.suit   == "Espadas":
                tipo = "S"
            elif carta.suit == "Diamantes":
                tipo = "D"
            elif carta.suit == "Treboles":
                tipo = "C"
            elif carta.suit == "Corazones":
                tipo = "H"

            cards.append(valor + tipo)

        return cards

    # Communication Functions

    def getGameState(self):
        return self.gameState

    def gamePlayerWin(self):
        return self.playerWin

    def getPresupuesto(self):
        return self.prespuesto

    def setReady(self, Ready):
        self.ready = Ready

    def getConteoAI(self):
        return self.__getConteo(self.manoJugador)

    def getConteoDealer(self):
        if(self.isPrimerTurno):
            return self.__getConteo(self.manoDealer)[1]

        return self.__getConteo(self.manoDealer)

    def getCardsAI(self):
        return self.__getCards(self.manoJugador)

    def getCardsDealer(self):
        return self.__getCards(self.manoDealer)

    def setApuesta(self, apuestaAmount):
        self.apuesta = apuestaAmount
