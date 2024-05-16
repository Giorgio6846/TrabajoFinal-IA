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
        # 1 = Esperando movimiento de la IA
        # 3 = Juego finalizado
        self.gameState = 0

        self.isPrimerTurno = False

        # Jugador gano
        self.playerWin = False

        # Configuracion para IA
        self.presupuesto = presupuesto
        self.cantidadApuesta = 0

        # Inicio clases
        self.mazo = Mazo()
        self.manoJugador = Mano()
        self.manoDealer = Mano(dealer=True)

    def game(self):
        if self.gameState == 0:
            self.isPrimerTurno = True
            self.dealInitialCards()
            
        elif self.gameState == 1:
            print()
        elif self.gameState == 2:
            print()

    def dealInitialCards(self):
        for i in range(2):
            self.dealCard(self.manoJugador)
            self.dealCard(self.manoDealer)

    def dealCard(self, Hand):
        Hand.add_Carta(self.mazo.deal())

    def getGameState(self):
        return self.gameState

    def gamePlayerWin(self):
        return self.playerWin

    def getPresupuesto(self):
        return self.prespuesto

    def getCards(self, Hand):
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

    def getConteo(self, Hand):
        return Hand.valor        

    def getConteoAI(self):
        return self.getConteo(self.manoJugador)

    def getConteoDealer(self):
        if(self.isPrimerTurno):
            return self.getConteo(self.manoDealer)[1]
        else:                
            return self.getConteo(self.manoDealer)

    def getCardsAI(self):
        return self.getCards(self.manoJugador)

    def getCardsDealer(self):
        return self.getCards(self.manoDealer)
