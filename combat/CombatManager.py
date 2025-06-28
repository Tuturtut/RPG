from entities.Entity import Entity
from EventManager import EventManager

class CombatManager:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.current_enemies = list(enemies)
        EventManager.register(self.handle_event)

    def handle_event(self, event, data):
        if event == "summon" and isinstance(data, Entity):
            self.add_enemy(data)

    def player_turn(self, action, target):
        if self.player.is_alive():
            action.setTarget(target)
            self.player.use_action(action)

    def enemy_turn(self):
        for enemy in self.current_enemies[:]:
            if enemy.is_alive():
                action = enemy.getAction()
                action.setTarget(self.player)
                enemy.use_action(action)
            else:
                self.current_enemies.remove(enemy)

    def is_combat_over(self):
        return not self.player.is_alive() or not any(enemy.is_alive() for enemy in self.current_enemies)

    def add_enemy(self, enemy):
        self.current_enemies.append(enemy)
