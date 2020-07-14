import random
# represents Action squares on board and chance + community chest CardDecks
class Action:

    def __init__(self, name):
        self.name = name

    def __str__(self): return self.name


# Using Monopoly Grab & Go version of CardDecks

    # each class has global dictionary of cards
    # each instance represents a Card Square
    # randomly select and remove card -- reset if empty

    # return name of card and action + parameters
        # print name of card
        # action + param format
            # series of numbers, correspond to functions which can be executed in the Game class
            # name of method + actual parameters (ideal)
            #! ensure that all functions can be made in Game class -- do this first?

    #! card action codes
    # 0: give GOJF card
    
    # 1: collect money
    # 2: fined money

    # 3: building repairs

        # replace specific places with board position general places
    # 4: Advance/go back to square
    # 5: Move back three spaces

    # 6: go to jail

    # 7: fine or chance
    # 8: collect birthday money from each player


class Chance(): 
    cards = {
        1: ("Get out of jail free",0),
        2: ("Get out of jail free",0),
        3: ("Get out of jail free",0),
        4: ("Bank pays dividend of £50.",1,50),
        5: ("Your building loan matures; receive £150.",1,150),
        6: ("You have won a crossword competition; collect £100.",1,100),
        7: ("Speeding fine: £15.",2,15),
        8: ("Pay school fees of £150.",2,150),
        9: ("'Drunk in charge'; £20 fine.",2,20),
        10: ("You are assessed for Street repairs: £40 per house, £115 per hotel.",3,40,115),
        11: ("Make general repairs on all of your buildings: £25 per house, £100 per hotel.",3,25,100),
        12: ("Advance to Trafalgar Square; if you pass Go, collect £200.",4,1,24),
        13: ("Advance to Go.",4,1,0),
        14: ("Advance to Mayfair.",4,1,39),
        15: ("Advance to Pall Mall; if you pass Go, collect £200.",4,1,11),
        16: ("Take a trip to Marylebone Station; if you pass Go, collect £200.",4,1,15),
        17: ("Go to jail.",6),
        18: ("Go back three spaces.",5)
    }
    availableCards = []

    @staticmethod
    def selectCard():
        if not Chance.availableCards: 
            Chance.availableCards = list(range(1,19))
        cardNumber = random.choice(Chance.availableCards)
        Chance.availableCards.remove(cardNumber)
        return Chance.cards[cardNumber]

class CommunityChest():
    cards = {
        1: ("Get out of jail free",0),
        2: ("Get out of jail free",0),
        3: ("Get out of jail free",0),
        4: ("Bank error in your favour; collect £200.",1,200),
        5: ("You have won second prize in a beauty contest; collect £10.",1,10),
        6: ("Income tax refund; collect £20.",1,20),
        7: ("From sale of stock you get £50.",1,50),
        8: ("Receive interest in 7% preference shares: £25.",1,25),
        9: ("Annuity matures; collect £100.",1,100),
        10: ("You inherit £100.",1,100),
        11: ("Pay hospital £100.",2,100),
        12: ("Pay your insurance premium £50.",2,50),
        13: ("Doctor's fee; pay £50.",2,50),
        14: ("Pay a £10 fine or take a chance.",7),
        15: ("It's your birthday; collect £10 from each player.",8),
        16: ("Advance to Go.",4,1,0),
        17: ("Go back to Old Kent Road.",4,0,1),
        18: ("Go to jail.")
    }
    availableCards = []

    @staticmethod
    def selectCard():
        if not CommunityChest.availableCards: 
            CommunityChest.availableCards = list(range(1,19))
        cardNumber = random.choice(CommunityChest.availableCards)
        CommunityChest.availableCards.remove(cardNumber)
        return CommunityChest.cards[cardNumber]
