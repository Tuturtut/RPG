from tui.interface.InterfaceContext import InterfaceContext

class BaseContext(InterfaceContext):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

    def render(self, info_win, zone_win, dialogue_win):
        info_win.clear(); info_win.box()
        zone_win.clear(); zone_win.box()
        dialogue_win.clear(); dialogue_win.box()

        # Infos globales
        self.draw_multiline(info_win, self.controller.render_game_info().split("\n"), info_win.getmaxyx()[0])

        # Partie spécifique
        self.render_zone_content(zone_win)

        # Messages
        self.draw_multiline(dialogue_win, self.controller.render_messages().split("\n"), dialogue_win.getmaxyx()[0])

        info_win.refresh()
        zone_win.refresh()
        dialogue_win.refresh()

    def draw_multiline(self, win, lines, max_height):
        for i, line in enumerate(lines):
            if i + 1 < max_height - 1:
                try:
                    win.addstr(i + 1, 2, line)
                except Exception:
                    pass  # Ignore overflow silently

    def render_zone_content(self, zone_win):
        raise NotImplementedError("Les sous-classes doivent implémenter render_zone_content.")

