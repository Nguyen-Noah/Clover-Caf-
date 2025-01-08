from typing import Optional
from engine.observers.events.event import Event
from engine.observers.observer import Observer

class EventSystem:
    observers = []

    @classmethod
    def add_observer(cls, observer: Observer):
        cls.observers.append(observer)

    @classmethod
    def notify(cls, event: Event, entity: Optional[Event] = None):
        for observer in cls.observers:
            observer.on_notify(entity, event)
