class DialogueEntry:
    def __init__(self, text, conditions=None, priority=1, tag=None):
        self.text = text
        self.conditions = conditions or []
        self.priority = priority
        self.tag = tag

    def is_available(self, entity, world_state):
        return all(condition(entity, world_state) for condition in self.conditions)

    @classmethod
    def from_json(cls, json_data):
        from dialogue.Dialogue import parse_condition_string
        text = json_data.get("text")
        raw_conditions = json_data.get("conditions", [])
        parsed_conditions = [parse_condition_string(c) for c in raw_conditions]
        priority = json_data.get("priority", 1)
        tag = json_data.get("tag")

        return cls(text, parsed_conditions, priority, tag)


def parse_condition_string(condition_str):
    try:
        if condition_str.startswith("weather == "):
            target_weather = condition_str.split("==")[1].strip()
            return lambda entity, ws: ws.weather.current == target_weather

        if condition_str.startswith("flag == "):
            flag = condition_str.split("==")[1].strip()
            return lambda entity, ws: ws.has_flag(flag)

        raise ValueError(f"[Condition inconnue] : {condition_str}")
    except Exception as e:
        print(f"[Erreur de parsing condition] : {condition_str} → {e}")
        return lambda entity, ws: False
