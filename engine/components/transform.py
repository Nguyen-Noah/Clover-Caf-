from dataclasses import dataclass

from .component import Component
from .component_deserializer import register_component
from engine.primitives.vec2 import vec2

@dataclass
@register_component
class TransformComponent(Component):
    position: vec2 = vec2()
    scale: vec2 = vec2(1, 1)
    rotation: float = 0
    z_index: int = 0

    def __post_init__(self):
        super().__init__()

    def copy(self, to=None):
        if to:
            to.position = self.position.copy()
            to.scale = self.scale.copy()
            to.rotation = self.rotation * 1
            to.z_index = self.z_index * 1
        else:
            return TransformComponent(self.position.copy(), self.scale.copy())

    def equals(self, o):
        if o is None:
            return False
        if not isinstance(o, TransformComponent):
            return False
        return self.position == o.position and self.scale == o.scale and self.rotation == o.rotation and self.z_index == o.z_index

    def serialize(self):
        data = super().serialize()
        data.update({
            "position": self.position.serialize(),
            "scale": self.scale.serialize(),
            "rotation": self.rotation,
            "z_index": self.z_index
        })
        return data
    
    @classmethod
    def deserialize(cls, data):
        position = vec2().deserialize(data["position"]) if "position" in data else vec2(0, 0)
        scale = vec2().deserialize(data["scale"]) if "scale" in data else vec2(0, 0)
        return cls(position=position, scale=scale, rotation=data.get('rotation'), z_index=data.get('z_index'))