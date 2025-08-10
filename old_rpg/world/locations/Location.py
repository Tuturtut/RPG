class Location:
    def __init__(self):
        self.entities = []
        self.events = []
    
    def add_entity(self, entity):
        self.entities.append(entity)
        entity.location = self
    
    def get_entities(self):
        return self.entities
    
    def remove_entity(self, entity):
        self.entities.remove(entity)

    def get_other_entities(self, entity):
        return [e for e in self.entities if e != entity]

    def add_event(self, event):
        self.events.append(event)

    def trigger_events(self, entity, controller):
        for event in self.events:
            result = event.execute([entity], controller)
            if result:
                controller.handle_event_result(result)