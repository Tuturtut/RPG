class InputManager:
    def __init__(self):
        self.keymap = {}
    
    def register(self, key, state, action_name):
        """Register a key with an action name."""
        if key not in self.keymap:
            self.keymap[key] = {}
        self.keymap[key][state] = action_name

    def get_action(self, key, state):
        """Get the action name for a given key."""
        return self.keymap.get(key, {}.get(state))