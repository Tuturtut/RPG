from actions.Action import Action
from entities.Entity import Entity

class AttackAction(Action):
    def __init__(self, name, rounds=0, description="", proc_chance=1, needs_target=True, valid_target_types=[Entity], additional_damage=0):
        super().__init__(name, rounds, description=description, proc_chance=proc_chance, needs_target=needs_target, valid_target_types=valid_target_types)
        self.additional_damage = additional_damage
    def perform(self, user, messages=None):
        if messages is not None:
            messages.append(f"{user.getName()} attaque {self.target.getName()} avec {self.name}.")
        self.target.take_damage(user.damage + self.additional_damage, messages=messages)
