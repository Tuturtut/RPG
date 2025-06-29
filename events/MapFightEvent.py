from combat.CombatManager import CombatManager
from events.Event import Event

class MapFightEvent(Event):
    def __init__(self, enemy):
        super().__init__("Combat imminent")
        self.enemy = enemy

    def execute(self, world_state, player):
        self.message = f"[Événement] Un {self.enemy.getName()} surgit du chemin !"
        return {"type": "fight", "enemy": self.enemy}
