from Actions.Action import Action
from EventManager import EventManager
from random import randint


class SummonEntityAction(Action):
    def __init__(self, name, entity,rounds=0, description="", proc_chance=1):
        super().__init__(name, rounds, description=description, proc_chance=proc_chance)
        self.entity = entity

    def perform(self, user):
        print(f"{user.name} successfully summons {self.entity.name}")
        EventManager.emit("summon", self.entity)
