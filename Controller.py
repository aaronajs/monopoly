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
                if str.lower(str(decision)) in options: break
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