from world.PlayerPath import PlayerPath

class GameController:
    def __init__(self, game):
        self.game = game
        self.world = game.world
        self.messages = [] 
        self.current_path = None

    def render_zone(self):
        zone = self.game.current_area
        lines = [zone.name, "", zone.description, "", "Chemins disponibles :"]
        for i, (dest, path) in enumerate(zone.paths.items(), start=1):
            lines.append(f"{i}. {dest.name} ({path.steps} pas)")
        return "\n".join(lines)

    def render_game_info(self):
        return f"Jour {self.world.day} - {self.game.time_manager.get_time_of_day()} ({self.game.time_manager.get_hours_minutes()})\n" \
               f"Météo : {self.world.weather.current}\n" \

    def render_messages(self):
        if len(self.messages) > 10:
            self.messages.pop(0)
        
        # Retourne les 3 derniers messages ou un message par défaut
        if not self.messages:
            return "Aucun message à afficher."
        return "\n".join(self.messages[-3:])

    def get_available_paths(self):
        return list(self.game.current_area.paths.items())

    def move_to(self, index):
        paths = self.get_available_paths()
        if 0 <= index < len(paths):
            destination, path = paths[index]
            self.current_path = PlayerPath(path)
            self.messages.append(f"Déplacement vers {destination.name} en cours...")
        else:
            self.messages.append("Chemin invalide.")
    


    def advance_step(self):
        if self.current_path:
            arrived = self.current_path.advance(self.game)
            triggered_events = self.current_path.get_triggered_events()  # méthode à ajouter
            for event in triggered_events:
                if event.message:
                    self.messages.append(event.message)
            if arrived:
                self.messages.append(f"Arrivé à destination : {self.game.current_area.name}")
                self.current_path = None
            else:
                self.messages.append(f"Vous faites un pas... ({self.current_path.steps_done} / {self.current_path.path.steps})")

        else:
            self.messages.append("Aucun déplacement en cours.")
