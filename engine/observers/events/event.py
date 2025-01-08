from engine.observers.events import EventType

class Event:
    def __init__(self, event_type=EventType.USER_EVENT):
        self.type = event_type