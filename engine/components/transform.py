from .component import Component
from ..primitives.vec2 import vec2

class Transform(Component):
    def __init__(self, position=None, scale=None, rotation=0.0, z_index=0):
        super().__init__()
        self.position = position if position else vec2(0, 0)
        self.scale = scale if scale else vec2(1, 1)
        self.rotation = rotation
        self.z_index = z_index

    def copy(self, to=None):
        if to:
            to.position = self.position.copy()
            to.scale = self.scale.copy()
        else:
            return Transform(self.position.copy(), self.scale.copy())

    def equals(self, o):
        if o is None:
            return False
        if not isinstance(o, Transform):
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
        return cls(position=position, scale=scale)