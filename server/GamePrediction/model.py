import array
from fnmatch import translate
from sympy import true
import tensorflow as tf
import tensorflow.keras as models
import numpy as np

# Solo soporta archivos .keras
# Solo funciona en maquinas unix
model = models.load_model("./finished_1.keras")
typesCards = ["S", "D", "C", "H"]


def translateArray(cards):
    array = np.zeros(13)

    for card in cards:
        print(card["TypeCard"])
        cat = categoryCard(card["TypeCard"])
        value = valueCard(card["TypeCard"], cat)
        array[value - 1] = array[value - 1] + 1

    print(array)
    return array

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

    return count - 1

def parseCards(setCards):
    cardsParsed = []
    
    for card in setCards:
        toParse = True
        
        if len(cardsParsed) == 0:
            toParse = True
                
        else:
            for cardP in cardsParsed:
                if cardP["TypeCard"] == card["TypeCard"]:
                    toParse = False 
                    if card["Conf"] > cardP["Conf"]:
                        cardP["Conf"] = card["Conf"]
            
        if toParse:    
            cardsParsed.append(card) 
        
        return cardsParsed
           
    print(cardsParsed)

def gamePrediction(cardsDealerBoxes, cardsPlayerBoxes):
    state = states(cardsDealerBoxes, cardsPlayerBoxes)

    return np.argmax(
        model.predict(state, verbose=1, use_multiprocessing=True)[0]
    )

def states(cardsDealerBoxes, cardsPlayerBoxes):
    playerParsed = parseCards(cardsPlayerBoxes)
    dealerParsed = parseCards(cardsDealerBoxes)

    arrayPlayer = translateArray(playerParsed)
    arrayDealer = translateArray(dealerParsed)

    sumCardsDealer = countCards(arrayDealer)
    sumCardsPlayer = countCards(arrayPlayer)

    prob_21 = get_prob_of_bust(sumCardsPlayer)

    #Actualmente se va a asumir que no se puede selecionar double
    game_state = 0
    pos_double = pos_double(arrayPlayer)
    
    state = np.array(
            [
                sumCardsPlayer,
                sumCardsDealer,
                usable_ace,
                pos_double,
                prob_21,
                game_state,
            ]
        )

    state = state.astype(np.uint8)
    state = np.reshape(state, [1, 6])
    
    return state

def usable_ace(arrayPlayer, sumCardsPlayer):
    if sumCardsPlayer + 10 <= 21 and arrayPlayer[0] > 0:
        return True
    return False

def pos_double(arrayPlayer):
    for index in range(13):
        if arrayPlayer[index] == 2:
            return 1
        
    return 0

def get_prob_of_bust(sumCards):
    value_needed = 21 - sumCards
    # if value_needed < 0:
    #    return -1
    # if value_needed == 0:
    #    return 100  # Si ya está en 21 o más, la probabilidad de volar es del 100%
    # busting_cards = 0
    # for card in remaining_deck:
    #    card_value = card['number']
    #    if card_value in ['J', 'Q', 'K']:
    #        card_value = 10
    #    elif card_value == 'A':
    #        card_value = 11
    #    else:
    #        card_value = int(card_value)

    #    if card_value > value_needed:
    #        busting_cards += 1

    # total_cards = len(remaining_deck)
    # probability_of_bust = (busting_cards / total_cards) * 100
    # probability_of_bust = probability_of_bust/10

    probability_of_bust = abs(100 * value_needed / 21)
    probability_of_bust = probability_of_bust / 10

    probability_of_bust = round(probability_of_bust)

    if probability_of_bust > 10:
        probability_of_bust = 0

    return int(probability_of_bust)
