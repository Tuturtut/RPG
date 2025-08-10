from entities.Entity import Entity


class Human(Entity):
    def __init__(self, name="Human", health=100, damage=10, defense=5, actions=None):
        
        super().__init__(name, health, damage, defense, actions)
        self.languages = ["human"]
    