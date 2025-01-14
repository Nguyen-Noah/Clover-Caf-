from engine.components.component import Component
from engine.components.component_deserializer import register_component

@register_component
class NonPickable(Component):
    def serialize(self):
        return super().serialize()

    @classmethod
    def deserialize(cls, data):
        return cls()