from utils.InputManager import InputManager

class CombatContext:
    def __init__(self, controller, combat_manager):
        self.controller = controller
        self.combat_manager = combat_manager

        self.state = "choice_action"
        self.selected_action_index = 0
        self.selected_target_index = 0

        self.input_manager = InputManager()

        # Actions : mappe 1-5 → action_1 à action_5
        for i in range(1, 6):
            self.input_manager.register(ord(str(i)), f"action_{i}")

        # Cible navigation
        self.input_manager.register(ord("a"), "target_left")
        self.input_manager.register(ord("e"), "target_right")
        self.input_manager.register(ord("d"), "target_validate")

        # Quitter
        self.input_manager.register(ord("q"), "quit")

    def handle_input(self, key):
        action_name = self.input_manager.get_action(key)

        if action_name == "quit":
            self.state = "end"

        elif self.state == "choice_action":
            self.handle_action_choice(action_name)

        elif self.state == "choice_target":
            self.handle_target_choice(action_name)

        elif self.state == "execute_player":
            self.execute_player_turn()

        elif self.state == "execute_enemies":
            self.execute_enemy_turn()

        elif self.state == "check_end":
            self.check_combat_end()

    def handle_action_choice(self, action_name):
        if action_name and action_name.startswith("action_"):
            index = int(action_name.split("_")[1])
            self.selected_action_index = index - 1
            selected_action = self.combat_manager.player.actions[self.selected_action_index]
            self.controller.messages.append(f"Action choisie : {selected_action.name}")

            if selected_action.needsTarget():
                self.state = "choice_target"
            else:
                self.state = "execute_player"
        else:
            self.controller.messages.append(f"Action non reconnue : {action_name}")

    def handle_target_choice(self, action_name):
        enemies = self.combat_manager.current_enemies
        if not enemies:
            self.controller.messages.append("Aucun ennemi disponible.")
            self.state = "end"
            return

        if action_name == "target_left":
            self.selected_target_index = (self.selected_target_index - 1) % len(enemies)
        elif action_name == "target_right":
            self.selected_target_index = (self.selected_target_index + 1) % len(enemies)
        elif action_name == "target_validate":
            self.state = "execute_player"

    def execute_player_turn(self):
        player = self.combat_manager.player
        action = player.actions[self.selected_action_index]

        if action.needsTarget():
            target = self.combat_manager.current_enemies[self.selected_target_index]
        else:
            target = None

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

    def render(self, info_win, zone_win, dialogue_win):
        info_win.clear(); info_win.box()
        zone_win.clear(); zone_win.box()
        dialogue_win.clear(); dialogue_win.box()

        # Info combat
        info_win.addstr(1, 2, f"Combat : {self.combat_manager.player.getName()} vs {len(self.combat_manager.current_enemies)} ennemis")

        # Affiche le joueur
        zone_win.addstr(1, 2, f"{self.combat_manager.player.getName()}")
        hp_lines = self.combat_manager.player.health_bar(
            self.combat_manager.player.health,
            self.combat_manager.player.max_health
        ).splitlines()
        for i, line in enumerate(hp_lines):
            zone_win.addstr(2 + i, 4, line)

        # Affiche les ennemis
        zone_win.addstr(5, 2, "Ennemis :")
        y = 6
        for enemy in self.combat_manager.current_enemies:
            zone_win.addstr(y, 4, enemy.getName())
            hp_lines = enemy.health_bar(enemy.health, enemy.max_health).splitlines()
            for hp_line in hp_lines:
                y += 1
                zone_win.addstr(y, 6, hp_line)
            y += 1  # espace entre ennemis

        # Actions si nécessaire
        if self.state == "choice_action":
            zone_win.addstr(y + 1, 2, "Actions :")
            for i, action in enumerate(self.combat_manager.player.actions):
                marker = " (choisie)" if i == self.selected_action_index else ""
                zone_win.addstr(y + 2 + i, 4, f"{i+1}. {action.name}{marker}")

        elif self.state == "choice_target":
            zone_win.addstr(y + 1, 2, "Cibles :")
            for i, enemy in enumerate(self.combat_manager.current_enemies):
                marker = " (cible)" if i == self.selected_target_index else ""
                zone_win.addstr(y + 2 + i, 4, f"{enemy.getName()}{marker}")

        elif self.state == "end":
            from tui.interface.ExplorationContext import ExplorationContext

            zone_win.addstr(y + 1, 2, "Combat terminé. Appuyez sur q.")
            self.controller.set_context(ExplorationContext(self.controller))

        # Dialogue/messages
        max_lines = dialogue_win.getmaxyx()[0] - 3
        for i, msg in enumerate(self.controller.messages[-max_lines:]):
            dialogue_win.addstr(1 + i, 2, msg)

        # Refresh
        info_win.refresh()
        zone_win.refresh()
        dialogue_win.refresh()


