import pygame, sys

from engine.ecs.entity import Entity
from engine.observers.event_system import EventSystem
from engine.observers.events.event import Event
from engine.observers.observer import Observer
from engine.utils.elements import ElementSingleton

class Game(ElementSingleton, Observer):
    def __init__(self):
        ElementSingleton.__init__(self)
        Observer.__init__(self)
        EventSystem.add_observer(self)
        
    def load(self):
        pass

    # for handling events
    def on_notify(self, entity: Entity, event: Event):
        pass
    
    def update(self):
        pass
    
    def run(self):
        self.load()
        self.f = False      # used for profiling
        while True:
            if self.f:
                break
            self.update()

    def quit(self):
        self.current_scene.save()
        pygame.quit()
        sys.exit()