from entities.Human import Human

class Player(Human):
    def __init__(self, name, health, damage, defense, actions=None):
        super().__init__(name, health, damage, defense, actions)
