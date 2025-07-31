class EntityPath:
    def __init__(self, entity, path):
        self.entity = entity
        self.path = path
        self.steps_done = 0
        self.triggered_event = []
    
    def get_triggered_events(self):
        if self.steps_done in self.path.events:
            self.triggered_event.append(self.path.events[self.steps_done])
        return self.triggered_event
    
    def get_steps_done(self):
        return self.steps_done
    
    def get_name(self):
        return self.path.get_name()
    
    def advance(self, game):
        self.triggered_event = []
        self.steps_done += 1
        if self.steps_done in self.path.events:
            self.path.events[self.steps_done].execute(game.world, self.entity)
        
        event = self.path.trigger_random_event(game.world, self.entity)
        if (event):
            self.triggered_event.append(event)
        
        
        if self.steps_done >= self.path.steps:


            # Arrivé à destination
            destination = self.path.get_other_end(self.entity.location)

            from utils.debug import log
            log(f"{self.entity.name} arrivé à {destination.name}")

            self.entity.location.entities.remove(self.entity)
            destination.add_entity(self.entity)
            game.current_area = destination 
            return True
        return False
    
    def __str__(self):
        return f"{self.path}"