import random

class Action:
    def __init__(self, name, rounds,  target=None, description="", proc_chance=1):
        self.name = name
        self.description = description
        self.rounds = rounds
        self.rounds_left = rounds
        self.target = target
        self.proc_chance = proc_chance
    
    def execute(self, user):
        if self.rounds_left > 0:
            print(f"{user.name} prepares {self.name} ({self.rounds_left} rounds left)")
            self.setRoundsLeft(self.rounds_left - 1)
            return

        if random.random() > self.proc_chance:
            print(f"{user.name} failed to execute {self.name}")
            # Recommencer le chargement si échoué
            self.setRoundsLeft(self.rounds)
            return

        print(f"{user.name} uses {self.name} on {self.target.name if self.target else 'n/a'}")
        self.perform(user)

        self.setRoundsLeft(self.rounds)
    def setRoundsLeft(self, rounds_left):
        self.rounds_left = rounds_left
        if (self.rounds_left < 0):
            self.rounds_left = 0
        print("Rounds left: " + str(self.rounds_left))



    def perform(self, user):
        raise NotImplementedError("Subclasses must implement perform()")
    
    def setTarget(self, target):
        if self.rounds_left == self.rounds:
            self.target = target

    def __str__(self):
        return self.name
