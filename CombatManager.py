from Entity import Entity
from EventManager import EventManager
from Goblin import Goblin
import time


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
        if event == "summon" and isinstance(data, Goblin):
            self.add_enemy(data)
    
    def run_combat(self):
        while self.player.is_alive() and any(enemy.is_alive() for enemy in self.current_enemies):
            self.player_turn()
            self.enemy_turn()

            self.show_turn()
            time.sleep(3)

        self.show_results()

    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            goblin1 = Goblin("Goblin 1")
            goblin2 = Goblin("Goblin 2")


            player = Entity("John", 100, 40, 5)

            cls._instance = CombatManager(player, [goblin1, goblin2])
        return cls._instance

    def player_turn(self):
        if (self.player.is_alive()):
            self.player.attack(self.current_enemies[0])

        time.sleep(1)

    
    def enemy_turn(self):
        for enemy in self.current_enemies:
            if enemy.is_alive():
                enemy.attack(self.player)
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
            print("You win!")
        else:
            print("You lose!")

    def add_enemy(self, enemy):
        self.current_enemies.append(enemy)