from world.WorldState import WorldState
from world.DialogueManager import DialogueManager
from core.GameContext import GameContext
from core.TimeManager import TimeManager
from entities.Player import Player
from actions.Action import Action

class Game:
    def __init__(self):
        self.world = WorldState()
        self.dialogue_manager = DialogueManager()  # gestionnaire de dialogues
        self.journal = GameContext.journal  # référence partagée
        self.areas = {}
        self.current_area = None
        self.time_manager = TimeManager()


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
