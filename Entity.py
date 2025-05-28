import random

class Entity:
    def __init__(self, name, health, damage, defense, actions=None):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.defense = defense
        self.actions = actions
        self.current_action = None
    
    def __str__(self):
        return f"{self.name} {self.health_bar(self.health, self.max_health)}"
    

    def health_bar(self, current, max_hp, length=20):
        filled = int(length * current / max_hp)
        empty = length - filled
        return f"[{'█'*filled}{'░'*empty}] {current}/{max_hp}\n"

    
    def take_damage(self, damage):
        final_damage = max(0, damage - self.defense)
        self.health -= final_damage
        # Affichage des dégâts dans un format lisible
        print(f"{self.name} takes {final_damage} damage!")
        print(self.health_bar(self.health, self.max_health))
    
    def use_action(self, action):
        action.execute(self)
    
    def is_alive(self):
        return self.health > 0
    
    def setTarget(self, target):
        for action in self.actions:
            action.setTarget(target)

    # Renvoie une action au hasard ou retourne l'action courante si elle n'est pas terminée
    def getAction(self):
        if self.current_action is None:
            self.current_action = self.getRandomAction()
            return self.current_action
        else:
            if self.current_action.rounds_left > 0:
                return self.current_action
            else:
                returned_action = self.current_action
                self.current_action = None
                return returned_action
    
    def getRandomAction(self):
        return self.actions[random.randint(0, len(self.actions) - 1)]
    
    def add_action(self, action):
        self.actions.append(action)
    