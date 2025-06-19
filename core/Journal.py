class Journal:
    def __init__(self):
        self.entries = {}

    def add(self, day, text):
        if day not in self.entries:
            self.entries[day] = []
        self.entries[day].append(text)

    def show(self):
        print("\n=== Journal de bord ===")
        for day in sorted(self.entries):
            print(f"\n— Jour {day} —")
            for entry in self.entries[day]:
                print(f"• {entry}")
