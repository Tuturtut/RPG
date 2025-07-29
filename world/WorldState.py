from world.Weather import Weather

class WorldState:
    def __init__(self):
        self.day = 1
        self.weather = Weather()
        self.flags = set()

    def advance_day(self):
        self.day += 1
        self.weather.set_weather()
        print(f"[Monde] Passage au jour {self.day} — météo : {self.weather.current}")

    def add_flag(self, flag):
        self.flags.add(flag)

    def has_flag(self, flag):
        return flag in self.flags
