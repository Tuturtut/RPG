from EventManager import EventManager
from Monster import Monster


class Goblin(Monster):
    def __init__(self, name="Goblin", health=100, damage=10, defense=5, can_summon=True):
        super().__init__(name, health, damage, defense)
        self.can_summon = can_summon
    
    def after_damage(self):
        if (not self.can_summon):
            return
        if self.health < 50 and self.is_alive():
            print("A Goblin appears!")
            EventManager.emit("summon", Goblin("Goblin", 40, 8, 0, False))
            