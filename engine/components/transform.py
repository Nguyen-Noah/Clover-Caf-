from ..primitives.vec2 import vec2

class Transform:
    def __init__(self, position=vec2(0, 0), scale=vec2(0, 0)):
        self.position = position
        self.scale = scale

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
        return self.position == o.position and self.scale == o.scale
    
    def serialize(self):
        return {
            "position": self.position.serialize(),
            "scale": self.scale.serialize()
        }
    
    @classmethod
    def deserialize(cls, data):
        position = vec2().deserialize(data["position"]) if "position" in data else vec2(0, 0)
        scale = vec2().deserialize(data["scale"]) if "scale" in data else vec2(0, 0)
        return cls(position=position, scale=scale)