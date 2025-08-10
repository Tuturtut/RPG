from actions.Action import Action
from EventManager import EventManager
from entities.Monster import Monster
from actions.AttackAction import AttackAction
from entities.Entity import Entity

class Goblin(Monster):
    def __init__(self, name="Goblin", health=100, damage=10, defense=5, can_summon=True):
        
        super().__init__(name, health, damage, defense, [AttackAction("Attack", rounds=0, description="Attack the player", valid_target_types=[Entity])])
        self.can_summon = can_summon
    
    def after_taking_damage(self):
        if self.is_injured() and self.can_summon:
            pass