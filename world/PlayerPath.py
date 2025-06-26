class PlayerPath:
    def __init__(self, path):
        self.path = path          # Le Path emprunté
        self.steps_done = 0       # Nombre de pas effectués

    def advance(self, game):
        self.steps_done += 1
        if self.steps_done in self.path.events:
            self.path.events[self.steps_done].execute(game.world, game.player)

        self.path.trigger_random_event(game.world, game.player)
        game.wait(10)

        if self.steps_done >= self.path.steps:
            # Arrivé à destination
            destination = self.path.get_other_end(game.player.location)
            game.player.location.entities.remove(game.player)
            destination.add_entity(game.player)
            game.current_area = destination 
            return True
        return False
    
    def get_triggered_events(self):
        triggered = []
        if self.steps_done in self.path.events:
            triggered.append(self.path.events[self.steps_done])
        return triggered

