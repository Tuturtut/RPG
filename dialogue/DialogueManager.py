import os
import json
from dialogue.Dialogue import DialogueEntry

class DialogueManager:
    def __init__(self, dialogue_folder="data/dialogues"):
        self.entities = {}  # dict : nom → instance de entity
        self.dialogue_folder = dialogue_folder

    def register(self, entity):
        self.entities[entity.name] = entity
        self.load_dialogues(entity)

    def load_dialogues(self, entity):
        entity.dialogues.clear()  # on efface les anciens dialogues
        path = os.path.join(self.dialogue_folder, f"{entity.name}.json")

        if not os.path.exists(path):
            print(f"[DM] Pas de dialogue pour {entity.name} ({path})")
            return

        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for entry in data:
                    entity.add_dialogue(DialogueEntry.from_json(entry))
                print(f"[DM] {len(entity.dialogues)} dialogues chargés pour {entity.name}")
            except Exception as e:
                print(f"[DM] Erreur dans {path} : {e}")

    def reload_all_dialogues(self):
        for entity in self.entities.values():
            self.load_dialogues(entity)
            print(f"[DM] Dialogues rechargés pour {entity.name}")
