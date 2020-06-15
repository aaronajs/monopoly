# represents a player of the game
from Property import Street, Utility, Station
class Player:

    board = []

    def __init__(self, token):
        self.token = token
        self.money = 1500 # starting amount
        self.properties = []
        self.getOutOfJailFreeCards = 0
        self.timeInJail = -1 # -1 is not in jail
        self.stationsOwned = 0
        self.utilitiesOwned = 0
        self.doublesRolled = 0 # to track 3 doubles in a row
        self.position = 0

    # def takeTurn(self, movePlayer):
    #     # decision = self.makeDecision("what to do? ", ["roll", "build", "sell", "offer"])
    #     # TODO: opportunity to do other stuff
    #     movePlayer(self) # ready to roll dice and move
    #     # TODO: (add functionality to do other stuff afterwards too until end turn)

    def leaveJail(self, fine):
        self.doublesRolled = 0
        self.money -= fine
        self.timeInJail = -1

    def buyProperty(self, prop):
        self.money -= prop.value
        prop.owner = self
        self.properties.append(prop)
        if isinstance(prop, Station): self.stationsOwned += 1
        if isinstance(prop, Utility): self.utilitiesOwned += 1
        # check if colour set
        if isinstance(prop, Street):
            colourSet = Street.colourSets[prop.colour]
            if all(street.owner == self for street in colourSet):
                for street in colourSet: street.colourSetOwned = True
                print(self.token + " owns the colour set " + prop.colour)

    def sellProperty(self, prop, other, price): #TODO: check if removing a property from colour set
        self.properties.remove(prop)
        other.properties.append(prop)
        self.money += price
        other.money -= price
        if isinstance(prop, Station): 
            self.stationsOwned -= 1
            other.stationsOwned += 1
        if isinstance(prop, Utility): 
            self.utilitiesOwned -= 1
            other.utilitiesOwned += 1

    def mortgageProperty(self, prop):
        prop.isMortgaged = True
        self.money += prop.mortgage

    def unmortgageProperty(self, prop):
        prop.isMortgaged = True
        self.money -= prop.mortgage * 1.1 # 10% extra

    def buyHouse(self, street):
        street.numberOfHouses += 1
        self.money -= street.houseCost

    def sellHouse(self, street):
        street.numberOfHouses -= 1
        self.money += street.houseCost*0.5

    def canMortgageProperties(self): return next((prop for prop in self.properties if prop.canMortgage()), None)
    def canUnmortgageProperties(self): return next((prop for prop in self.properties if prop.isMortgaged), None)
    def canSellHouse(self): return next((prop for prop in self.properties if isinstance(prop, Street) and prop.canSellHouse()), None)
    def canBuyHouse(self): return next((prop for prop in self.properties if isinstance(prop, Street) and prop.canBuyHouse()), None)

    # return unmortgaged properties that aren't a street, or if they are a street, they have no houses
    def getUnmortgagedProperties(self): return list(filter(lambda prop: (prop.isMortgaged == False and (not isinstance(prop, Street) or (isinstance(prop, Street) and prop.numberOfHouses == 0))), self.properties))

    def getPropertiesWithHouses(self): return list(filter(lambda prop: (isinstance(prop, Street) and prop.numberOfHouses != 0 and prop.colourSetOwned and all(prop.numberOfHouses <= street.numberOfHouses for street in Street.colourSets[prop.colour])), self.properties))


    def canAfford(self, payment): return self.money - payment >= 0

    def isBankrupt(self, other=None):
        # sell all houses and hotels at half price
        if other != None:
            other.getOutOfJailFreeCards += self.getOutOfJailFreeCards
            other.stationsOwned += self.stationsOwned
            other.utilitiesOwned += self.utilitiesOwned
            other.properties += self.properties
            other.money += self.money
        else:
            for prop in self.properties: 
                prop.owner = None 
                prop.isMortgages = False
                # auction all properties
        # check deleting objects? memory etc
        self.money = 0
        self.properties = []
        self.position = 0

    def __str__(self): 
        position = str(Player.board[self.position])
        if self.position == 10 and self.timeInJail == -1: position += " (visiting)"
        return self.token + " " + str(self.money) + " " + position + "(" + str(self.position) + ")"