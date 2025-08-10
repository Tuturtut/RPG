from world.locations.Location import Location

class Area(Location):
    def __init__(self, name, description="", subareas=None):
        super().__init__()
        self.name = name
        self.description = description
        self.subareas = subareas or []
        self.parent = None
        if subareas:
            for subarea in subareas:
                subarea.parent = self
        self.paths = {}
    
    def add_connection(self, other_area, path):
        self.paths[other_area] = path
    
    def is_subarea(self):
        return self.parent is not None
    
    def get_name(self):
        return self.name
    
    def get_full_name(self):
        if self.is_subarea():
            return f"{self.parent.get_full_name()} > {self.name}"
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
        return f"[{self.name}]"
