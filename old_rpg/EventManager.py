class EventManager:
    _listeners = []

    @classmethod
    def register(cls, listener):
        cls._listeners.append(listener)

    @classmethod
    def emit(cls, event, data=None):
        for listener in cls._listeners:
            listener(event, data)