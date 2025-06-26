from world.WorldState import WorldState
from dialogue.DialogueManager import DialogueManager
from core.GameContext import GameContext
from core.TimeManager import TimeManager
from entities.Player import Player
from actions.AttackAction import AttackAction
from world.Area import Area
from world.Path import Path
from events.MapDialogueEvent import MapDialogueEvent

class Game:
    def __init__(self):
        self.world = WorldState()
        self.dialogue_manager = DialogueManager()  # gestionnaire de dialogues
        self.journal = GameContext.journal  # référence partagée
        self.areas = {}
        self.current_area = None
        self.time_manager = TimeManager()

    def set_player(self, player, starting_area):
        self.player = player
        starting_area.add_entity(player)
        self.current_area = starting_area

    def setup(self):
        # Création des zones
        village = Area("Village", "Un petit village calme.")
        forest = Area("Forêt", "Une forêt dense et mystérieuse.")
        mountain = Area("Montagne", "Une montagne enneigée.")

        # Création des chemins
        path1 = Path(village, forest, 50)
        path2 = Path(forest, mountain, 3)

        path2.add_event(1, MapDialogueEvent("Un voyageur vous aborde pour discuter."))

        # Ajout du joueur
        player = Player("Héros", damage=10, health=100, defense=5, actions=[AttackAction("Attaque", description="Attaque de base")])
        self.set_player(player, village)

        self.add_area(village)
        self.add_area(forest)

        self.current_area = village    

    def add_area(self, area):
        self.areas[area.name] = area
        if self.current_area is None:
            self.current_area = area  # première zone définie

    def change_area(self, name):
        if name in self.areas:
            self.current_area = self.areas[name]
            print(f"\n[Déplacement] Vous entrez dans {name}.")
            self.journal.add(self.world.day, f"Entrée dans {name}.")
        else:
            print(f"[Erreur] Zone inconnue : {name}")

    def wait(self, minutes):
        day_changed = self.time_manager.advance_minutes(minutes)
        self.journal.add(self.world.day, f"Vous avez attendu {minutes} minutes.")

        if day_changed:
            self.world.advance_day()
            self.journal.add(self.world.day, f"Un nouveau jour commence. Météo : {self.world.weather.current}.")
