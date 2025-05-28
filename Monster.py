from Entity import Entity

# extends Entity
class Monster(Entity):
    
    def __init__(self, name, health, damage, defense, actions):
        super().__init__(name, health, damage, defense, actions)
         