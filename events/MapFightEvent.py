from combat.CombatManager import CombatManager
from events.Event import Event
from entities.Player import Player

class MapFightEvent(Event):
    def __init__(self, enemies):
        super().__init__("fight")
        self.enemies = enemies

    def execute(self, entities, controller):
        from utils.debug import log
        log("MapFightEvent")

        for entity in entities:

            if not isinstance(entity, Player):
                return None
            
        living_enemies = [e for e in self.enemies if e.is_alive()]
        if not living_enemies:
            return {"type": "info", "message": "Aucun ennemi vivant."}
        return {
            "type": "fight",
            "triggers": entities,
            "enemies": living_enemies,
            "message": f"{len(living_enemies)} ennemi(s) surgissent du chemin !"
        }
