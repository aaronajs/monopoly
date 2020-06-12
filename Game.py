import random
from Player import Player
from Action import Card
from Property import Property, Street, Station, Utility 
from BoardBuilder import BoardBuilder
# controls the game, acts as the bank

class Game:

    def __init__(self, board):
        self.players = [] # list of all players and their position
        self.board = board # represents the board, 40 squares
        self.turn = 0 # index of self.players
        self.activePlayers = 0
        self.doubleRolled = False

    def rollDice(self): return [random.randint(1,6),random.randint(1,6)]

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
        # self.printBoard()
        # print()

    def sendPlayerToJail(self, player):
        player.timeInJail = 0
        player.position = 10
        player.doublesRolled = 0
    
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
                    query = "\'p\'ay 50 or use GO\'J\'F card, or \'c\'ontinue later?"
                    options = ["c", "p", "j"]
                else:
                    query = "\'p\'ay 50 or \'c\'ontinue later?"
                    options = ["c", "p"]
                decision = player.makeDecision(query, options)
                if decision == "p": 
                    while player in self.players and not player.canAfford(50): 
                        self.playerNeedsMoney(player)
                    if player in self.players: self.playerLeavesJail(player, moveSpaces, 50)
                elif decision == "j": self.playerLeavesJail(player, moveSpaces)

    def playerLeavesJail(self, player, moveSpaces, fine=0):
        player.leaveJail(fine)
        self.newPlayerPosition(player, moveSpaces)
        print(player.token + " leaves jail")

    def playerNeedsMoney(self, player, owner=None):
        print(player.token + " has " + str(player.money))
        if not player.properties: self.playerGoesBankrupt(player, owner)
        else: 
            query = player.token + ": declare \'b\'ankruptcy, sell a \'p\'roperty"
            options = ["p", "b"]
            propsWithHouses = player.getPropertiesWithHouses() # unmortgaged, have houses/hotel
            if propsWithHouses: 
                options.append("h")
                query += ", sell a \'h\'ouse"
            unmortgaged = player.getUnmortgagedProperties() # can be mortgaged, have no houses
            if unmortgaged: 
                options.append("m")
                query += ", \'m\'ortgage"
            decision = player.makeDecision(query, options)
            if decision == "p": self.playerSellsProperty(player)
            elif decision == "b": self.playerGoesBankrupt(player, owner)
            elif decision == "m": self.playerMortgagesProperty(player, unmortgaged)
            # elif decision == "h": self.playerSellsHouses(player, propsWithHouses)

    def playerGoesBankrupt(self, player, owner):
        player.isBankrupt(owner) #TODO what to do when owner is bank
        if player in self.players: self.players.remove(player)
        self.activePlayers -= 1
        # TODO: check if destroy player object?
        print(player.token + " is bankrupt!")

    def playerMortgagesProperty(self, player, props):
        options = [str(index) for index in range(len(props))]
        for index in options: print(str(index) + ": " + str(props[int(index)]))
        query = "Which property to sell? (enter number)"
        decision = int(player.makeDecision(query, options))
        player.mortgageProperty(player.properties[decision])

    def playerSellsProperty(self, player):
        options = [str(index) for index in range(len(player.properties))]
        for index in options: 
            print(index + ": " + str(player.properties[int(index)]))
        query = "Which property to sell? (enter number)"
        decision = player.makeDecision(query, options)
        prop = player.properties[int(decision)]
        # TODO: add option to sell buildings straight away
        if isinstance(prop, Street) and prop.numberOfHouses != 0: print("sell houses first") 
        else: # sell property to another player
            buyers = [buyer for buyer in self.players if buyer != player]
            options = [str(index) for index in range(len(buyers))]
            for index in options: print(str(index) + ": " + str(buyers[int(index)]))
            # options = [buyer.token for buyer in self.players if buyer != player]
            query = "Sell property to another player: (enter number)" # + str(options)
            # BUG: why does it need ''? ----- only works with Python 3
            decision = buyers[int(player.makeDecision(query, options))]
            # TODO: players must agree on a price before the transaction goes through
            # for now leave as agree outside game
            # ensure that it's within range of BOTH players of the game
            price = int(player.choosePrice("what price to sell to " + str(decision))) # BUG: infinite loop?
            player.sellProperty(prop, decision, price) 

    # controls the outcome of where the player lands
    def newPlayerPosition(self, player, moveSpaces):
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
                    query = player.token + ": \'b\'uy or \'a\'uction " + prop.name + "?"
                    options = ["b", "a"]
                    decision = player.makeDecision(query, options)
                    if decision == "b": 
                        while player in self.players and not player.canAfford(prop.value):
                            print(player.token + " can't afford " + prop.name + "; it costs " + str(prop.value))
                            self.playerNeedsMoney(player)
                        if player in self.players:
                            player.buyProperty(prop)
                            # check if colour set
                            if isinstance(prop, Street):
                                colourSet = Street.colourSets[prop.colour]
                                if all(street.owner == player for street in colourSet):
                                    for street in colourSet: street.colourSetOwned = True
                                    print(player.token + " owns the colour set " + prop.colour)

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
                        
    def printBoard(self):
        rows = [list(range(11))] # go -> jail
        for i in range(9): # 9 rows of 11: (39 ... 11, 38 ... 12)
            rows.append([39-i, "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", i+11])
        rows.append(list(range(30,19,-1))) # goToJail -> Free parking
        for row in rows: 
            # print(row)
            for section in row: 
                # for player in self.players:
                    # multiple players on same square
                # if player.position == section: print(str.capitalize(player.token[0]), end=' ')
                if str(self.players[0].position) == str(section): print("D", end = ' ')
                elif str(self.players[1].position) == str(section): print("C", end = ' ')
                else: print(section, end=' ')
            print()

    def playGame(self, player): # runs the game
        test = 0
        while self.activePlayers > 1 and test <= 500:
            if not self.doubleRolled: self.turn = self.turn + 1 if self.turn < self.activePlayers - 1 else 0
            test += 1
            self.players[self.turn].takeTurn(self.movePlayer)
        print("DONE")

    def startGame(self, players): # chooses player to go first
        self.players = players # all start at go
        self.activePlayers = len(players)
        highestRoll = 0
        first = self.players[0]
        for player in self.players: 
            if sum(self.rollDice()) > highestRoll: first = player
        self.turn = self.players.index(first) # which player goes first
        self.playGame(first)
    
if __name__ == "__main__":
    board = BoardBuilder().build("default")
    game = Game(board)
    Player.board = board
    dog = Player("dog")
    cat = Player("cat")
    # print(Street.colourSets["Light Blue"])
    game.startGame([dog, cat])
    # game.printBoard()
    