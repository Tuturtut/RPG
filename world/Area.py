class Area:
    def __init__(self, name, description="", subareas=None):
        self.name = name
        self.description = description
        self.subareas = subareas or []
        self.parent = None
        if subareas:
            for subarea in subareas:
                subarea.parent = self
        self.entities = []
        self.events = []
        self.paths = {}
    
    def add_connection(self, other_area, path):
        self.paths[other_area] = path
    

    def get_entities(self):
        """
        Retourne la liste des entitées présentes dans la zone.
        """
        return self.entities
    
    def get_other_entities(self, entity):
        return [e for e in self.entities if e != entity]

    def add_entity(self, entity):
        self.entities.append(entity)
        entity.location = self

    def add_event(self, event):  # <- cette méthode est nécessaire
        self.events.append(event)

    def check_events(self, world_state):
        for event in self.events:
            event.check_and_trigger(world_state, self)
    
    def is_subarea(self):
        return self.parent is not None
    
    def getName(self):
        return self.name
    
    def getFullName(self):
        if self.is_subarea():
            return f"{self.parent.getFullName()} > {self.name}"
        return self.name

    def describe(self):
        print(f"\n[Zone] {self.name}")
        print(f"{self.description}\n")
        if self.entities:
            print("Personnes présentes :")
            for entity in self.entities:
                print(f"- {entity.name}")
        else:
            print("Il n'y a personne ici.")

    def __str__(self):
        return f"Area(name={self.name}, description={self.description})"
