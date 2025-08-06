class Event:
    def __init__(self, description=None):
        self.message = None 
        self.description = description or "Événement"

    def execute(self, entity, controller):
        """
        Return a dictionary with the following keys:
        {
            "type": "info" | "fight" | "dialogue" | ...,
            "message": The message to display
        }
        """
        raise NotImplementedError("Event subclasses must implement execute()")

    def __str__(self):
        return self.description
    
    def __repr__(self):
        return f"Event(description={self.description})"