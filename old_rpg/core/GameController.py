from tui.interface.CombatContext import CombatContext 
from combat.CombatManager import CombatManager
from tui.interface.ExplorationContext import ExplorationContext

class GameController:
    def __init__(self, game):
        self.game = game
        self.world = game.world
        self.messages = []
        self.context = None  # Sera défini au démarrage
        self.exploration_context = ExplorationContext(self)

    def set_context(self, context):
        """ Change le contexte actif """
        self.context = context

    def render_game_info(self):
        return (
            f"Jour {self.world.day} - {self.game.time_manager.get_time_of_day()} "
            f"({self.game.time_manager.get_hours_minutes()})\n"
            f"Météo : {self.world.weather.current}\n"
            f"Zone : {self.game.current_area.name}"
        )

    def render_zone(self):
        zone = self.game.current_area
        lines = [zone.name, "", zone.description, "", "Chemins disponibles :"]
        for i, (dest, path) in enumerate(zone.paths.items(), start=1):
            lines.append(f"{i}. {dest.name} ({path.steps} pas)")
        
        lines.append("\n")
        
        if zone.entities and zone.entities != [self.game.player]:
            lines.append("Personnes présentes :")
            for entity in zone.entities:
                if entity != self.game.player:
                    lines.append(f" - {entity.describe()}")
        else:
            lines.append("Il n'y a personne ici.")

        return "\n".join(lines)

    def render_messages(self):
        if not self.messages:
            return "Aucun message à afficher."
        return "\n".join(self.messages[-5:])

    def move_to(self, index):
        paths = list(self.game.current_area.paths.items())
        if 0 <= index < len(paths):
            dest, path = paths[index]
            self.game.player.start_path(path, dest)
            self.messages.append(f"Déplacement vers {dest.name} en cours...")
        else:
            self.messages.append(f"Chemin invalide.")
    
    def get_possible_moves(self):
        return list(self.game.current_area.paths.keys())
        
    def handle_event_result(self, result):
        type_ = result.get("type")
        message = result.get("message")

        if type_ == "info":
            self.display_message(message)

        elif type_ == "dialogue":
            self.display_dialogue(message)

        elif type_ == "fight":
            self.start_fight(result["triggers"] ,result["enemies"], message)

        else:
            self.display_message(f"(Événement inconnu) {message}")

    def display_message(self, message):
        self.messages.append(message)

    def display_dialogue(self, message):
        self.messages.append(f"Dialogue : {message}")

    def start_fight(self, triggers, enemies, message):
        self.set_context(CombatContext(self, CombatManager(self.game.player, enemies), self.context))
