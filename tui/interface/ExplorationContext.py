import curses
from utils.InputManager import InputManager
from tui.interface.BaseContext import BaseContext
from utils.helpers.SelectionHelper import SelectionHelper
from utils.ui import draw_selection_list

class ExplorationContext(BaseContext):
    def __init__(self, controller):
        super().__init__(controller)
        self.input_manager = InputManager()

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

    def handle_input(self, key):
        action = self.input_manager.get_action(key, self.state)
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
        elif action_name.get("choice_direction").startswith("direction_"):
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
            self.state = "move"
        else:
            self.controller.messages.append("Aucune direction sélectionnée.")

    def handle_move(self, action_name):
        if action_name.get("move") == "advance_step":
            self.controller.advance_step()
            if not self.controller.current_path:
                self.directions = self.controller.get_possible_moves()
                self.selection = SelectionHelper(self.directions)
                self.state = "choice_direction"

    def render_zone_content(self, zone_win):
        if self.state == "choice_direction":
            zone_win.addstr(1, 2, "Choisissez une direction :")
            draw_selection_list(
                win=zone_win,
                items=[dest.name for dest in self.directions],
                selection_index=self.selection.index,
                start_y=2
            )

        elif self.state == "move":
            zone_win.addstr(1, 2, "Déplacement en cours... Appuyez sur ESPACE pour avancer.")