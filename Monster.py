from Entity import Entity

# extends Entity
class Monster(Entity):
    
    def __init__(self, name, health, damage, defense):
        super().__init__(name, health, damage, defense)
         