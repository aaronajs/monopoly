from Player import Player
# contains controller types with the game
# v1: will be terminal text based input

class Controller:

    def __init__(self):
        print("init")

    def updateOptions(self, update, query="", options=[]):  
        query += update
        options.append(update[update.find("(")+1])
        return query, options

    def makeDecision(self, query, options):
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
    def choosePrice(self, query):
        while True:
            price = input(query + " ")
            try:
                price = int(price)
                break
            except: print("error")
        return price

    def choosePlayerAction(self, player, rolled):
        query, options = self.updateOptions("\'s turn: make (o)ffer, declare (b)ankruptcy")
        query = player.token + "\'s turn: make (o)ffer, declare (b)ankruptcy"
        options = ["o", "b"]
        if player.properties: 
            query, options = self.updateOptions(", sell (p)roperty", query, options)
            if player.canMortgageProperties(): query, options = self.updateOptions(", (m)ortgage", query, options)
            if player.canUnmortgageProperties(): query, options = self.updateOptions(", (u)nmortgage", query, options)
            if player.canBuyHouse(): query, options = self.updateOptions(", buy (h)ouse", query, options)
            if player.canSellHouse(): query, options = self.updateOptions(", (s)ell house", query, options)
        if rolled: query, options = self.updateOptions(", (e)nd turn", query, options)
        else: query, options = self.updateOptions(", (r)oll dice", query, options)
        return self.makeDecision(query, options)

    def chooseJailAction(self, player):
        if player.doublesRolled == 1: return "l"
        else: 
            player.timeInJail += 1
            if player.timeInJail == 3: return "p"
            else: 
                query, options = self.updateOptions("(w)ait for next turn")
                if player.canAfford(50): query, options = self.updateOptions(", (p)ay 50 to leave", query, options)
                if player.getOutOfJailFreeCards > 0: query, options = self.updateOptions(", use GO(j)F card", query, options)
        return self.makeDecision(query, options)

    #TODO: get out of jail, buy property, select property, player needs money, offer