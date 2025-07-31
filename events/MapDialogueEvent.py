from events.Event import Event


class MapDialogueEvent(Event):
    def __init__(self, dialogue_message):
        super().__init__(description="Dialogue simple")
        self.dialogue_message = dialogue_message

        self.message = None

    def execute(self, world_state, entity):
        # if entity instanceof Player:
        if entity.is_player():
            self.message = f"[Événement] {self.dialogue_message}"
        
