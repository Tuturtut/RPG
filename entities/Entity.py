import random
from capabilities.Talkable import Talkable
from actions.NoneAction import NoneAction

from logger import logger

class Entity(Talkable):
    def __init__(self, name, health, damage, defense, actions=None):
        super().__init__()
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.defense = defense
        self.actions = actions
        if actions is None:
            actions = [NoneAction()]
        self.current_action = None
        self.location = None
    
    def getName(self):
        return f"[{self.name}]"

    def __str__(self):
        return f"{self.getName()} {self.health_bar(self.health, self.max_health)}"
    

    def health_bar(self, current, max_hp, length=20):
        filled = int(length * current / max_hp)
        empty = length - filled
        return f"[{'█'*filled}{'░'*empty}] {current}/{max_hp}\n"
    
    def take_damage(self, damage):
        final_damage = max(0, damage - self.defense)
        self.health -= final_damage
        print(f"{self.getName()} takes {final_damage} damage!")
        print(self.health_bar(self.health, self.max_health))
        self.after_taking_damage()


    def after_taking_damage(self):
        pass
    
    def use_action(self, action):
        action.execute(self)
    
    def is_injured(self):
        return self.health < self.max_health
    
    def is_alive(self):
        return self.health > 0
    
    def setTarget(self, target):
        if not self.current_action.needsTarget():
            return

        if not any(isinstance(target, t) for t in self.current_action.valid_target_types):
            logger.warning(f"{self.getName()} tried to set an invalid target: {target.getName()}")
            self.current_action.setTarget(None)
            return

        self.current_action.setTarget(target)


    # Renvoie une action au hasard ou retourne l'action courante si elle n'est pas terminée
    def getAction(self):
        if self.current_action is None:
            self.current_action = self.getRandomAction()
            logger.debug(f"{self.getName()} selected new action: {self.current_action.name}")
            return self.current_action
        else:
            if self.current_action.rounds_left > 0:
                logger.debug(f"{self.getName()} continues with action: {self.current_action.name}")
                return self.current_action
            else:
                logger.debug(f"{self.getName()} action finished: {self.current_action.name}")
                return self.current_action


    
    def getRandomAction(self):
        if not self.actions:
            return NoneAction()

        return self.actions[random.randint(0, len(self.actions) - 1)]
    
    def addAction(self, action):
        self.actions.append(action)
    

    def describe(self):
        return f"{self.name}"
    
