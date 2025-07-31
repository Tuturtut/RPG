import curses
from utils.InputManager import InputManager
from tui.interface.BaseContext import BaseContext
from tui.interface.WalkingContext import WalkingContext
from utils.helpers.SelectionHelper import SelectionHelper
from utils.ui import draw_selection_list

class ExplorationContext(BaseContext):
    def __init__(self, controller):
        super().__init__(controller)
        self.state = "choice_direction"
        self.directions = self.controller.get_possible_moves()
        self.selection = SelectionHelper(self.directions)

        # Choix direction
        self.input_manager.register(curses.KEY_LEFT, "choice_direction", "direction_left")
        self.input_manager.register(curses.KEY_RIGHT, "choice_direction", "direction_right")
        self.input_manager.register(ord(" "), "choice_direction", "direction_validate")
        self.input_manager.register(ord("\n"), "choice_direction", "direction_validate")
        for i in range(1, 6):
            self.input_manager.register(ord(str(i)), "choice_direction", f"direction_{i}")

        # Déplacement
        self.input_manager.register(ord(" "), "move", "advance_step")

    def handle_input_contextual(self, action):
        if not action:
            self.controller.messages.append("Action non reconnue.")
            return

        if self.state == "choice_direction":
            self.handle_direction_choice(action)
        elif self.state == "move":
            self.handle_move(action)

    def handle_direction_choice(self, action_name):
        if action_name.get("choice_direction") == "direction_left":
            self.selection.move_left()
        elif action_name.get("choice_direction") == "direction_right":
            self.selection.move_right()
        elif action_name.get("choice_direction") == "direction_validate":
            self.start_move()
        elif action_name.get("choice_direction"):
            if action_name.get("choice_direction").startswith("direction_"):
                number = int(action_name.get("choice_direction").split("_")[1])
                if self.selection.select_by_number(number):
                    self.start_move()
                else:
                    self.controller.messages.append("Direction invalide.")

    def start_move(self):
        selected_dest = self.selection.get_selected()
        if selected_dest:
            self.controller.messages.append(f"Déplacement vers {selected_dest.name}...")
            index = self.selection.index
            self.controller.move_to(index)
            self.controller.set_context(WalkingContext(self.controller))
        else:
            self.controller.messages.append("Aucune direction sélectionnée.")

    def handle_move(self, action):
        if action.get("move") == "advance_step":
            self.controller.advance_step()
            if not self.controller.game.player.current_path:
                self.directions = self.controller.get_possible_moves()
                self.selection = SelectionHelper(self.directions)
                self.state = "choice_direction"
    
    def render_zone_content(self, zone_win):
        y = 1
        if self.state == "choice_direction":
            zone_win.addstr(y, 2, "Choisissez une direction :")
            y += 1
            y += draw_selection_list(
                win=zone_win,
                items=[dest.name for dest in self.directions],
                selection_index=self.selection.index,
                start_y=y
            )
        
        # Affiche les entités dans la zone
        y += 1
        if (self.controller.game.current_area.get_other_entities(self.controller.game.player) == []):
            zone_win.addstr(y, 2, "Il n'y a personne ici.")
        else:
            zone_win.addstr(y, 2, "Personnes dans la zone :")
        y += 1
        for entity in self.controller.game.current_area.get_other_entities(self.controller.game.player):
            zone_win.addstr(y, 2, f"    - {entity.name}")
            y += 1

    def draw_multiline(self, win, lines, max_height):
        """Draw multiline text in a window, respecting the maximum height."""
        for i, line in enumerate(lines):
            if i + 1 < max_height - 1:
                try:
                    win.addstr(i + 1, 2, line)
                except curses.error:
                    pass  # ignore overflow silently
