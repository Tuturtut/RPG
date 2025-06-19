from entities.Entity import Entity
from EventManager import EventManager
from entities.Goblin import Goblin
from entities.Player import Player
import time
from actions.AttackAction import AttackAction
from actions.SummonEntityAction import SummonEntityAction
from logger import logger


class CombatManager:

    _instance = None

    def __init__(self, player, enemies):
        if CombatManager._instance is not None:
            raise Exception("Use CombatManager.instance() instead of creating a new one.")
        self.player = player
        self.enemies = enemies
        self.current_enemies = list(enemies)

        EventManager.register(self.handle_event)
    

    def handle_event(self, event, data):
        if event == "summon" and isinstance(data, Entity):
            self.add_enemy(data)
    
    def run_combat(self):
        while self.player.is_alive() and any(enemy.is_alive() for enemy in self.current_enemies):
            self.player_turn()
            self.enemy_turn()

            self.show_turn()
            time.sleep(3)

        self.show_results()

    def player_turn(self):
        

        if (self.player.is_alive()):
            action = self.player.getAction()

            logger.debug(f"Player chose action: {action.name}")

            self.player.setTarget(self.current_enemies)
            self.player.use_action(action)

        time.sleep(1)

    
    def enemy_turn(self):
        print(f" - {self.player.name} ({self.player.health} PV) [{type(self.player)}]")
        for enemy in self.current_enemies[:]:
            if enemy.is_alive():
                action = enemy.getAction()
                enemy.setTarget(self.player)
                enemy.use_action(action)
            else: 
                self.current_enemies.remove(enemy)
        
            time.sleep(1)
    
    def show_turn(self):
        print("\n---------------Résultat du tour----------------")
        print(f"Player: {self.player}")
        for enemy in self.current_enemies:
            print(f"Enemy: {enemy}")
        print("\n")

    def show_results(self):
        if self.player.is_alive():
            logger.info("You win!")
        else:
            logger.info("You lose!")

    def add_enemy(self, enemy):
        self.current_enemies.append(enemy)
    
    @staticmethod
    def start(player, enemies):
        cm = CombatManager(player, enemies)
        cm.run_combat()