class Action:
    def __init__(self, name, rounds,  target=None, description=""):
        self.name = name
        self.description = description
        self.rounds = rounds
        self.rounds_left = rounds
        self.target = target
    
    def execute(self, user):
        raise NotImplementedError("execute must be overridden")
    
    def setTarget(self, target):
        if self.rounds_left == self.rounds:
            self.target = target
