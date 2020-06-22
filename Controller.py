from Player import Player
import re
# contains controller types with the game
# v1: will be terminal text based input

class Controller:

    def __init__(self):
        print("init")

    def updateOptions(self, update, query, options):  
        query += update
        for option in re.findall(r'\((.*?)\)',update): options.append(option)
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
        query, options = self.updateOptions(player.token + "\'s turn: make (o)ffer, declare (b)ankruptcy", "", [])
        if player.properties: 
            query, options = self.updateOptions(", sell (p)roperty", query, options)
            if player.canMortgageProperties(): query, options = self.updateOptions(", (m)ortgage", query, options)
            if player.canUnmortgageProperties(): query, options = self.updateOptions(", (u)nmortgage", query, options)
            if player.canBuyHouse(): query, options = self.updateOptions(", buy (h)ouse", query, options)
            if player.canSellHouse(): query, options = self.updateOptions(", (s)ell house", query, options)
        if rolled: query, options = self.updateOptions(", (e)nd turn", query, options)
        else: query, options = self.updateOptions(", (r)oll dice", query, options)
        print(options)
        return self.makeDecision(query, options)

    def chooseJailAction(self, player): # TODO: TEST
        query, options = self.updateOptions(player.token + "'s choice: (w)ait for next turn", "", [])
        if player.canAfford(50): query, options = self.updateOptions(", (p)ay 50 to leave", query, options)
        if player.getOutOfJailFreeCards > 0: query, options = self.updateOptions(", use GO(j)F card", query, options)
        return self.makeDecision(query, options)
    
    def buyOrAuction(self, player, prop): # TODO: let player have option to raise money, and change mind.
        # player can buy it, or get bank to auction property
        query, options = self.updateOptions(player.token + "'s choice: (a)uction", "", [])
        if player.canAfford(prop.value): query, options = self.updateOptions(", (b)uy property", query, options)
        return self.makeDecision(query, options)

    def chooseProperty(self, props, version):
        if version == "mortgage": query = "Which property do you want to mortgage?"
        elif version == "unmortgage": query = "Which property do you want to unmortgage?"
        elif version == "buyHouse": query = "Which property do you want to build a house on?"
        elif version == "sellHouse": query = "From which property do you want to sell a house?"
        elif version == "sellProp": query = "Which property do you want to sell?"
        options = [str(index) for index in range(len(props))]
        for index in options:
            prop = props[int(index)]
            print(index + ": " + str(prop))
        decision = self.makeDecision(query, options)
        return props[int(decision)]

    def chooseMultipleProperties(self, props):
        query, options = self.updateOptions("Which properties to offer? (a)ll, (n)one; (d)one choosing", "", [])
        options += [str(index) for index in range(len(props))]
        for index in options:
            prop = props[int(index)]
            print(index + ": " + str(prop))
        chosenProperties = []
        while True:
            selection = self.makeDecision(query, options)
            if selection == "a": chosenProperties = props; break
            elif selection == "n": chosenProperties = None; break
            elif selection == "d": break
            else:
                chosenProperties.append(props[int(index)])
                props.remove(index) #TODO: test
        return chosenProperties

    def offerDecision(self, player):
        query, options = self.updateOptions(player.token + ": what is your decision? (a)ccept or (r)eject", "", [])
        return self.makeDecision(query, options)

    def choosePlayer(self, others):
        options = [str(index) for index in range(len(others))]
        for index in options:
            other = others[int(index)]
            print(index + ": " + str(other))
        decision = self.makeDecision("Which player?", options)
        return others[int(decision)]

    def chooseFinancing(self, player):
        query, options = self.updateOptions(player.token + "\'s turn: declare (b)ankruptcy", "", [])
        if player.properties: 
            query, options = self.updateOptions(", sell (p)roperty", query, options) # careful with selling properties with houses
            if player.canMortgageProperties(): query, options = self.updateOptions(", (m)ortgage", query, options)
            if player.canSellHouse(): query, options = self.updateOptions(", (s)ell house", query, options)
        return self.makeDecision(query, options)

    #TODO: offer