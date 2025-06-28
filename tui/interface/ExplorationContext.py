from tui.interface.InterfaceContext import InterfaceContext
import curses
from core.Game import Game
from utils.InputManager import InputManager
from tui.interface.CombatContext import CombatContext
from combat.CombatManager import CombatManager
from entities.Monster import Monster
from actions.AttackAction import AttackAction

class ExplorationContext(InterfaceContext):
    def __init__(self, controller):
        super().__init__(controller)
        self.input_manager = InputManager()
        self.input_manager.register(ord("q"), "quit")
        self.input_manager.register(ord(" "), "advance_step")
        for i in range(1, 6):
            self.input_manager.register(ord(str(i)), f"move_{i}")
        
        # TEMP
        self.input_manager.register(ord("c"), "combat")


    def handle_input(self, key):
        """Handle input for the exploration context."""

        action = self.input_manager.get_action(key)
        if not action:
            self.controller.messages.append("Action non reconnue.")
            return

        if action == "quit":
            self.controller.messages.append("Sortie du jeu.")
            return "quit"
        elif action == "advance_step":
            self.controller.advance_step()
        elif action.startswith("move_"):
            index = int(action.split("_")[1])
            self.controller.move_to(index-1)

        # TEMP
        elif action == "combat":
            player = self.controller.game.player
            enemies = [Monster("Loup", 25, 7, 1, [AttackAction("Attaque")]) for i in range(5)]        
            combat_manager = CombatManager(player, enemies)
            self.controller.set_context(CombatContext(self.controller, combat_manager))

        else:
            self.controller.messages.append(f"Action non reconnue : {action}")

    
    def render(self, info_win, zone_win, dialogue_win):
        """Render the exploration context."""

        info_win.clear(); info_win.box()
        zone_win.clear(); zone_win.box()
        dialogue_win.clear(); dialogue_win.box()

        self.draw_multiline(info_win, self.controller.render_game_info().split("\n"), info_win.getmaxyx()[0])
        self.draw_multiline(zone_win, self.controller.render_zone().split("\n"), zone_win.getmaxyx()[0])
        self.draw_multiline(dialogue_win, self.controller.render_messages().split("\n"), dialogue_win.getmaxyx()[0])


        info_win.refresh()
        zone_win.refresh()
        dialogue_win.refresh()

    def draw_multiline(self, win, lines, max_height):
        """Draw multiline text in a window, respecting the maximum height."""
        for i, line in enumerate(lines):
            if i + 1 < max_height - 1:
                try:
                    win.addstr(i + 1, 2, line)
                except curses.error:
                    pass  # ignore overflow silently