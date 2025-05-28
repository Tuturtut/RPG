from Actions.Action import Action

class AttackAction(Action):
    def __init__(self, name, rounds=0, description=""):
        super().__init__(name, rounds, description=description)
    
    def execute(self, user):

        if (self.rounds_left > 0):
            print(f"{user.name} attacks {self.target.name} -> {self.name} ({self.rounds_left} rounds left)")
            self.rounds_left -= 1
            return
        print(f"[{user.name} -> {self.target.name}]")
        self.target.take_damage(user.damage)
        self.rounds_left = self.rounds