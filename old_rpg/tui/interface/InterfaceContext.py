class InterfaceContext:
    def __init__(self, controller):
        self.controller = controller
    
    def handle_input(self, key):
        raise NotImplementedError("handle_input must be implemented by subclasses")
    
    def render(self):
        raise NotImplementedError("render must be implemented by subclasses")