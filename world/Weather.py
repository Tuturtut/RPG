import random

class Weather:
    def __init__(self):
        self.current = "sunny"

    def set_weather(self, condition=None):
        if condition:
            self.current = condition
        else:
            self.current = random.choice(["sunny", "rainy", "foggy", "windy"])
        print(f"[Météo] Nouvelle météo : {self.current}")
