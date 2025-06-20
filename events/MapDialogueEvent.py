class MapDialogueEvent:
    def __init__(self, message):
        self.message = message

    def execute(self, world_state, player):
        print(f"[Événement] {self.message}")
