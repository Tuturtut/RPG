import curses
from tui.interface.BaseContext import BaseContext

class WalkingContext(BaseContext):
    def __init__(self, controller):
        super().__init__(controller)
        self.state = "move"

        self.input_manager.register(ord(" "), "move", "advance_step")

    def handle_input_contextual(self, action):
        if not action:
            self.controller.messages.append("Action non reconnue.")
            return

        if self.state == "move":
            self.handle_move(action)
    
    def handle_move(self, action):
        if action.get("move") == "advance_step":
            self.controller.game.tick()
            if not self.controller.game.player.current_path:
                from tui.interface.ExplorationContext import ExplorationContext
                self.controller.set_context(ExplorationContext(self.controller))

    def render_zone_content(self, zone_win):

        height, width = zone_win.getmaxyx()

        player = self.controller.game.player
        player_current_path = player.current_path

        steps_done = player_current_path.steps_done
        steps = player_current_path.path.steps

        progress_bar_width = width - 15
        y = 1

        # Afficher une barre de progression

        entities_on_path = self.controller.game.player.location.get_other_entities(player)

        bar_positions = {}

        player_pos = int(progress_bar_width * steps_done / steps)
        bar_positions[player_pos] = "|"

        for entity in entities_on_path:
            path_obj = entity.get_current_path()
            if path_obj and path_obj.path == self.controller.game.player.current_path.path:

                n = 0
                if path_obj.destination != player_current_path.destination:
                    n = (player_current_path.path.steps - path_obj.steps_done)
                else:
                    n = path_obj.steps_done

                pos = int(progress_bar_width * n / path_obj.path.steps)

                symbol = entity.getName()[0]  # Prend la première lettre du nom
                if pos not in bar_positions:
                    bar_positions[pos] = symbol
                else:
                    bar_positions[pos] = "*"  # Collision visuelle

        bar = ["_"] * progress_bar_width

        for pos, symbol in bar_positions.items():
            if 0 <= pos < progress_bar_width:
                bar[pos] = symbol

        bar_str = "[" + "".join(bar) + "]"

        progress = int((steps_done / steps) * 100)
        zone_win.addstr(y, 2, f"Progression : {progress}%")
        filled = int(progress_bar_width * steps_done / steps)
        empty = progress_bar_width - filled
        y += 1

        zone_win.addstr(y, 2, bar_str)

        y += 1

        # Affiche les infos sur le chemin en cours, si il y en a un
        if self.controller.game.player.current_path:
            zone_win.addstr(y, 2, "Chemin en cours :")
            y += 1
            zone_win.addstr(y, 4, self.controller.game.player.get_current_path().get_name())
            y += 1
        
        # Affiche les entités dans la zone