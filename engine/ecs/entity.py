from ..utils.elements import Element
from ..components.transform import Transform
from ..primitives.vec2 import vec2
from ..components.component_deserializer import deserialize_component

class Entity(Element):
    def __init__(self, name, z_index=0, transform=Transform()):
        super().__init__()
        self.name = name
        self.components = []
        self.transform = transform
        self.z_index = z_index

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

    def imgui(self):
        for component in self.components:
            component.imgui()

    def serialize(self):
        return {
            "name": self.name,
            "z_index": self.z_index,
            "transform": self.transform.serialize() if self.transform else None,
            "components": [component.serialize() for component in self.components]
        }
    
    @classmethod
    def deserialize(cls, data):
        transform = Transform.deserialize(data["transform"]) if data.get("transform") else Transform()
        entity = cls(data["name"], z_index=data["z_index"], transform=transform)

        for component_data in data["components"]:
            component_type = deserialize_component(component_data)
            entity.add_component(component_type)

        return entity