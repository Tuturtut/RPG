from tui.interface.InterfaceContext import InterfaceContext
from utils.debug import log, get_logs
from utils.InputManager import InputManager

class BaseContext(InterfaceContext):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.input_manager = InputManager()

        self.input_manager.register(ord("q"), "quit", "quit")

    

    def handle_input(self, key):
        action = self.input_manager.get_action(key, self.state)

        if action and ("quit" in action.values()):
            return "quit"

        # Laisse les sous-classes gérer la suite
        return self.handle_input_contextual(action)


    def render(self, info_win, zone_win, dialogue_win, debug_win=None):
        info_win.clear(); info_win.box()
        zone_win.clear(); zone_win.box()
        dialogue_win.clear(); dialogue_win.box()

        self.draw_multiline(info_win, self.controller.render_game_info().split("\n"), info_win.getmaxyx()[0])
        self.render_zone_content(zone_win)  # reste identique
        self.draw_multiline(dialogue_win, self.controller.render_messages().split("\n"), dialogue_win.getmaxyx()[0])

        info_win.refresh(); zone_win.refresh(); dialogue_win.refresh()

        if debug_win is not None:
            debug_win.clear(); debug_win.box()
            # Option: un hook debug si besoin (ex. nom du contexte)
            try:
                self.draw_multiline(debug_win, get_logs(), debug_win.getmaxyx()[0])
            except Exception:
                pass
            debug_win.refresh()


    def draw_multiline(self, win, lines, max_height):
        for i, line in enumerate(lines):
            if i + 1 < max_height - 1:
                try:
                    win.addstr(i + 1, 2, line)
                except Exception:
                    pass  # Ignore overflow silently

    def render_zone_content(self, zone_win):
        raise NotImplementedError("Les sous-classes doivent implémenter render_zone_content.")

