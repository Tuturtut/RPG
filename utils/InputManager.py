class InputManager:
    def __init__(self):
        self.keymap = {}
    
    def register(self, key, action_name):
        """Register a key with an action name."""
        self.keymap[key] = action_name
    
    def get_action(self, key):
        """Get the action name for a given key."""
        return self.keymap.get(key, None)