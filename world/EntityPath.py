class EntityPath:
    def __init__(self, path):
        self.path = path
        self.steps_done = 0
        self.triggered_event = []
    
    def get_triggered_events(self):
        if self.steps_done in self.path.events:
            self.triggered_event.append(self.path.events[self.steps_done])
        return self.triggered_event
    
    def advance(self, game):

        from utils.debug import log
        log(f"Advancing path {self}, steps done: {self.steps_done}")

        self.triggered_event = []
        self.steps_done += 1
        if self.steps_done in self.path.events:
            self.path.events[self.steps_done].execute(game.world, game.player)
        
        event = self.path.trigger_random_event(game.world, game.player)
        if (event):
            self.triggered_event.append(event)
        
        
        if self.steps_done >= self.path.steps:
            # Arrivé à destination
            destination = self.path.get_other_end(game.player.location)
            game.player.location.entities.remove(game.player)
            destination.add_entity(game.player)
            game.current_area = destination 
            return True
        return False
    
    def __str__(self):
        return f"{self.path}"