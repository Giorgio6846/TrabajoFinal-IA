class Carta: 
    def __init__(self, suit , valor): 
        self.suit = suit 
        self.valor = valor 
    
    def __repr__(self):
        return " de " .join((self.valor , self.suit))