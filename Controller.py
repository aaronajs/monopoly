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
        query, options = self.updateOptions(player.token + "\'s turn: make (o)ffer, declare (b)ankruptcy")
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

    def chooseJailAction(self, player): # TODO: TEST
        query, options = self.updateOptions(player.token + "'s choice: (w)ait for next turn")
        if player.canAfford(50): query, options = self.updateOptions(", (p)ay 50 to leave", query, options)
        if player.getOutOfJailFreeCards > 0: query, options = self.updateOptions(", use GO(j)F card", query, options)
        return self.makeDecision(query, options)
    
    def buyOrAuction(self, player, prop):
        # player can buy it, or get bank to auction property
        query, options = self.updateOptions(player.token + "'s choice: (a)uction")
        if player.canAfford(prop.value): query, options = self.updateOptions(", (b)uy property", query, options)
        return self.makeDecision(query, options)
    
    def chooseProperty(self, props, query, details):
        options = [str(index) for index in range(len(props))]
        for index in options:
            prop = props[int(index)]
            print(index + ": " + str(prop) + "," + str(getattr(prop, details))) #adjust on action
        decision = self.makeDecision(query, options)
        return props[int(decision)]
        
    def choosePropertyToMortgage(self, props): self.chooseProperty(props, "Which property to mortgage?", "mortgage")
    def choosePropertyToUnmortgage(self, props): self.chooseProperty(props, "Which property to unmortgage?", "mortgage*1.1")
    def choosePropertyToBuyHouse(self, props): self.chooseProperty(props, "Which property do you want to build a house on?", "houseCost")
    def choosePropertyToSellHouse(self, props): self.chooseProperty(props, "From which property do you want to sell a house?", "houseCost*0.5")
    #TODO: add custom methods with queries and details

    #TODO: select property, sell property, player needs money, offer