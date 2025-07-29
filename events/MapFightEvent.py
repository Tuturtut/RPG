from combat.CombatManager import CombatManager
from events.Event import Event

class MapFightEvent(Event):
    def __init__(self, enemies):
        super().__init__("Combat imminent")
        self.enemies = enemies

    def execute(self, world_state, player):
        living_enemies = [enemy for enemy in self.enemies if enemy.is_alive()]

        if not living_enemies:
            self.message = "[Événement] Aucun ennemi vivant."
            return None

        if (len(self.enemies) == 0):
            return
        elif (len(self.enemies) == 1):
            self.message = f"[Événement] Un {self.enemies[0].getName()} surgit du chemin !"
        else:
            self.message = f"[Événement] {len(self.enemies)} ennemis surgissent du chemin !"
        return {"type": "fight", "enemies": self.enemies}
