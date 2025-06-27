import random

class Path:
    def __init__(self, start, end, steps=5):
        self.start = start
        self.end = end
        self.steps = steps
        self.events = {}  # {step: MapEvent}
        self.random_events = []
        self.random_chance = 0.3

        start.add_connection(end, self)
        end.add_connection(start, self)

    def add_random_event(self, event, weight=1):
        self.random_events.append((event, weight))
    
    def add_event(self, step, event):
        if step < 0 or step >= self.steps:
            raise ValueError("Step must be within the range of the path.")
        self.events[step] = event
    
    def trigger_random_event(self, world_state, player):
        if not self.random_events:
            return
        if random.random() < self.random_chance:
            total = sum(weight for (_, weight) in self.random_events)
            r = random.uniform(0, total)
            acc = 0
            for event, weight in self.random_events:
                acc += weight
                if r <= acc:
                    event.execute(world_state, player)
                    return event

    def get_other_end(self, from_area):
        return self.end if from_area == self.start else self.start