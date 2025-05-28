from Actions.Action import Action
from EventManager import EventManager
from random import randint


class SummonEntityAction(Action):
    def __init__(self, name, create_entity_function,rounds=0, description="", proc_chance=1):
        super().__init__(name, rounds, description=description, proc_chance=proc_chance)
        self.create_entity_function = create_entity_function

    def perform(self, user):
        print(f"[{user.name}] successfully summons [{self.create_entity_function().name}]")
        EventManager.emit("summon", self.create_entity_function())

