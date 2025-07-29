from tui.interface.InterfaceContext import InterfaceContext
from utils.InputManager import InputManager

class CombatContext(InterfaceContext):
    def __init__(self, controller):
        super().__init__(controller)
        self.fight_active = True  # Indique si le combat est en cours
        self.input_manager = InputManager()
        self.input_manager.register(ord('q'), 'quit')


    def handle_input(self, key):
        """ Gère les entrées utilisateur pendant le combat """

        action = self.input_manager.get_action(key)

        if action == 'quit':
            self.fight_active = False
            self.controller.messages.append("Vous avez quitté le combat.")
            return "quit"
        # Ajouter d'autres commandes de combat ici
        return None

    def render(self, info_win, zone_win, dialogue_win, debug_win=None):
        """ Affiche les informations du combat """
        info_win.clear(); info_win.box()
        zone_win.clear(); zone_win.box()
        dialogue_win.clear(); dialogue_win.box()

        if debug_win is not None:
            debug_win.clear(); debug_win.box()

        info_win.addstr(1, 2, "Combat en cours...")
        # Afficher les détails du combat ici

        info_win.refresh()
        zone_win.refresh()
        dialogue_win.refresh()

        if debug_win is not None:
            debug_win.addstr(1, 2, "CombatContext")
            debug_win.refresh()