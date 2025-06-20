from combat.CombatManager import CombatManager
from entities.Goblin import Goblin  # ou autre monstre

class MapFightEvent:
    def __init__(self, enemy):
        self.enemy = enemy

    def execute(self, world_state, player):
        print(f"[Événement] Un {self.enemy.getName()} surgit du chemin !")
        from entities.Player import Player  
        CombatManager.start(player, [self.enemy])
