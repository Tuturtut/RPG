from events.Event import Event


class MapDialogueEvent(Event):
    def __init__(self, dialogue_message):
        super().__init__("Dialogue")
        self.dialogue_message = dialogue_message

    def execute(self, entity, controller):
        return {
            "type": "dialogue",
            "message": self.dialogue_message
        }