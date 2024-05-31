import numpy as np

def translateArray(cards):
    array = np.zeros(13)

    for card in cards:
        print(card)
        cat = categoryCard(card)
        value = valueCard(card, cat)
        array[value - 1] = array[value - 1] + 1

    print(array)
    return array  
    
typesCards = ["S","D", "C", "H"]

def categoryCard(card):
    if typesCards[0] in card:
        return 0
    elif typesCards[1] in card:
        return 1
    elif typesCards[2] in card:
        return 2
    elif typesCards[3] in card:
        return 3
        
def valueCard(card, cat):
    value = card[0].split(typesCards[cat])[0]
    if value == "A":
        return 1
    elif value == "J":
        return 11
    elif value == "Q":
        return 12
    elif value == "K":
        return 13
    else:
        return int(value)

def countCards(arrayCards):
    arrayTMP = arrayCards
    count = 0
    ace = False
    for index in range(13):
        if arrayTMP[index] >= 1:
            if index == 0:
                ace = True
                if arrayTMP[index] == 2:
                    count = 21
                    ace = False
                else:
                    count = arrayTMP[index] * 1 + count
            elif index == 10:
                count = count + arrayTMP[index] * 10
            elif index == 11:
                count = count + arrayTMP[index] * 10
            elif index == 12:
                count = count + arrayTMP[index] * 10
            else: 
                count = count + arrayTMP[index] * (index + 1)

    if ace and count < 11:
        count = count + 11

    return count