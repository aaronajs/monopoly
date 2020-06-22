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
            while player in self.players:
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
                print(str(player)+"\n")
        print("Winner: " + str(self.players[0]))
    ###

    def rollDice(self): return [random.randint(1,6),random.randint(1,6)]

    ### NOTE: controls player position around board
    def movePlayer(self, player):
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
        else: 
            self.tryToLeaveJail(player, moveSpaces)

    def newPlayerPosition(self, player, moveSpaces):
        # controls the outcome of where the player lands
        newPosition = player.position + moveSpaces

        # TODO: simplify, organise by instances ----- check: Action: go to jail, taxes, cards; Properties

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
                    decision = self.controller.buyOrAuction(player, prop)
                    if decision == "b": self.playerBuysProperty(player, prop)
                    else: self.auctionProperty(prop)
                else: # property is owned by a player
                    print("owned by", owner.token)
                    if owner is not player and not prop.isMortgaged:
                        rentOwed = prop.calculateRent()
                        while player in self.players and not player.canAfford(rentOwed):
                            self.playerNeedsMoney(player, owner)
                        if player in self.players: player.payMoney(owner, rentOwed)

            # elif isinstance(prop, Card): print (player.token + " landed on chance or community chest")
    ###

    ### NOTE: controls jail movement; 
    def sendPlayerToJail(self, player): player.goToJail()

    def playerLeavesJail(self, player, moveSpaces, fine=0):
        self.doubleRolled = False # player can't double roll
        player.leaveJail(fine)
        self.newPlayerPosition(player, moveSpaces)
        print(player.token + " leaves jail")

    def playerPaysJailFine(self, player, moveSpaces):
        while player in self.players and not player.canAfford(50): 
            self.playerNeedsMoney(player)
        if player in self.players: self.playerLeavesJail(player, moveSpaces, 50)
    
    def tryToLeaveJail(self, player, moveSpaces): #TODO: adjust so actions happen in the right order.
        if player.doublesRolled == 1: self.playerLeavesJail(player, moveSpaces)
        else: 
            player.timeInJail += 1
            if player.timeInJail == 3: self.playerPaysJailFine(player, moveSpaces)
            else: 
                decision = self.controller.chooseJailAction(player)
                if decision == "p": self.playerPaysJailFine(player, moveSpaces)
                elif decision == "j": 
                    self.playerLeavesJail(player, moveSpaces)
                    player.getOutOfJailFreeCards -= 1
                # else try again later
    ###

    ### NOTE: deals with housing; TODO: test filters
    def playerBuysHouse(self, player): # add buy at colour set level
        street = self.controller.chooseProperty(player.getBuildableProperties(), "buyHouse")
        while player in self.players and not player.canAfford(street.houseCost): 
            self.playerNeedsMoney(player)
        if player in self.players: player.buyHouse(street)

    def playerSellsHouse(self, player): # add sell at colour set level
        street = self.controller.chooseProperty(player.getSellableHouses(), "sellHouse")
        player.sellHouse(street)
    ###

    ### NOTE: deals with mortgaging
    def playerMortgagesProperty(self, player):
        prop = self.controller.chooseProperty(player.getMortgagableProperties(), "mortgage")
        player.mortgageProperty(prop)

    def playerUnmortgagesProperty(self, player):
        prop = self.controller.chooseProperty(player.getUnmortgagableProperties(), "unmortgage")
        while player in self.players and not player.canAfford(int(prop.mortgage*1.1)): 
            self.playerNeedsMoney(player)
        player.unmortgageProperty(prop)
    ###

    ### deals with buying and selling property
    def playerBuysProperty(self, player, prop):
        while player in self.players and not player.canAfford(prop.value):
            print(player.token + " can't afford " + prop.name + "; it costs " + str(prop.value))
            self.playerNeedsMoney(player)
        if player in self.players: player.buyProperty(prop)

    def playerSellsProperty(self, player):
        prop = self.controller.chooseProperty(player.getSellableProperties(), "sellProp")
        # TODO: add option to sell buildings straight away
        buyer = self.controller.choosePlayer(list(filter(lambda other: (other != player), self.players)))
        # TODO: players must agree on a price before the transaction goes through
        price = int(self.controller.choosePrice("what price to sell to " + str(buyer) + "?"))
        player.sellProperty(prop, buyer, price)

    def auctionProperty(self, prop):
         print("auction property " + str(prop))

    ### NOTE: deals with finances and offers
    def playerNeedsMoney(self, player, owner=None):
        print(player.token + " has " + str(player.money))
        if not player.properties: self.playerGoesBankrupt(player, owner)
        else: 
            decision = self.controller.chooseFinancing(player)
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

    def playerMakesOffer(self, player):
        target = self.controller.choosePlayer(list(filter(lambda other: (other != player), self.players)))
        propsToOffer = self.controller.chooseMultipleProperties(player.getSellableProperties()) if player.properties else None
        moneyToOffer = int(self.controller.choosePrice("what money to give " + str(target) + "?"))
        propsToTake = self.controller.chooseMultipleProperties(target.getSellableProperties()) if target.properties else None
        moneyToTake = 0 if moneyToOffer != 0 else int(self.controller.choosePrice("what money to take from" + str(target) + "?"))
        print("\n"+ player.token + "offers to " + target.token + ":")
        for prop in propsToOffer: print(prop)
        if moneyToOffer: print("money: " + moneyToOffer)
        print("in exchange for:")
        for prop in propsToTake: print(prop)
        if moneyToTake: print("money: " + moneyToTake)
        targetDecision = self.controller.offerDecision(target)
        if targetDecision == "a": 
            print("Accepted")
            player.exchange(target, propsToOffer, moneyToOffer, propsToTake, moneyToTake)
        elif targetDecision == "r": print("Rejected")
    ###
    
if __name__ == "__main__":
    board = BoardBuilder().build("default")
    game = Game(board, Controller())
    Player.board = board
    dog = Player("dog")
    cat = Player("cat")
    game.startGame([dog, cat])
    