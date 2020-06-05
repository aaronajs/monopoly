# represents a player of the game

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

    def takeTurn(self, movePlayer):
        # decision = self.makeDecision("what to do? ", ["roll", "build", "sell", "offer"])
        # opportunity to do other stuff
        movePlayer(self) # ready to roll dice and move
        # (add functionality to do other stuff afterwards too until end turn)

    def leaveJail(self, fine):
        self.doublesRolled = 0
        self.money -= fine
        self.timeInJail = -1

    def buyProperty(self, prop):
        self.money -= prop.value
        prop.owner = self
        self.properties.append(prop)

    def sellProperty(self, prop, other, price):
        self.properties.remove(prop)
        other.properties.append(prop)
        self.money += price
        other.money -= price

    def mortgageProperty(self, index):
        prop = self.properties[index]
        prop.isMortgaged = True
        self.money += prop.mortgage

    def unmortgageProperty(self, index):
        prop = self.properties[index]
        prop.isMortgaged = True
        self.money -= prop.mortgage * 1.1 # 10% extra

    def canAfford(self, payment): return self.money - payment >= 0

    def isBankrupt(self, other):
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

    def makeDecision(self, query, options):
        while True:
            try:
                decision = input(query + " ")
                if str.lower(decision) in options: break
                else: continue
            except: print("error")
        return decision
    
    def choosePrice(self):
        while True:
            try:
                price = input(query + " ")
                if isinstance(price, int): break
                else: continue
            except: print("error")
        return price

    def __str__(self): 
        position = str(Player.board[self.position])
        if self.position == 10 and self.timeInJail == -1: position += " (visiting)"
        return self.token + " " + str(self.money) + " " + position + "(" + str(self.position) + ")"