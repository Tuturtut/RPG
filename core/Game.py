from world.WorldState import WorldState
from dialogue.DialogueManager import DialogueManager
from core.GameContext import GameContext
from core.TimeManager import TimeManager
from entities.Player import Player
from actions.AttackAction import AttackAction
from world.locations.Area import Area
from world.locations.Path import Path
from world.locations.EntityPath import EntityPath
from events.MapDialogueEvent import MapDialogueEvent
from events.MapFightEvent import MapFightEvent
from entities.Monster import Monster
from entities.Human import Human


class Game:
    def __init__(self):
        self.world = WorldState()
        self.dialogue_manager = DialogueManager()  # gestionnaire de dialogues
        self.journal = GameContext.journal  # référence partagée
        self.locations = {}  # dict : nom → instance de location
        self.current_area = None
        self.time_manager = TimeManager()

    def set_player(self, player, starting_area):
        self.player = player
        starting_area.add_entity(player)
        self.current_area = starting_area

    def setup(self):
        # 🏘️ Lieux
        village = Area("Lierrebourg", "Un village fortifié, cœur du royaume.")
        forêt = Area("Bois des Murmures", "Forêt dense et humide, réputée pour ses bruits étranges.")
        ferme = Area("Vieille Ferme", "Ferme abandonnée envahie par la végétation.")
        ruines = Area("Ruines du Nord", "Pierres oubliées d’un ancien fort.")
        route = Area("Route Royale", "Route pavée menant vers d’anciens royaumes.")

        # 🛣️ Chemins
        path1 = Path(village, forêt, steps=6)
        path2 = Path(village, ferme, steps=4)
        path3 = Path(forêt, ruines, steps=5)
        path4 = Path(ferme, ruines, steps=6)
        path5 = Path(village, route, steps=8)

        # 🌳 Événements
        path1.add_event_at(2, MapDialogueEvent("Un vieux bûcheron vous avertit des esprits de la forêt."))
        path2.add_event(MapFightEvent([
            Monster("Chien errant", 8, 3, 1, [AttackAction("Grognement", description="Un aboiement rauque vous surprend.")])
        ]))

        path3.add_event_at(4, MapDialogueEvent("Vous trouvez un pendentif ancien couvert de mousse."))
        path5.add_event_at(5, MapFightEvent([
            Monster("Bandit de grand chemin", 18, 6, 2, [AttackAction("Coup de masse", description="Le bandit vous attaque sans prévenir.")])
        ]))

        path1.add_event(MapDialogueEvent("Un vieux bûcheron vous avertit des esprits de la forêt."))

        # 🧍 Joueur
        base_attack = AttackAction("Coup d'épée", description="Une attaque de base.")
        player = Player("Écuyer", damage=22, health=90, defense=5, actions=[base_attack])
        self.set_player(player, village)

        # 👤 PNJ en route
        garde = Human("Garde royal", health=60, damage=10, defense=3, actions=[base_attack])
        village.add_entity(garde)
        garde.current_path = EntityPath(garde, path5, origin=path5.start)

        # 🗺️ Ajout au monde
        for area in [village, forêt, ferme, ruines, route]:
            self.add_area(area)
        for path in [path1, path2, path3, path4, path5]:
            self.add_path(path)


    def add_area(self, area):
        self.locations[area.name] = area
        if self.current_area is None:
            self.current_area = area  # première zone définie
        
    def add_path(self, path):
        self.locations[path.get_name()] = path
    
    def add_message(self, message):
        GameContext.get_game_controller(self).messages.append(message)
    
    def tick(self):

        # 1. Avance le temps
        if self.time_manager.advance_minutes(10):
            self.world.day = self.time_manager.get_day()

        # 2. Faire évoluer la météo
        self.world.weather.update(self.time_manager)

        # 3. Faire avancer les entités et verifier les événements
        for location in self.locations.values():
            for entity in location.get_entities():

                if entity.current_path:
                    entity.advance_path(self, GameContext.get_game_controller(self))
