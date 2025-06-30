from utils.InputManager import InputManager
import curses

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
            self.input_manager.register(ord(str(i)), "choice_action" ,f"action_{i}")

        # Cible navigation
        self.input_manager.register(curses.KEY_LEFT, "choice_action", "action_left")
        self.input_manager.register(curses.KEY_RIGHT, "choice_action", "action_right")
        self.input_manager.register(ord(" "), "choice_action", "action_validate")
        self.input_manager.register(ord("\n"), "choice_action", "action_validate")

        self.input_manager.register(curses.KEY_LEFT, "choice_target", "target_left")
        self.input_manager.register(curses.KEY_RIGHT, "choice_target", "target_right")
        self.input_manager.register(ord(" "), "choice_target", "target_validate")
        self.input_manager.register(ord("\n"), "choice_target", "target_validate")

    def handle_input(self, key):
        
        action_name = self.input_manager.get_action(key, self.state)

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
        actions = self.combat_manager.player.actions
        if not actions:
            self.controller.messages.append("Aucune action disponible.")
            self.state = "end"
            return
        if (not action_name):
            self.controller.messages.append("Action non reconnue.")
            return
        if action_name.get("choice_action") == "action_left":
            self.selected_action_index = (self.selected_action_index - 1) % len(actions)
        elif action_name.get("choice_action") == "action_right":
            self.selected_action_index = (self.selected_action_index + 1) % len(actions)
        elif action_name.get("choice_action") == "action_validate":
            selected_action = actions[self.selected_action_index]
            self.controller.messages.append(f"Action choisie : {selected_action.name}")

            if selected_action.needsTarget():
                self.state = "choice_target"
            else:
                self.state = "execute_player"
        elif action_name.get("choice_action").startswith("action_"):

            index = int(action_name.get("choice_action").split("_")[1])
            selected_action = actions[index-1]
            self.controller.messages.append(f"Action choisie : {selected_action.name}")

            if selected_action.needsTarget():
                self.state = "choice_target"
            else:
                self.state = "execute_player"
        
        else:
            self.controller.messages.append(f"Action non reconnue : {action_name}")


    def handle_target_choice(self, action_name):
        """Handle input for the target choice state"""
        
        enemies = self.combat_manager.current_enemies
        if not enemies:
            self.controller.messages.append("Aucun ennemi disponible.")
            self.state = "end"
            return
        
        if not action_name:
            self.controller.messages.append("Cible non reconnue.")
            return

        if action_name.get("choice_target") == "target_left":
            self.selected_target_index = (self.selected_target_index - 1) % len(enemies)
        elif action_name.get("choice_target") == "target_right":
            self.selected_target_index = (self.selected_target_index + 1) % len(enemies)
        elif action_name.get("choice_target") == "target_validate":
            # Vérifiez si l'index sélectionné correspond à une entité valide
            if self.selected_target_index < len(enemies) and enemies[self.selected_target_index].is_alive():
                self.state = "execute_player"
            else:
                # Si l'entité est morte, mettez à jour l'index sélectionné pour pointer vers la prochaine entité valide
                self.selected_target_index = next((i for i, enemy in enumerate(enemies) if enemy.is_alive()), None)
                if self.selected_target_index is None:
                    self.controller.messages.append("Aucun ennemi disponible.")
                    self.state = "end"
                else:
                    self.state = "choice_target"

    def execute_player_turn(self):
        player = self.combat_manager.player
        action = player.actions[self.selected_action_index]

        if action.needsTarget():
            # Vérifiez si l'index sélectionné correspond à une entité valide
            if self.selected_target_index < len(self.combat_manager.current_enemies) and self.combat_manager.current_enemies[self.selected_target_index].is_alive():
                target = self.combat_manager.current_enemies[self.selected_target_index]
            else:
                # Si l'entité est morte, mettez à jour l'index sélectionné pour pointer vers la prochaine entité valide
                self.selected_target_index = next((i for i, enemy in enumerate(self.combat_manager.current_enemies) if enemy.is_alive()), None)
                if self.selected_target_index is None:
                    self.controller.messages.append("Aucun ennemi disponible.")
                    self.state = "end"
                    return
                else:
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
                marker = " <--" if i == self.selected_action_index else ""
                zone_win.addstr(y + 2 + i, 4, f"{i+1}. {action.name}{marker}")

        elif self.state == "choice_target":
            zone_win.addstr(y + 1, 2, "Cibles :")
            for i, enemy in enumerate(self.combat_manager.current_enemies):
                marker = " <--" if i == self.selected_target_index else ""
                zone_win.addstr(y + 2 + i, 4, f"{i+1}.{enemy.getName()}{marker}")

        elif self.state == "end":
            from tui.interface.ExplorationContext import ExplorationContext

            self.controller.set_context(ExplorationContext(self.controller))

        # Dialogue/messages
        max_lines = dialogue_win.getmaxyx()[0] - 3
        for i, msg in enumerate(self.controller.messages[-max_lines:]):
            dialogue_win.addstr(1 + i, 2, msg)

        # Refresh
        info_win.refresh()
        zone_win.refresh()
        dialogue_win.refresh()


