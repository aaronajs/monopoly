# represents all types of property, replaces need for Title Deed cards

class Property:

    def __init__(self, name, value, mortgage, rent):
        self.name = name
        self.value = value
        self.mortgage = mortgage
        self.rent = rent
        self.owner = "Bank"

    def __str__(self): 
        # return self.name + " " + str(self.value) + " " + str(self.mortgage)+ " " + str(self.rent) + " " + self.owner
        return self.name
    
class Street(Property):

    def __init__(self, name, value, mortgage, rent, one, two, three, four, hotel):
        Property.__init__(self, name, value, mortgage, rent)
        self.oneHouse = one
        self.twoHouses = two
        self.threeHouses = three
        self.fourHouses = four
        self.hotel = hotel


# could combine into other, add type param?
class Utility(Property):

    def __init__(self, name, value, mortgage, rent):
        Property.__init__(self, name, value, mortgage, rent)

class Station(Property):

    def __init__(self, name, value, mortgage, rent):
        Property.__init__(self, name, value, mortgage, rent)