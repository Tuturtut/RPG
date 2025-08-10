class TimeManager:
    def __init__(self):
        self.minutes = 0
        self.day = 1

    def advance_minutes(self, amount):
        self.minutes += amount
        previous_day = self.day
        self.day = (self.minutes // 1440) + 1  # 1 jour = 1440 min

        if self.day > previous_day:
            return True  # indique qu’un nouveau jour a commencé
        return False

    def get_time_of_day(self):
        hours = (self.minutes // 60) % 24
        if 6 <= hours < 12:
            return "matin"
        elif 12 <= hours < 18:
            return "après-midi"
        elif 18 <= hours < 23:
            return "soir"
        else:
            return "nuit"

    def get_day(self):
        return self.day

    def get_hours_minutes(self):
        h = (self.minutes // 60) % 24
        m = self.minutes % 60
        return f"{h:02d}:{m:02d}"
