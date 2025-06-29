from core.Game import Game
from world.PlayerPath import PlayerPath
from tui.interface.CombatContext import CombatContext 
from combat.CombatManager import CombatManager

class GameController:
    def __init__(self, game):
        self.game = game
        self.world = game.world
        self.messages = []
        self.current_path = None
        self.context = None  # Sera défini au démarrage

    def set_context(self, context):
        """ Change le contexte actif """
        self.context = context

    def render_game_info(self):
        return (
            f"Jour {self.world.day} - {self.game.time_manager.get_time_of_day()} "
            f"({self.game.time_manager.get_hours_minutes()})\n"
            f"Météo : {self.world.weather.current}"
        )

    def render_zone(self):
        zone = self.game.current_area
        lines = [zone.name, "", zone.description, "", "Chemins disponibles :"]
        for i, (dest, path) in enumerate(zone.paths.items(), start=1):
            lines.append(f"{i}. {dest.name} ({path.steps} pas)")
        return "\n".join(lines)

    def render_messages(self):
        if not self.messages:
            return "Aucun message à afficher."
        return "\n".join(self.messages[-5:])

    def move_to(self, index):
        self.messages.append(f"Index: {index}")
        paths = list(self.game.current_area.paths.items())
        if 0 <= index < len(paths):
            dest, path = paths[index]
            self.current_path = PlayerPath(path)
            self.messages.append(f"Déplacement vers {dest.name} en cours...")
        else:
            self.messages.append(f"Chemin invalide.")

    def advance_step(self):
        if self.current_path:
            arrived = self.current_path.advance(self.game)
            triggered_events = self.current_path.get_triggered_events()
            for event in triggered_events:
                if event.message:
                    self.messages.append(event.message)
                
                result = event.execute(self.game.world, self.game.player)
                if (result):
                    self.handle_event_result(result)

            if arrived:
                self.messages.append(f"Arrivé à destination : {self.game.current_area.name}")
                self.current_path = None
            else:
                self.messages.append(f"Vous faites un pas... ({self.current_path.steps_done} / {self.current_path.path.steps})")
        else:
            self.messages.append("Aucun déplacement en cours.")
    
    def handle_event_result(self, result):
        if result["type"] == "fight":
            combat_manager = CombatManager(self.game.player, [result["enemy"]])
            self.set_context(CombatContext(self, combat_manager))
