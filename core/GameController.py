from core.Game import Game
from world.PlayerPath import PlayerPath

class GameController:
    def __init__(self, game):
        self.game = game
        self.world = game.world
        self.messages = []
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
        self.messages.append(f"Index: {index}")
        paths = list(self.game.current_area.paths.items())
        if 0 <= index < len(paths):
            dest, path = paths[index]
            self.game.player.start_path(path)
            self.messages.append(f"Déplacement vers {dest.name} en cours...")
        else:
            self.messages.append(f"Chemin invalide.")

    def advance_step(self):
        player = self.game.player
        if player.current_path:
            arrived, triggered_events = player.advance_path(self.game)
            for event in triggered_events:
                if event.message:
                    self.messages.append(event.message)

            if arrived:
                self.messages.append(f"Arrivé à destination : {self.game.current_area.name}")
                self.current_path = None
            else:
                self.messages.append(f"Vous faites un pas... ({player.current_path.steps_done} / {player.current_path.path.steps})")

            self.game.tick()

        else:
            self.messages.append("Aucun déplacement en cours.")