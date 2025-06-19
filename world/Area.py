class Area:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.entities = []
        self.events = []

    def add_entity(self, entity):
        self.entities.append(entity)
        entity.area = self

    def add_event(self, event):  # <- cette méthode est nécessaire
        self.events.append(event)

    def check_events(self, world_state):
        for event in self.events:
            event.check_and_trigger(world_state, self)

    def describe(self):
        print(f"\n[Zone] {self.name}")
        print(f"{self.description}\n")
        if self.entities:
            print("Personnes présentes :")
            for entity in self.entities:
                print(f"- {entity.name}")
        else:
            print("Il n'y a personne ici.")
