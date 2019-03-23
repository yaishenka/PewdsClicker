import json
class Bonus:
    def __init__(self, points, cost, auto, bought, required_level):
        self.points = points
        self.cost = cost
        self.auto = auto
        self.bought = bought
        self.required_level = required_level

class JSonBonus(Bonus):
    pass

