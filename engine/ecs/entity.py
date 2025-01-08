import imgui

from ..utils.elements import Element
from ..components.transform import Transform
from ..components.component_deserializer import deserialize_component

class Entity(Element):
    ID_COUNTER = 1

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.components = []
        self.transform = None
        self.uid = Entity.ID_COUNTER
        Entity.ID_COUNTER += 1
        self.do_serialization = True
        self.alive = True

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
        c.generate_id()
        self.components.append(c)
        c.entity = self

    def start(self):
        for component in self.components:
            component.start()

    def destroy(self):
        self.alive = False
        for component in self.components:
            component.destroy()

    def imgui(self):
        for component in self.components:
            show, _ = imgui.collapsing_header(component.__class__.__name__)
            if show:
                component.imgui()

    def init(max_id):
        Entity.ID_COUNTER = max_id

    def set_no_serialize(self):
        self.do_serialization = False

    def editor_update(self, dt):
        for component in self.components:
            component.editor_update(dt)

        return self.alive

    def update(self, dt):
        for component in self.components:
            component.update(dt)

        return self.alive

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "components": [component.serialize() for component in self.components]
        }
    
    @classmethod
    def deserialize(cls, data):
        entity = cls(data["name"])

        for component_data in data["components"]:
            component_type = deserialize_component(component_data)
            entity.add_component(component_type)
        entity.transform = entity.get_component(Transform)

        return entity