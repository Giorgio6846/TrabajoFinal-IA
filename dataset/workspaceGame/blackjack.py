import random 

class Carta: 
    def __init__(self, suit , valor): 
        self.suit = suit 
        self.valor = valor 
    
    def __repr__(self):
        return " de " .join((self.valor , self.suit))

class mazo: 
    def __init__(self): 
        self.Cartas = [Carta(s, v) for _ in range(5) for s in["Espadas" , "Treboles" , "Corazones ", 
        "Diamantes"] for v in ["A" ,"2" ,"3" ,"4" ,"5" ,"6" 
        ,"7" ,"8" ,"9" ,"10" , "J" , "Q" , "K"] ]

    def shuffle(self):
        if len(self.Cartas) > 1:
            random.shuffle(self.Cartas)
    
    def deal(self):
        if len(self.Cartas) > 1:
            return self.Cartas.pop(0)

class Mano: 
    def __init__(self , dealer = False):
        self.dealer = dealer 
        self.Cartas = []
        self.valor = 0 

    def add_Carta(self, Carta):
        self.Cartas.append(Carta)

    def calculate_valor(self):
        self.valor = 0 
        has_ace = False
        for Carta in self.Cartas:
            if Carta.valor.isnumeric():
                self.valor += int(Carta.valor)
            else:
                if Carta.valor == "A":
                    has_ace = True
                    self.valor += 11
                else:
                    self.valor += 10
        
        if has_ace and self.valor > 21: 
            self.valor -= 10 
    
    def get_valor(self):
        self.calculate_valor()
        return self.valor
    
    def display_all(self):
        for Carta in self.Cartas:
            print(Carta)

    def display(self):
        if self.dealer: 
            print("Carta volteada")
            print(self.Cartas[1])
        else:
            for Carta in self.Cartas: 
                print(Carta)
            print("Total:" , self.get_valor())


class Game: 
    def __init__(self):
        pass 

    def play(self):
        playing = True 
        presupuesto = 100
        while playing and presupuesto>0: 
            self.mazo = mazo()
            self.mazo.shuffle()
            
            print("Presupuesto actual: ", presupuesto)
            while True:
                apuesta = int(input("Escoge la cantidad de tu apuesta: "))
                
                if apuesta <= presupuesto:
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
                        presupuesto = presupuesto-apuesta
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
                        presupuesto = presupuesto+apuesta
                        print("Usted ha ganado!")
                    elif jugador_Mano_valor == dealer_Mano_valor:
                        print("Empate!")
                    else: 
                        presupuesto = presupuesto-apuesta
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

        return jugador , dealer 
    
    def show_blackjack_results(self , jugador_has_blackjack , dealer_has_blackjack):
        if jugador_has_blackjack and dealer_has_blackjack:
            print("Mano del dealer:")
            self.dealer_Mano.display_all()
            print("Mano del jugador:")
            self.jugador_Mano.display_all()

            print("Los dos jugadores tienen blackjack! Draw!")

        elif jugador_has_blackjack:
            print("Mano del jugador:")
            self.jugador_Mano.display_all() 
            presupuesto = presupuesto+apuesta
            print("Usted tiene blackjack! Usted gana!")
        
        elif dealer_has_blackjack:
            print("Mano del dealer:")
            self.dealer_Mano.display_all()
            presupuesto = presupuesto-apuesta
            print("El dealer tiene blackjack! El dealer gana!")

if __name__ == "__main__":
    g = Game()
    g.play()
            
