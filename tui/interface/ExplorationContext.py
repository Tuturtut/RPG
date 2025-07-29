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
    
    def render(self, info_win, zone_win, dialogue_win, debug_win=None):
        """Render the exploration context."""

    def render_zone_content(self, zone_win):
        if self.state == "choice_direction":
            zone_win.addstr(1, 2, "Choisissez une direction :")
            y = draw_selection_list(
                win=zone_win,
                items=[dest.name for dest in self.directions],
                selection_index=self.selection.index,
                start_y=2
            )

        if debug_win is not None:
            debug_win.clear(); debug_win.box()

        self.draw_multiline(info_win, self.controller.render_game_info().split("\n"), info_win.getmaxyx()[0])
        self.draw_multiline(zone_win, self.controller.render_zone().split("\n"), zone_win.getmaxyx()[0])
        self.draw_multiline(dialogue_win, self.controller.render_messages().split("\n"), dialogue_win.getmaxyx()[0])


        info_win.refresh()
        zone_win.refresh()
        dialogue_win.refresh()

        if debug_win is not None:
            debug_win.addstr(1, 2, "ExplorationContext")
            debug_win.refresh()

    def draw_multiline(self, win, lines, max_height):
        """Draw multiline text in a window, respecting the maximum height."""
        for i, line in enumerate(lines):
            if i + 1 < max_height - 1:
                try:
                    win.addstr(i + 1, 2, line)
                except curses.error:
                    pass  # ignore overflow silently
