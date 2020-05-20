# represents nonProperty squares on board and chance + community chest cards
class NonProperty:

    def __init__(self, name):
        self.name = name

    def __str__(self): return self.name


class Card(NonProperty):

    def __init__(self, name):
        NonProperty.__init__(self, name)
        # actions based on name
        