class CombatController:
    def __init__(self, combat_manager):
        self.combat_manager = combat_manager
        self.state = "choix_action"  # états : choix_action, choix_cible, tour_enemy, fin
        self.selected_action_index = 0
        self.selected_target_index = 0

    def handle_input(self, key):
        if self.state == "choix_action":
            if key in (ord("1"), ord("2"), ord("3"), ord("4"), ord("5")):
                self.selected_action_index = key - ord("1")
                self.state = "choix_cible" if self.combat_manager.player.actions[self.selected_action_index].needsTarget() else "execute"
            elif key == ord("q"):
                self.state = "fin"
        
        elif self.state == "choix_cible":
            if key in (ord("a"), ord("d")):
                # Navigation gauche/droite entre les cibles
                self.selected_target_index += 1 if key == ord("d") else -1
                self.selected_target_index %= len(self.combat_manager.current_enemies)
            elif key == ord("e"):
                self.state = "execute"
            elif key == ord("q"):
                self.state = "fin"

        if self.state == "execute":
            self.next_player_turn()
            if not self.combat_manager.is_combat_over():
                self.combat_manager.next_enemy_turn()
            self.state = "choix_action" if not self.combat_manager.is_combat_over() else "fin"

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
