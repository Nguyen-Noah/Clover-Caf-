from engine.ecs.entity import Entity
from engine.observers.events.event import Event


class Observer:
    def on_notify(self, event: Event, entity: Entity):
        pass