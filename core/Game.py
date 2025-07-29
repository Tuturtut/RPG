from world.WorldState import WorldState
from dialogue.DialogueManager import DialogueManager
from core.GameContext import GameContext
from core.TimeManager import TimeManager
from entities.Player import Player
from actions.AttackAction import AttackAction
from world.Area import Area
from world.Path import Path
from events.MapDialogueEvent import MapDialogueEvent
from events.MapFightEvent import MapFightEvent
from entities.Monster import Monster
from entities.Human import Human

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
        lake = Area("Lac", "Un lac tranquille.")
        cave = Area("Caverne", "Une caverne sombre.")
        hill = Area("Colline", "Une colline rocheuse.")
        swamp = Area("Marais", "Un marais sombre.")

        goblin_des_montagnes = Monster("Gobelin des Montagnes", 10, 5, 2, actions=[AttackAction("Morsure", description="Attaque de base")])
        mountain.add_entity(goblin_des_montagnes)

        # Création des chemins
        path1 = Path(village, forest, 10)
        path2 = Path(forest, mountain, 8)
        path3 = Path(mountain, lake, 6)
        path4 = Path(lake, village, 5)
        path5 = Path(mountain, cave, 4)
        path7 = Path(lake, hill, 12)
        path6 = Path(cave, lake, 100)
        path7 = Path(hill, swamp, 10)

        maruen = Human(name="Maruen", health=100, damage=10, defense=5)
        village.add_entity(maruen)
        # Load dialogues
        self.dialogue_manager.load_dialogues(maruen)

        path1.add_event(0, MapDialogueEvent("Un voyageur vous aborde pour discuter."))

        path7.add_event(6, MapDialogueEvent("Un renard vous aborde."))

        path2.add_event(4, MapDialogueEvent("Un voyageur vous aborde pour discuter."))
        # path6.add_random_event(MapDialogueEvent("Vous entendez le loup, le renard, et la belette."))


        wolves =  [Monster("Loup", 13, 20, 1, [AttackAction("Morsure", description="Croc Croc")])
                   for _ in range(4)]

        path3.add_event(2, MapFightEvent(wolves))


        attack1 = AttackAction("Attaque", description="Attaque de base")
        attack2 = AttackAction("Attaque lourde", description="Attaque de base", rounds=1, additional_damage=5)


        # Ajout du joueur
        player = Player("Héros", damage=30, health=100, defense=5, actions=[attack1, attack2])
        self.set_player(player, village)

        self.add_area(village)
        self.add_area(forest)
        self.add_area(mountain)
        self.add_area(lake)
        self.add_area(cave)
        self.add_area(hill)

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
