# represents a player of the game

class Player:

    board = []

    def __init__(self, token):
        self.token = token
        self.money = 1500 # starting amount
        self.titleDeeds = []
        self.getOutOfJailFreeCards = 0
        self.timeInJail = -1 # -1 is not in jail
        self.stationsOwned = 0
        self.utilitiesOwned = 0
        self.doublesRolled = 0 # to track 3 doubles in a row
        self.bankrupt = False
        self.position = 0

    def takeTurn(self, movePlayer):
        # opportunity to do other stuff
        movePlayer(self) # ready to roll dice and move
        # (add functionality to do other stuff afterwards too until end turn)

    def leaveJail(self, fine):
        self.doublesRolled = 0
        self.money -= fine
        self.timeInJail = -1

    def makeDecision(self, query, options):
        # while True:
        #     try:
        #         decision = input(query + " ")
        #         if str.lower(decision) in options: break
        #         else: continue
        #     except: print("error")
        # return decision
        return "continue"

    def __str__(self): 
        position = str(Player.board[self.position])
        if self.position == 10 and self.timeInJail == -1: position += " (visiting)"
        return self.token + " " + str(self.money) + " " + position