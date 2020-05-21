# represents all types of property, replaces need for Title Deed cards

class Property:

    def __init__(self, name, value, mortgage):
        self.name = name
        self.value = value
        self.mortgage = mortgage
        self.isMortgaged = False
        self.owner = None

    def __str__(self): 
        # return self.name + " " + str(self.value) + " " + str(self.mortgage)+ " " + str(self.rent) + " " + self.owner
        return self.name
    
class Street(Property):

    def __init__(self, name, value, mortgage, rent, one, two, three, four, hotel):
        Property.__init__(self, name, value, mortgage) # rent based on housing
        self.rent = [rent, one, two, three, four, hotel]
        self.numberOfHouses = 0 # 5 = hotel


# could combine into other, add type param?
class Utility(Property):

    def __init__(self, name, value, mortgage, rent):
        Property.__init__(self, name, value, mortgage)

class Station(Property):

    def __init__(self, name, value, mortgage, rent):
        Property.__init__(self, name, value, mortgage)
        self.rent = rent