import random
from Player import Player
from Action import Card
from Property import Property, Street, Station, Utility 
from BoardBuilder import BoardBuilder
from Controller import Controller
# controls the game

class Game:

    def __init__(self, board, controller):
        self.players = [] # list of all players and their position
        self.board = board # represents the board, 40 squares
        self.turn = 0 # index of self.players
        self.activePlayers = 0
        self.doubleRolled = False
        self.controller = controller

    ### NOTE: Controls game flow
    def startGame(self, players): # chooses player to go first
        self.players = players # all start at go
        self.activePlayers = len(players)
        highestRoll = 0
        first = self.players[0]
        for player in self.players: 
            if sum(self.rollDice()) > highestRoll: first = player
        print (first.token + " is going first")
        self.turn = self.players.index(first) # which player goes first
        self.playGame()

    def playGame(self): # runs the game
        while self.activePlayers > 1:
            player = self.players[self.turn]
            if not self.doubleRolled: self.turn = self.turn + 1 if self.turn < self.activePlayers - 1 else 0
            rolled = False
            while True:
                decision = self.controller.choosePlayerAction(player, rolled)
                if decision == "m": self.playerMortgagesProperty(player)
                elif decision == "u": self.playerUnmortgagesProperty(player)
                elif decision == "p": self.playerSellsProperty(player)
                elif decision == "h": self.playerBuysHouse(player)
                elif decision == "s": self.playerSellsHouse(player)
                elif decision == "o": print("make offer") #TODO: offer functionality
                elif decision == "b": self.playerGoesBankrupt(player)
                elif decision == "r": 
                    self.movePlayer(player)
                    rolled = True
                elif decision == "e": break  
        print("Winner: " + self.players[0])
    ###

    def rollDice(self): return [random.randint(1,6),random.randint(1,6)]

    ### NOTE: controls player position around board
    def movePlayer(self, player): # TODO: finishing moving protocols
        dice = self.rollDice()
        moveSpaces = sum(dice)

        if dice[0] == dice[1]: 
            player.doublesRolled += 1
            print(player.token + ": double rolled")
            self.doubleRolled = True
        else: 
            player.doublesRolled = 0
            self.doubleRolled = False

        if player.timeInJail == -1: # player not in jail
            if player.doublesRolled == 3: # got to jail for 3 doubles in a row
                self.sendPlayerToJail(player)
                print(player.token + " rolled 3 doubles, goes to jail")
            else: 
                self.newPlayerPosition(player, moveSpaces)
        else: self.tryToLeaveJail(player, moveSpaces)
        print(str(player)+"\n")

    def newPlayerPosition(self, player, moveSpaces):
        # controls the outcome of where the player lands
        newPosition = player.position + moveSpaces

        # TODO: simplify, organise by instances

        # jail, passing go
        if newPosition == 30: # player lands on go to jail, goes to jail, doesn't pass go/collects 200
            self.sendPlayerToJail(player)
            print(player.token + " go to jail!")
        else:
            if newPosition >=40: # player passes go
                newPosition -= 40
                player.money += 200
                print(player.token + " passes go")
            player.position = newPosition # moves the player

            # taxes
            tax = 0
            if newPosition == 4: tax = 200 # player pays income tax
            elif newPosition == 38: tax = 100 # player pays super tax
            if tax != 0:
                while player in self.players and not player.canAfford(tax): 
                    self.playerNeedsMoney(player)
                if player in self. players: player.money -= tax

            # rent (utilities, stations, properties)
            prop = board[newPosition]
            if isinstance(prop, Property):
                owner = prop.owner
                if owner is None: # property is unowned
                    # player can buy it, or get bank to auction property
                    query = player.token + ": (b)uy or (a)uction " + prop.name + "?"
                    options = ["b", "a"]
                    decision = self.controller.makeDecision(query, options)
                    if decision == "b": self.playerBuysProperty(player, prop)

                    else: print(player.token + " can't afford " + prop.name) # TODO: auction by default
                
                else: # property is owned by a player
                    print("owned by", owner.token)
                    if owner is not player and not prop.isMortgaged:
                        if isinstance(prop, Station): rentOwed = prop.rent * 2^(owner.stationsOwned - 1) 
                        elif isinstance(prop, Utility): rentOwed = moveSpaces * (3^owner.utilitiesOwned +1)
                        elif isinstance(prop, Street): 
                            rentOwed = prop.rent[prop.numberOfHouses] 
                            if prop.colourSetOwned and prop.numberOfHouses == 0: rentOwed *= 2

                        while player in self.players and not player.canAfford(rentOwed):
                            self.playerNeedsMoney(player, owner)
                        if player in self.players:
                            player.money -= rentOwed
                            owner.money += rentOwed
                            print(player.token + " pays rent (" + str(rentOwed) + ") to " + owner.token)

            # elif isinstance(prop, Card): print (player.token + " landed on chance or community chest")
    ###

    ### NOTE: controls jail movement
    def sendPlayerToJail(self, player):
        player.timeInJail = 0
        player.position = 10
        player.doublesRolled = 0

    def playerLeavesJail(self, player, moveSpaces, fine=0):
        player.leaveJail(fine)
        self.newPlayerPosition(player, moveSpaces)
        print(player.token + " leaves jail")
    
    def tryToLeaveJail(self, player, moveSpaces):
        if player.doublesRolled == 1: 
            self.playerLeavesJail(player, moveSpaces)
            print(player.token + "rolled a double")
        else: 
            player.timeInJail += 1
            if player.timeInJail == 3: 
                while player in self.players and not player.canAfford(50): 
                    self.playerNeedsMoney(player)
                if player in self.players: self.playerLeavesJail(player, moveSpaces, 50)
            else: # in jail for less than 3 turns; give options based on GOJF card
                if player.getOutOfJailFreeCards > 0:
                    query = "(p)ay 50 or use GO(j)F card, or (w)ait for next turn?"
                    options = ["w", "p", "j"]
                else:
                    query = "(p)ay 50 or (w)ait for next turn??"
                    options = ["w", "p"]
                decision = self.controller.makeDecision(query, options)
                if decision == "p": 
                    while player in self.players and not player.canAfford(50): 
                        self.playerNeedsMoney(player)
                    if player in self.players: self.playerLeavesJail(player, moveSpaces, 50)
                elif decision == "j": self.playerLeavesJail(player, moveSpaces)
    ###

    ### NOTE: deals with housing
    def playerBuysHouse(self, player): # add buy at colour set level
        buildableStreets = [prop for prop in player.properties if isinstance(prop, Street) and prop.colourSetOwned and prop.numberOfHouses < 5 and all(prop.numberOfHouses <= street.numberOfHouses for street in Street.colourSets[prop.colour])]
        options = [str(index) for index in range(len(buildableStreets))]
        if options:
            for index in options:
                prop = buildableStreets[int(index)]
                print(index + ": " + str(prop) + "," + str(prop.houseCost))
            query = "Which property do you want to build a house on?"
            decision = self.controller.makeDecision(query, options)
            street = buildableStreets[int(decision)]
            while player in self.players and not player.canAfford(street.houseCost): 
                self.playerNeedsMoney(player)
            player.buyHouse(street)
        else: print("there are no properties " + player.token + " can build houses on")

    def playerSellsHouse(self, player): # add sell at colour set level
        props = player.getPropertiesWithHouses()
        options = [str(index) for index in range(len(props))]
        for index in options:
            prop = props[int(index)]
            print(index + ": " + str(prop) + "," + str(prop.houseCost*0.5))
        query = "From which property do you want to sell a house?"
        decision = self.controller.makeDecision(query, options)
        street = props[int(decision)]
        player.sellHouse(street)
    ###

    ### NOTE: deals with mortgaging
    def playerMortgagesProperty(self, player):
        props = player.getUnmortgagedProperties()
        options = [str(index) for index in range(len(props))]
        for index in options: print(str(index) + ": " + str(props[int(index)]))
        query = "Which property to mortgage? (enter number)"
        decision = int(self.controller.makeDecision(query, options))
        player.mortgageProperty(player.properties[decision])

    def playerUnmortgagesProperty(self, player):
        props = list(filter(lambda prop: (prop.isMortgaged == True), player.properties))
        options = [str(index) for index in range(len(props))]
        for index in options: print(str(index) + ": " + str(props[int(index)]))
        query = "Which property to unmortgage? (enter number)"
        decision = int(self.controller.makeDecision(query, options))
        prop = props[decision]
        while player in self.players and not player.canAfford(prop.mortgage*1.1): 
            self.playerNeedsMoney(player)
        player.unmortgageProperty(prop)
    ###

    ### deals with buying and selling property
    def playerBuysProperty(self, player, prop):
        while player in self.players and not player.canAfford(prop.value):
            print(player.token + " can't afford " + prop.name + "; it costs " + str(prop.value))
            self.playerNeedsMoney(player)
        if player in self.players:
            player.buyProperty(prop)

    def playerSellsProperty(self, player): #TODO: change to check for unsold houses before this?
        options = [str(index) for index in range(len(player.properties))]
        for index in options: 
            print(index + ": " + str(player.properties[int(index)]))
        query = "Which property to sell? (enter number)"
        decision = self.controller.makeDecision(query, options)
        prop = player.properties[int(decision)]
        # TODO: add option to sell buildings straight away
        if isinstance(prop, Street) and prop.numberOfHouses != 0: print("sell houses first") 
        else: # sell property to another player
            buyers = [buyer for buyer in self.players if buyer != player]
            options = [str(index) for index in range(len(buyers))]
            for index in options: print(str(index) + ": " + str(buyers[int(index)]))
            # options = [buyer.token for buyer in self.players if buyer != player]
            query = "Sell property to another player: (enter number)" # + str(options)
            decision = buyers[int(self.controller.makeDecision(query, options))]
            # TODO: players must agree on a price before the transaction goes through
            # for now leave as agree outside game
            # ensure that it's within range of BOTH players of the game
            price = int(self.controller.choosePrice("what price to sell to " + str(decision))) # BUG: infinite loop?
            player.sellProperty(prop, decision, price)

    ### NOTE: deals with insufficient finances
    def playerNeedsMoney(self, player, owner=None):
        print(player.token + " has " + str(player.money))
        if not player.properties: self.playerGoesBankrupt(player, owner)
        else: 
            query = player.token + ": declare (b)ankruptcy, sell a (p)roperty"
            options = ["p", "b", "h", "m"]
            decision = self.controller.makeDecision(query, options)
            if decision == "p": self.playerSellsProperty(player)
            elif decision == "b": self.playerGoesBankrupt(player, owner)
            elif decision == "m": self.playerMortgagesProperty(player)
            elif decision == "h": self.playerSellsHouse(player)

    def playerGoesBankrupt(self, player, owner=None):
        player.isBankrupt(owner) #TODO what to do when owner is bank
        if player in self.players: self.players.remove(player)
        self.activePlayers -= 1
        # TODO: check if destroy player object?
        print(player.token + " is bankrupt!")
        # TODO: default end turn
    ###
    
if __name__ == "__main__":
    board = BoardBuilder().build("default")
    game = Game(board, Controller())
    Player.board = board
    dog = Player("dog")
    cat = Player("cat")
    game.startGame([dog, cat])
    