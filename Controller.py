from Player import Player
# contains controller types with the game
# v1: will be terminal text based input

class Controller:

    def __init__(self):
        print("init")

    def makeDecision(self, query, options): # move to controller file
        x = True
        while x:
            try:
                decision = input(query + " ")
                if str.lower(str(decision)) == "exit": x = False; break
                elif str.lower(str(decision)) in options: break
                else: continue
            except: print("error")
        if x == False: exit()
        return decision
    
    # TODO: simplify
    def choosePrice(self, query): # move to controller file
        while True:
            price = input(query + " ")
            try:
                price = int(price)
                break
            except: print("error")
        return price

    def choosePlayerAction(self, player, rolled):
        query = player.token + "\'s turn: make (o)ffer, declare (b)ankruptcy"
        options = ["o", "b"]
        if player.properties: 
            query += ", sell (p)roperty"
            options.append("p")
            if player.canMortgageProperties():
                query += ", (m)ortgage"
                options.append("m")
            if player.canUnmortgageProperties():
                query += ", (u)nmortgage"
                options.append("u")
            if player.canBuyHouse():
                query += ", buy (h)ouse"
                options.append("h")
            if player.canSellHouse():
                query += ", (s)ell house"
                options.append("s")
        if rolled:
            query += ", (e)nd turn"
            options.append("e")
        else:
            query += ", (r)oll dice"
            options.append("r")
        return self.makeDecision(query, options)