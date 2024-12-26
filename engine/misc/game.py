import pygame, sys
from ..utils.elements import ElementSingleton

class Game(ElementSingleton):
    def __init__(self):
        super().__init__()
        
    def load(self):
        pass
    
    def update(self):
        pass
    
    def run(self):
        self.load()
        while True:
            self.update()