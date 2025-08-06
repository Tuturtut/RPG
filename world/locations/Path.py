import random
from world.locations.Location import Location

class Path(Location):
    def __init__(self, start, end, steps=5):
        super().__init__()
        self.start = start
        self.end = end
        self.steps = steps

        start.add_connection(end, self)
        end.add_connection(start, self)

    def add_event_at(self, step, event):
        # self.events[step] = event
        pass

    def get_other_end(self, from_area):
        return self.end if from_area == self.start else self.start
    
    def get_name(self):
        return f"{self.start.name} -> {self.end.name}"

    def __str__(self):
        return f"[{self.end.name}]"