from ..utils.elements import Element
from ..components.transform import Transform

class Entity(Element):
    def __init__(self, name, transform=Transform()):
        super().__init__()
        self.name = name
        self.components = []
        self.transform = transform

    def get_component(self, component_class):
        for component in self.components:
            if isinstance(component, component_class):
                return component
        return None
    
    def remove_component(self, component_class):
        for i, component in enumerate(self.components):
            if isinstance(component, component_class):
                self.components.pop(i)
                break

    def add_component(self, c):
        self.components.append(c)
        c.entity = self

    def update(self, dt):
        for component in self.components:
            component.update(dt)

    def start(self):
        for component in self.components:
            component.start()