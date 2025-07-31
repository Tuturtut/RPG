class Event:
    def __init__(self, description=None):
        self.message = None 
        self.description = description

    def execute(self, world_state, entity):
        self.message = (f"[Événement] {self.message}")
