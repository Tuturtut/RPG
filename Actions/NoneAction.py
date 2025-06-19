from actions.Action import Action

class NoneAction(Action):
    def __init__(self):
        super().__init__(name="None", rounds=0, description="No action performed", proc_chance=1, needs_target=False, valid_target_types=None)
    
    def perform(self, user):
        print(f"{user.getName()} has no actions to performs.")