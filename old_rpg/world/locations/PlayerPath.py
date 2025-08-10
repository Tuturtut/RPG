from world.locations.EntityPath import EntityPath

class PlayerPath(EntityPath):
    def __init__(self, player, path, origin):
        super().__init__(player, path, origin)
    
