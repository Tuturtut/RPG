import random
from logger import logger  # Ajouté pour le logging

class Action:
    def __init__(self, name, rounds, target=None, description="", proc_chance=1, usable=True, needs_target=True, valid_target_types=None):
        self.name = name
        self.description = description
        self.rounds = rounds
        self.rounds_left = rounds
        self.target = target
        self.proc_chance = proc_chance
        self.usable = usable
        self.needs_target = needs_target
        self.valid_target_types = valid_target_types if valid_target_types is not None else []
        logger.debug(f"Action created: {self.name}, needs_target={self.needs_target}, rounds={self.rounds}")

    def needsTarget(self):
        return self.needs_target

    def execute(self, user):
        if self.rounds_left > 0:
            print(f"{user.getName()} prepares {self.name} ({self.rounds_left} rounds left)")
            self.setRoundsLeft(self.rounds_left - 1)
            logger.debug(f"{user.getName()} is charging {self.name}: {self.rounds_left} rounds left")
            return

        if random.random() > self.proc_chance:
            print(f"{user.getName()} failed to execute {self.name}")
            self.setRoundsLeft(self.rounds)
            logger.debug(f"{user.getName()} failed {self.name}, resetting rounds to {self.rounds}")
            return

        if self.needs_target:
            if self.target is None:
                print(f"{user.getName()} cannot perform {self.name} without a target")
                self.setRoundsLeft(self.rounds)
                logger.warning(f"{user.getName()} tried to perform {self.name} without a target")
                return
        else:
            print(f"{user.getName()} performs {self.name}")

        self.perform(user)

        self.setRoundsLeft(self.rounds)
        logger.debug(f"{user.getName()} executed {self.name}, rounds reset to {self.rounds}")

    def setRoundsLeft(self, rounds_left):
        self.rounds_left = rounds_left
        if self.rounds_left < 0:
            self.rounds_left = 0
        logger.debug(f"Rounds left for {self.name}: {self.rounds_left}")
        print("Rounds left: " + str(self.rounds_left))

    def perform(self, user):
        raise NotImplementedError("Subclasses must implement perform()")

    def setTarget(self, target):
        if self.rounds_left == self.rounds:
            self.target = target
            logger.debug(f"Target set for {self.name}: {self.target}")

    def __str__(self):
        return self.name
