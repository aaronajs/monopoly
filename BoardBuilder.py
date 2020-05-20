import csv
from Property import Street, Station, Utility
from Action import NonProperty, Card

class BoardBuilder:

    def build(self, version):
        board = [None]*40
        with open('boards/'+version+'.csv') as propertyFile:
            # position, property(name), value, mortgage, rent, 1H, 2Hs, 3Hs, 4Hs, Hotel
            readCSV = csv.reader(propertyFile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                position = int(row[0])
                if position %5 ==0: board[position] = Station(*row[1:4], 25)
                elif position == 12 or position == 28: board[position] = Utility(*row[1:4], 0)
                else: board[position] = Street(*row[1:])
            board[0] = NonProperty("GO!")
            board[10] = NonProperty("Jail")
            board[20] = NonProperty("Free Parking")
            board[30] = NonProperty("Go To Jail!")
            board[4] = NonProperty("Income Tax")
            board[38] = NonProperty("Super Tax")
            for pos in [2, 17, 33]: board[pos] = Card("Community Chest")
            for pos in [7, 22, 36]: board[pos] = Card("Chance")
        return board