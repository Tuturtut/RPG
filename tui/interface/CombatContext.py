import curses
from utils.InputManager import InputManager
from tui.interface.BaseContext import BaseContext
from utils.helpers.SelectionHelper import SelectionHelper
from utils.ui import draw_selection_list

class CombatContext(BaseContext):
    def __init__(self, controller, combat_manager, calling_context=None):
        super().__init__(controller)
        self.combat_manager = combat_manager

        self.calling_context = calling_context

        self.state = "choice_action"
        self.action_selection = SelectionHelper(self.combat_manager.player.actions)
        self.target_selection = SelectionHelper(self.combat_manager.current_enemies)

        # Actions : navigation et validation
        self.input_manager.register(curses.KEY_LEFT, "choice_action", "action_left")
        self.input_manager.register(curses.KEY_RIGHT, "choice_action", "action_right")
        self.input_manager.register(ord(" "), "choice_action", "action_validate")
        self.input_manager.register(ord("\n"), "choice_action", "action_validate")
        for i in range(1, 6):
            self.input_manager.register(ord(str(i)), "choice_action", f"action_{i}")

        # Cibles : navigation et validation
        self.input_manager.register(curses.KEY_LEFT, "choice_target", "target_left")
        self.input_manager.register(curses.KEY_RIGHT, "choice_target", "target_right")
        self.input_manager.register(ord(" "), "choice_target", "target_validate")
        self.input_manager.register(ord("\n"), "choice_target", "target_validate")
    
    def handle_input_contextual(self, action):
        if not action:
            self.controller.messages.append("Action non reconnue.")
            return

        if self.state == "choice_action":
            self.handle_action_choice(action)
        elif self.state == "choice_target":
            self.handle_target_choice(action)
        elif self.state == "execute_player":
            self.execute_player_turn()
        elif self.state == "execute_enemies":
            self.execute_enemy_turn()
        elif self.state == "check_end":
            self.check_combat_end()

    def handle_action_choice(self, action_name):
        if action_name.get("choice_action") == "action_left":
            self.action_selection.move_left()
        elif action_name.get("choice_action") == "action_right":
            self.action_selection.move_right()
        elif action_name.get("choice_action") == "action_validate":
            self.confirm_action()
        elif action_name.get("choice_action").startswith("action_"):
            number = int(action_name.get("choice_action").split("_")[1])
            if self.action_selection.select_by_number(number):
                self.confirm_action()
            else:
                self.controller.messages.append("Action invalide.")

    def confirm_action(self):
        action = self.action_selection.get_selected()
        if action:
            self.controller.messages.append(f"Action choisie : {action.name}")
            if action.needsTarget():
                self.state = "choice_target"
                self.target_selection = SelectionHelper(
                    [e for e in self.combat_manager.current_enemies if e.is_alive()]
                )
            else:
                self.state = "execute_player"
        else:
            self.controller.messages.append("Aucune action sélectionnée.")

    def handle_target_choice(self, action_name):
        if action_name.get("choice_target") == "target_left":
            self.target_selection.move_left()
        elif action_name.get("choice_target") == "target_right":
            self.target_selection.move_right()
        elif action_name.get("choice_target") == "target_validate":
            self.state = "execute_player"

    def execute_player_turn(self):
        player = self.combat_manager.player
        action = self.action_selection.get_selected()
        target = self.target_selection.get_selected() if action and action.needsTarget() else None

        if action:
            action.setTarget(target)
            player.use_action(action, messages=self.controller.messages)

        self.state = "execute_enemies"

    def execute_enemy_turn(self):
        for enemy in self.combat_manager.current_enemies[:]:
            if enemy.is_alive():
                action = enemy.getAction()
                action.setTarget(self.combat_manager.player)
                enemy.use_action(action, messages=self.controller.messages)
            else:
                self.combat_manager.current_enemies.remove(enemy)

        self.state = "check_end"

    def check_combat_end(self):
        if not self.combat_manager.player.is_alive():
            self.controller.messages.append("Défaite...")
            self.state = "end"
        elif not any(enemy.is_alive() for enemy in self.combat_manager.current_enemies):
            self.controller.messages.append("Victoire !")
            self.state = "end"
        else:
            self.state = "choice_action"

    def render_zone_content(self, zone_win):
        # Affiche joueur
        zone_win.addstr(1, 2, f"{self.combat_manager.player.getName()}")
        hp_lines = self.combat_manager.player.health_bar(
            self.combat_manager.player.health,
            self.combat_manager.player.max_health
        ).splitlines()
        for i, line in enumerate(hp_lines):
            zone_win.addstr(2 + i, 4, line)

        # Affiche ennemis
        y = 2 + len(hp_lines) + 1
        zone_win.addstr(y, 2, "Ennemis :")
        y += 1
        y = draw_selection_list(
                win=zone_win,
                items=[f"{e.getName()}\n\t{e.health_bar(e.health, e.max_health)}" for e in self.target_selection.items],
                selection_index=self.target_selection.index,
                start_y=y + 1,
                has_marker=self.state == "choice_target"
            )


        if self.state == "choice_action":
            zone_win.addstr(y, 2, "Actions :")
            draw_selection_list(
                win=zone_win,
                items=[a.name for a in self.combat_manager.player.actions],
                selection_index=self.action_selection.index,
                start_y=y + 1
            )

        elif self.state == "end":
            if (self.calling_context):
                self.controller.set_context(self.calling_context)
                return
            
            from tui.interface.ExplorationContext import ExplorationContext
            self.controller.set_context(self.controller.exploration_context)
