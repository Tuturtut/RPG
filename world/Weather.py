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
    
    def update(self, time_manager=None):
        """
        Met à jour la météo dynamiquement. Peut être appelée à chaque tick du jeu.
        """
        chance_of_change = 0.05

        if random.random() < chance_of_change:
            previous_weather = self.current
            options = ["sunny", "rainy", "foggy", "windy"]
            options.remove(self.current)
            self.current = random.choice(options)