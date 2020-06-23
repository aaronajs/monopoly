import random
# represents Action squares on board and chance + community chest CardDecks
class Action:

    def __init__(self, name):
        self.name = name

    def __str__(self): return self.name


# Using Mononpoly Grab & Go version of CardDecks
class CardDeck(Action): 

    def __init__(self, name, details):
        Action.__init__(self, name)
        self.index = list(range(1,19))
        self.used = []
        self.details = details # index : (description, action)

    def giveGetOutOfJailFreeCard(self, player): player.getOutOfJailFreeCards += 1

    def updateCardDecks(self):
        if not self.index:
            print("empty deck")
            self.index = self.used # check copying works
            self.used = []
        card = random.choice(self.index)
        self.index.remove(card)
        self.used.append(card)
        return self.details[card]
        
class CommunityChest(CardDeck):
    # 3x GOJF Cards

    # Bank pays dividend of £50.
    # Your building loan matures; receive £150.
    # You have won a crossword competition; collect £100.

    # Speeding fine: £15.
    # Pay school fees of £150.
    # 'Drunk in charge'; £20 fine.
    
    # You are assessed for Street repairs: £40 per house, £115 per hotel.
    # Make general repairs on all of your buildings: £25 per house, £100 per hotel.
    
    # Advance to Trafalgar Square; if you pass Go, collect £200.
    # Advance to Go.
    # Advance to Mayfair.
    # Advance to Pall Mall; if you pass Go, collect £200,
    # Take a trip to Marylebone Station; if you pass Go, collect £200.
    # Go to jail.
    # Go back three spaces.

    def __init__(self, name):
        details = {
            1: "Get out of jail free",
            2: "Get out of jail free",
            3: "Get out of jail free",
            4: "Bank pays dividend of £50.",
            5: "Your building loan matures; receive £150.",
            6: "You have won a crossword competition; collect £100.",
            7: "Speeding fine: £15.",
            8: "Pay school fees of £150.",
            9: "'Drunk in charge'; £20 fine.",
            10: "You are assessed for Street repairs: £40 per house, £115 per hotel.",
            11: "Make general repairs on all of your buildings: £25 per house, £100 per hotel.",
            12: "Advance to Trafalgar Square; if you pass Go, collect £200.",
            13: "Advance to Go.",
            14: "Advance to Mayfair.",
            15: "Advance to Pall Mall; if you pass Go, collect £200.",
            16: "Take a trip to Marylebone Station; if you pass Go, collect £200.",
            17: "Go to jail.",
            18: "Go back three spaces."
        }

        CardDeck.__init__(self, name, details)

class Chance(CardDeck):
    # 3x GOJF Cards

    # Bank error in your favour; collect £200.
    # You have won second prize in a beauty contest; collect £10.
    # Income tax refund; collect £20.
    # From sale of stock you get £50.
    # Receive interest in 7% preference shares: £25.
    # Annuity matures; collect £100.
    # You inherit £100.

    # Pay hospital £100.
    # Pay your insurance premium £50.
    # Doctor's fee; pay £50.

    # Pay a £10 fine or take a chance.
    # It's your birthday; collect £10 from each player
    
    # Advance to Go.
    # Go back to Old Kent Road.
    # Go to jail.

    def __init__(self, name):
        CardDeck.__init__(self, name, {})

if __name__ == "__main__":
    cards = CommunityChest("Community Chest")
    x = 0
    while x < 30:
        x += 1
        print(cards.updateCardDecks())