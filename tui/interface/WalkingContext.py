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
            self.controller.advance_step()
            if not self.controller.game.player.current_path:
                from tui.interface.ExplorationContext import ExplorationContext
                self.controller.set_context(ExplorationContext(self.controller))

    def render_zone_content(self, zone_win):

        height, width = zone_win.getmaxyx()
        steps_done = self.controller.game.player.current_path.steps_done
        steps = self.controller.game.player.current_path.path.steps

        from utils.debug import log
        log(f"Width: {width}, Height: {height}")

        progress_bar_width = width - 15

        y = 1
        # Afficher une barre de progression
        progress = int((steps_done / steps) * 100)
        zone_win.addstr(y, 2, f"Progression : {progress}%")
        filled = int(progress_bar_width * steps_done / steps)
        empty = progress_bar_width - filled
        y += 1

        zone_win.addstr(y, 2, f"[{'█'*filled}{'░'*empty}] {steps_done}/{steps}")

        y += 1

        # Affiche les infos sur le chemin en cours, si il y en a un
        if self.controller.game.player.current_path:
            zone_win.addstr(y, 2, "Chemin en cours :")
            y += 1
            zone_win.addstr(y, 4, self.controller.game.player.get_current_path().get_name())
            y += 1
        
        # Affiche les entités dans la zone