from Actions.Action import Action

class AttackAction(Action):
    def __init__(self, name, rounds=0, description="", proc_chance=1):
        super().__init__(name, rounds, description=description, proc_chance=proc_chance)
    
    def perform(self, user):
        self.target.take_damage(user.damage)