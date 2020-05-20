import random
from Player import Player
from Property import Street, Station, Utility 
from BoardBuilder import BoardBuilder
# controls the game, acts as the bank

class Game:

    def __init__(self, board):
        self.players = [] # list of all players and their position
        self.board = board # represents the board, 40 squares
        self.turn = 0 # index of self.players
        self.activePlayers = 0

    def rollDice(self): return [random.randint(1,6),random.randint(1,6)]

    def movePlayer(self, player): # finishing moving protocols
        dice = self.rollDice()
        moveSpaces = sum(dice)
        if dice[0] == dice[1]: player.doublesRolled+=1
        if player.timeInJail == -1: # player not in jail
            if player.doublesRolled == 3: # got to jail for 3 doubles in a row
                player.timeInJail = 0
                player.position = 10
                player.doublesRolled = 0
            else: self.newPlayerPosition(player, moveSpaces)
        else: self.tryToLeaveJail(player, moveSpaces)
        print(player)
    
    def tryToLeaveJail(self, player, moveSpaces):
        if player.doublesRolled == 1: self.playerLeavesJail(player, moveSpaces)
        else: 
            player.timeInJail += 1
            if player.timeInJail == 3: self.playerLeavesJail(player, moveSpaces, 50)
            else: # in jail for less than 3 turns; give options based on GOJF card
                if player.getOutOfJailFreeCards > 0:
                    query = "\n\'pay\' 50 or use GOJF \'card\', or \'continue\' later"
                    options = ["continue", "pay", "card"]
                else:
                    query = "\n\'pay\' 50 or \'continue\' later"
                    options = ["continue", "pay"]
                decision = player.makeDecision(query, options)
                if decision == "pay": self.playerLeavesJail(player, moveSpaces, 50)
                elif decision == "card": self.playerLeavesJail(player, moveSpaces)

    def playerLeavesJail(self, player, moveSpaces, fine=0):
        player.leaveJail(fine)
        self.newPlayerPosition(player, moveSpaces)

    # controls the outcome of where the player lands
    def newPlayerPosition(self, player, moveSpaces):
        newPosition = player.position + moveSpaces
        # jail, passing go
        if newPosition == 30: # player lands on go to jail, goes to jail, doesn't pass go/collects 200
            player.timeInJail = 0
            newPosition = 10
        elif newPosition >=40: # player passes go
            newPosition -= 40
            player.money += 200

        player.position = newPosition # moves the player

        # taxes
        if newPosition == 4: player.money -= 200 # player pays income tax
        elif newPosition == 38: player.money -= 100 # player pays super tax

        # rent (utilities, stations, properties)
        #stations
        prop = board[newPosition]
        if prop.owner == "Bank": # property is unowned: 
            print("unowned")
        if isinstance(prop, Station): print('')
            


    def printBoard(self):
        rows = [list(range(11))] # go -> jail
        for i in range(9): # 9 rows of 11: (39 ... 11, 38 ... 12)
            rows.append([40-i, "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", i+10])
        rows.append(list(range(30,19,-1))) # goToJail -> Free parking
        for row in rows: print(row)

    def playGame(self, player): # runs the game
        test = 0
        while self.activePlayers > 1 and test <= 100:
            self.turn = self.turn + 1 if self.turn < self.activePlayers - 1 else 0
            test += 1
            self.players[self.turn].takeTurn(self.movePlayer)

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
    game.startGame([dog, cat])
    # game.printBoard()