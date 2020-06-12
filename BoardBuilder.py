import csv
from Property import Street, Station, Utility
from Action import NonProperty, Card

class BoardBuilder:

    def build(self, version):
        board = [NonProperty("GO!")] + [None]*39
        with open('boards/'+version+'x.csv') as propertyFile:
            # position, type, name, value, mortgage, rent, 1H, 2Hs, 3Hs, 4Hs, hotel, colour
            readCSV = csv.reader(propertyFile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                position = int(row[0])
                squareType = row[1]
                row[3:-1] = [0 if attribute == '' else int(attribute) for attribute in row[3:-1]]
                if squareType == "Street": board[position] = Street(*row[2:])
                elif squareType == "Station": board[position] = Station(*row[2:6])
                elif squareType == "Utility": board[position] = Utility(*row[2:5])
                elif squareType == "Card": board[position] = Card(row[2])
                else: board[position] = NonProperty(row[2])
        return board