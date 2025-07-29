class SelectionHelper:
    def __init__(self, items):
        self.items = items
        self.index = 0

    def move_left(self):
        if self.items:
            self.index = (self.index - 1) % len(self.items)

    def move_right(self):
        if self.items:
            self.index = (self.index + 1) % len(self.items)

    def select_by_number(self, number):
        if 1 <= number <= len(self.items):
            self.index = number - 1
            return True
        return False

    def get_selected(self):
        if self.items:
            return self.items[self.index]
        return None
