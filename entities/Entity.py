import random
from capabilities.Talkable import Talkable
from actions.NoneAction import NoneAction

class Entity(Talkable):
    def __init__(self, name, health, damage, defense, actions=None):
        super().__init__()
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.defense = defense
        self.actions = actions
        self.location = None
        if actions is None:
            actions = [NoneAction()]
        self.current_action = None
        self.current_path = None
    
    def getName(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.getName()} {self.health_bar(self.health, self.max_health)}"
    
    def get_current_path(self):
        return self.current_path


    def start_path(self, path, destination):
        from world.locations.EntityPath import EntityPath
        self.current_path = EntityPath(self, path)
        self.location = self.current_path.path
 
    def advance_path(self, game, controller):
        from utils.debug import log
        log(f"{self.getName()} va vers {self.current_path.destination} ({self.current_path.steps_done} / {self.current_path.path.steps}) index: {self.current_path.index}")
        self.location.trigger_events(self, controller)

        if self.current_path:
            arrived = self.current_path.advance(game)
            if arrived:
                log(f"{self.getName()} arrived at {self.location}")
                self.location = self.current_path.path.end
                self.location.trigger_events(self, controller)
                self.current_path = None
            return arrived
        return False, []

    def health_bar(self, current, max_hp, length=20):
        filled = int(length * current / max_hp)
        empty = length - filled
        return f"[{'█'*filled}{'░'*empty}] {current}/{max_hp}"
    
    def take_damage(self, damage, messages=None):
        final_damage = max(0, damage - self.defense)
        self.health -= final_damage

        if messages is not None:
            messages.append(f"{self.getName()} subit {final_damage} dégâts.")
            messages.append(f"{self.getName()} HP : {self.health}/{self.max_health}")

        if not self.is_alive() and messages is not None:
            messages.append(f"{self.getName()} est vaincu !")

        self.after_taking_damage()

    def after_taking_damage(self):
        pass
    
    def use_action(self, action, messages=None):
        action.execute(self, messages=messages)
    
    def is_injured(self):
        return self.health < self.max_health
    
    def is_alive(self):
        return self.health > 0
    
    def setTarget(self, target):
        if not self.current_action.needsTarget():
            return

        if not any(isinstance(target, t) for t in self.current_action.valid_target_types):
            self.current_action.setTarget(None)
            return

        self.current_action.setTarget(target)


    # Renvoie une action au hasard ou retourne l'action courante si elle n'est pas terminée
    def getAction(self):
        if self.current_action is None:
            self.current_action = self.getRandomAction()
            return self.current_action
        else:
            if self.current_action.rounds_left > 0:
                return self.current_action
            else:
                return self.current_action


    
    def getRandomAction(self):
        if not self.actions:
            return NoneAction()

        return self.actions[random.randint(0, len(self.actions) - 1)]
    
    def addAction(self, action):
        self.actions.append(action)
    

    def describe(self):
        return f"{self.name}"
    
