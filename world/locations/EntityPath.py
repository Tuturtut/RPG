class EntityPath:
    def __init__(self, entity, path, origin):
        self.entity = entity
        self.path = path
        self.steps_done = 0
        self.origin = origin
        self.origin.remove_entity(self.entity)
        self.path.add_entity(self.entity)
    
    
    def get_steps_done(self):
        return self.steps_done
    
    def get_name(self):
        return f"{self.origin.name} -> {self.path.get_other_end(self.origin).name}"
    
    def advance(self, game):
        self.steps_done += 1
        step_index = self.steps_done
        if self.origin == self.path.end:
            step_index = self.path.steps - self.steps_done - 1
            
        if self.steps_done >= self.path.steps:


            destination = self.path.get_other_end(self.origin)

            self.path.remove_entity(self.entity)
            destination.add_entity(self.entity)
            game.current_area = destination 
            return True
        return False
    
    def __str__(self):
        return f"{self.origin.name} -> {self.path.get_other_end(self.origin).name}"