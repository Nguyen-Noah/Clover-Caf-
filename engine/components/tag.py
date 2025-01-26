from dataclasses import dataclass

from engine.components.component import Component
from engine.components.component_deserializer import register_component


@dataclass
@register_component
class TagComponent(Component):
    name: str

    def __post_init__(self):
        super().__init__()

    def serialize(self):
        data = super().serialize()
        data.update({
            "name": self.name
        })
        return data

    @classmethod
    def deserialize(cls, data):
        return cls(data['name'])