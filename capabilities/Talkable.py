class Talkable:
    def __init__(self):
        self.dialogues = []
        self.languages = [] 

    def add_dialogue(self, dialogue_entry):
        self.dialogues.append(dialogue_entry)

    def get_dialogue(self, world_state, observer=None):
        valid = [d for d in self.dialogues if d.is_available(self, world_state)]
        if not valid:
            return f"{self.name} : '...'"

        best = max(valid, key=lambda d: d.priority)

        if observer and hasattr(observer, "languages"):
            if any(lang in observer.languages for lang in self.languages):
                return f"{self.name} : '{best.text}'"
            else:
                return f"{self.name} s’exprime dans un langage incompréhensible."
        else:
            return f"{self.name} : '{best.text}'"

def debug_dialogue_selection(self, world_state):
        valid_dialogues = [d for d in self.dialogues if d.is_available(self, world_state)]

        if not valid_dialogues:
            return

        for d in valid_dialogues:
            print(f"  - Priorité {d.priority} → \"{d.text}\"")

        best = max(valid_dialogues, key=lambda d: d.priority)
