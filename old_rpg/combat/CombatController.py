from utils.InputManager import InputManager
import curses

class CombatController:
    def __init__(self, combat_manager):
        self.combat_manager = combat_manager
        self.state = "choice_action"  # états : choix_action, choix_cible, tour_enemy, fin
        self.selected_action_index = 0
        self.selected_target_index = 0

        self.input_manager = InputManager()
        self.input_manager.register(ord("1"), "action_1")
        self.input_manager.register(ord("2"), "action_2")
        self.input_manager.register(ord("3"), "action_3")
        self.input_manager.register(ord("4"), "action_4")
        self.input_manager.register(ord("5"), "action_5")
        self.input_manager.register(curses.KEY_LEFT, "target_left")
        self.input_manager.register(curses.KEY_RIGHT, "target_right")
        self.input_manager.register(ord(" "), "target_validate")
        self.input_manager.register(ord("\n"), "target_validate")

    def handle_input(self, key):
        if self.state == "choice_action":
            if key in (ord("1"), ord("2"), ord("3"), ord("4"), ord("5")):
                self.selected_action_index = key - ord("1")
                self.state = "choice_target" if self.combat_manager.player.actions[self.selected_action_index].needsTarget() else "execute"
            

        elif self.state == "choice_target":
            if key in (ord("a"), ord("e")):
                # Navigation gauche/droite entre les cibles
                self.selected_target_index += 1 if key == ord("a") else -1
                self.selected_target_index %= len(self.combat_manager.current_enemies)
            elif key == ord("d"):
                self.state = "execute"
            elif key == ord("q"):
                self.state = "end"

        if self.state == "execute":
            self.next_player_turn()
            if not self.combat_manager.is_combat_over():
                self.combat_manager.next_enemy_turn()
            self.state = "choice_action" if not self.combat_manager.is_combat_over() else "end"

    def render_combat(self):
        if not self.combat_manager:
            return "Aucun combat en cours."

        lines = []
        lines.append(f"Combat : {self.combat_manager.player.getName()} vs {len(self.combat_manager.current_enemies)} ennemis")
        lines.append("\nActions :")
        for i, action in enumerate(self.combat_manager.player.actions):
            marker = " (choisie)" if i == self.selected_action_index else ""
            lines.append(f"{i + 1}. {action.name}{marker}")

        lines.append("\nCibles :")
        for i, enemy in enumerate(self.combat_manager.current_enemies):
            marker = " (cible)" if i == self.selected_target_index else ""
            lines.append(f"{i + 1}. {enemy.getName()} {enemy.health_bar(enemy.health, enemy.max_health).strip()}{marker}")

        return "\n".join(lines)

    def next_player_turn(self):
        player = self.combat_manager.player
        player.setActionByIndex(self.selected_action_index)
        action = player.getAction()

        if action.needsTarget():
            player.setTargetByIndex(self.combat_manager.current_enemies, self.selected_target_index)
        else:
            player.setTargetByIndex(self.combat_manager.current_enemies, None)

        player.use_action(action)
