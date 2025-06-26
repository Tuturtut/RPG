from combat.CombatManager import CombatManager
from events.Event import Event

class MapFightEvent(Event):
    def __init__(self, enemy):
        super().__init__("Combat imminent")
        self.enemy = enemy

    def execute(self, world_state, player):
        message = f"[Événement] Un {self.enemy.getName()} surgit du chemin !"
        CombatManager.start(player, [self.enemy])
        self.message = message
