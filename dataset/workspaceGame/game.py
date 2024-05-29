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

class GameAI():
    def __init__(self, presupuesto):
        # Paso realizado
        # Para permitir la comunicacion entre la IA y el juego
        self.ready = False

        # Estado de juego
        # 0 = Esperando cantidad de apuesta
        # 1 = Inicio de partida
        # 2 = Mid game

        # 3 = El dealer tiene As - Solo esta activo el dealer tiene 2 cartas

        # 4 = El jugador ha solicitado split - Solo esta activo en el inicio del juego y el jugador tiene dos  cartas iguales
        # 5 = El jugador ha solicitado doblar - Solo esta activo en el inicio del juego

        # 6 = Juego finalizado

        self.gameState = 0
        self.isPrimerTurno = False

        # Outputs jugador
        # 0 = Seguir
        # 1 = Quedarse
        # 2 = Split
        # 3 = Doblar
        self.outputPlayer = 0

        # Estado ganador
        # 0 Player Wins
        # 1 Draw
        # 2 Dealer Wins
        self.winner = 4

        # Configuracion para IA
        self.presupuesto = presupuesto
        self.apuesta = 0

        # Inicio clases
        self.mazo = Mazo()
        self.manoJugador = Mano()
        self.manoDealer = Mano(dealer=True)

    def __reset(self):
        self.ready = False
        self.gameState = 0
        self.isPrimerTurno = False
        self.outputPlayer = 0
        self.winner = 4
        
        self.apuesta = 0

        self.mazo = Mazo()
        self.manoJugador = Mano()
        self.manoDealer = Mano(dealer=True)

    def __game(self):
        # Esto se activa si el dealer tiene As
        # if self.__checkDealerAs():
        #    self.gameState = 4

        if self.ready == False:
            return

        if self.gameState == 0:
            self.gameState = 1
            self.ready = False

        elif self.gameState == 1:
            self.gameState = 2
            self.isPrimerTurno = True
            self.__dealInitialCards()

        # En este momento se pregunta al jugador si seguir o quedarse.
        # Actualmente todavia no se consideran los casos como split o doblar

        elif self.gameState == 2:
            # El jugador ha solicitado una carta adicional
            if self.outputPlayer == 0:
                # Se entrega carta al jugador
                self.__dealCard(self.manoJugador)

                # Se verifica si los jugadores han llegado a blackjack o ha superado 21
                # Si es correcto se va directo a juego finalizado
                if self.__checkWinner():
                    self.gameState = 6

                # Se entrega carta al dealer
                # ToDo verificar si las cartas de dealer ya son 17 antes de entregar una nueva carta
                self.__dealCard(self.manoDealer)

                # Se verifica si los jugadores han llegado a blackjack, han superado 21 o volaron
                # Si es correcto se va directo a juego finalizado
                if self.__checkWinner():
                    self.gameState = 6

            # El jugador ha solicitado quedarse con las cartas que tiene
            # El dealer se va a entregar cartas hasta que supere el numero minimo
            elif self.outputPlayer == 1:
                self.__dealCardDealer()

                # Se verifica si los jugadores han llegado a blackjack, han superado 21 o volaron
                # Si es correcto se va directo a juego finalizado
                if self.__checkWinner():
                    self.gameState = 6

        # ToDo si el dealer tiene As
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

        # ToDo si el jugador ha solicitado split
        elif self.gameState == 4:
            print()

        # ToDo si el jugador ha solicitado doblar
        elif self.gameState == 5:
            print()

        elif self.gameState == 6:
            if self.winner == 0:
                self.presupuesto = self.presupuesto + self.apuesta
            elif self.winner == 2:
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
        if self.manoJugador.get_valor() == self.manoDealer.get_valor():
            self.winner = 1
            return True
        elif self.manoJugador.get_valor() > self.manoDealer.get_valor():
            self.winner = 0
            return True
        elif self.manoJugador.get_valor() < self.manoDealer.get_valor():
            self.winner = 2
            return True
        return False

    def __checkBlowCards(self):
        if self.manoJugador.get_valor() > 21 and self.manoDealer.get_valor() > 21:
            self.winner = 1
            return True 
        elif self.manoJugador.get_valor() > 21:
            self.winner = 2
            return True
        elif self.manoDealer.get_valor() > 21:
            self.winner = 0
            return True

        return False

    def __checkBlackjack(self):
        if self.manoJugador.get_valor() == 21 and self.manoDealer.get_valor() == 21:
            self.winner = 1
            return True
        elif self.manoJugador.get_valor() == 21:
            self.winner = 0
            return True
        elif self.manoDealer.get_valor() == 21:
            self.winner = 2
            return True

        return False

    def __dealInitialCards(self):
        self.mazo.shuffle()

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
        if(self.manoDealer.getCount() == 2 & ("A" in self.__getCards(self.manoDealer)[1])):
            return True
        return False

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

    def setOutputPlayer(self, output):
        self.outputPlayer = output
    
    def getGameState(self):
        return self.gameState

    def gameWin(self):
        return self.winner

    def getPresupuesto(self):
        return self.prespuesto

    def setReady(self, Ready):
        self.ready = Ready

    def getCardsAI(self):
        return self.__getCards(self.manoJugador)

    def getCardsDealer(self):
        return self.__getCards(self.manoDealer)

    def setApuesta(self, apuestaAmount):
        self.apuesta = apuestaAmount 
