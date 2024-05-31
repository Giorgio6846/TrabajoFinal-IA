class Mano: 
    def __init__(self , isDealer = False):
        self.isDealer = isDealer 
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
        
        if self.isDealer:
            if has_ace and self.valor > 17: 
                self.valor -= 10
        else:        
            if has_ace and self.valor > 21: 
                self.valor -= 10 
        
    def get_valor(self):
        self.calculate_valor()
        return self.valor
    
    def display_all(self):
        for Carta in self.Cartas:
            print(Carta)

    def getCartas(self):
        return self.Cartas

    def getCount(self):
        return self.Cartas.size()

    def display(self):
        if self.dealer: 
            print("Carta volteada")
            print(self.Cartas[1])
        else:
            for Carta in self.Cartas: 
                print(Carta)
            print("Total:" , self.get_valor())
            
    #ToDo delete carta
    def deleteCarta(self):
        print()