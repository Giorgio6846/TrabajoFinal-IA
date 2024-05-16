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