import random

from dataset.workspaceGame.Model1.cartas import Carta

class Mazo: 
    def __init__(self): 
        self.Cartas = [Carta(s, v) for _ in range(5) for s in["Espadas" , "Treboles" , "Corazones", 
        "Diamantes"] for v in ["A" ,"2" ,"3" ,"4" ,"5" ,"6" 
        ,"7" ,"8" ,"9" ,"10" , "J" , "Q" , "K"] ]

    def shuffle(self):
        if len(self.Cartas) > 1:
            random.shuffle(self.Cartas)
    
    def deal(self):
        if len(self.Cartas) > 1:
            return self.Cartas.pop(0)
        
    